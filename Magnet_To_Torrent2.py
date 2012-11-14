#!/usr/bin/python
'''
Created on Apr 19, 2012
@author: dan, Faless

    GNU GENERAL PUBLIC LICENSE - Version 3
                       
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    http://www.gnu.org/licenses/gpl-3.0.txt

'''

import shutil, tempfile, os.path as pt, sys, libtorrent as lt, time, hashlib


def magnet2torrent(magnet, output_name = None):
  if output_name and \
      not pt.isdir(output_name) and \
      not pt.isdir(pt.dirname(pt.abspath(output_name))):
    print "Invalid output folder: " + pt.dirname(pt.abspath(output_name))
    print ""
    return

  tempdir = tempfile.mkdtemp()
  ses = lt.session()
  params = {
    'save_path': tempdir,
    'duplicate_is_error': True,
    'storage_mode': lt.storage_mode_t(2),
    'paused': False,
    'auto_managed': True,
    'duplicate_is_error': True
  }
  handle = lt.add_magnet_uri(ses, magnet, params)
  print "Downloading Metadata (this may take a while)"
  while (not handle.has_metadata()):
    try:
      time.sleep(1)
    except KeyboardInterrupt:
      print "Abrorting..."
      ses.pause()
      print "Cleanup dir " + tempdir
      shutil.rmtree(tempdir)
      return
  print "done"

  torinfo = handle.get_torrent_info()

  output = pt.abspath(torinfo.name() + ".torrent" )

  if output_name:
    if pt.isdir(output_name):
      output = pt.abspath(pt.join(output_name, torinfo.name() + ".torrent"))
    elif pt.isdir(pt.dirname(pt.abspath(output_name))) == True:
      output = pt.abspath(output_name)
  print 'saving torrent file here : ' + output + " ..."

  fs = lt.file_storage()
  for file in torinfo.files():
    fs.add_file(file)
  torfile = lt.create_torrent(fs)
  torfile.set_comment(torinfo.comment())
  torfile.set_creator(torinfo.creator())

  torcontent = lt.bencode(torfile.generate())
  f = open(output, "wb")
  f.write(lt.bencode(torfile.generate()))
  f.close()
  print 'Saved! Cleaning up dir: ' + tempdir
  shutil.rmtree(tempdir)
  return output
 

def showHelp():
  print ""
  print "USAGE: " + pt.basename( sys.argv[0] ) + " MAGNET [OUTPUT]"
  print "  MAGNET\t- the magnet url"
  print "  OUTPUT\t- the output torrent file name"
  print ""

if __name__ == "__main__":
  if len(sys.argv) < 2:
    showHelp();
    sys.exit(0)
  magnet = sys.argv[1]
  output_name = None
  if len(sys.argv) >= 3:
    output_name = sys.argv[2]
  magnet2torrent(magnet, output_name)
