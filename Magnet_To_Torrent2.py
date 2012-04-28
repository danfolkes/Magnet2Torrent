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

def showHelp():
  print ""
  print "USAGE: " + pt.basename( sys.argv[0] ) + " MAGNET [OUTPUT]"
  print "  MAGNET\t- the magnet url"
  print "  OUTPUT\t- the output torrent file name"
  print ""

if len(sys.argv) < 2:
  showHelp();
  sys.exit(0)

magnet = sys.argv[1]
digest = hashlib.md5(sys.argv[1]).hexdigest()
output = pt.abspath(digest + ".torrent" )

if len(sys.argv) == 3:
  if pt.isdir(sys.argv[2]):
    output = pt.abspath(pt.join(sys.argv[2],digest + ".torrent"))
  elif pt.isdir(pt.dirname(pt.abspath(sys.argv[2]))) == True:
    output = pt.abspath(sys.argv[2])
  else:
    showHelp();
    print "Invalid output folder: " + pt.dirname(pt.abspath(sys.argv[2]))
    print ""
    sys.exit(0)

tempdir = tempfile.mkdtemp()
ses = lt.session()
#ses.listen_on(6881, 6891)
params = {
    'save_path': tempdir,
    'duplicate_is_error': True}
handle = lt.add_magnet_uri(ses, magnet, params)
#ses.start_dht()
print 'saving torrent file here : ' + output + " ..."
while (not handle.has_metadata()):
    try:
        time.sleep(.1)
    except KeyboardInterrupt:
        print "Abrorting..."
        ses.pause()
        print "Cleanup dir " + tempdir
        shutil.rmtree(tempdir)
        sys.exit(0)

torinfo = handle.get_torrent_info()

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
 
#Uncomment to Download the Torrent:
#    print 'starting torrent download...'
 
#    while (handle.status().state != lt.torrent_status.seeding):
#        s = handle.status()
#        time.sleep(55)
#        print 'downloading...'


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
