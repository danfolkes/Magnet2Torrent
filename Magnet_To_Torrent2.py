#!/usr/bin/env python
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

import shutil
import tempfile
import os.path as pt
import sys
import libtorrent as lt
from time import sleep
from argparse import ArgumentParser


def magnet2torrent(magnet, output_name=None):
    if output_name and \
            not pt.isdir(output_name) and \
            not pt.isdir(pt.dirname(pt.abspath(output_name))):
        print("Invalid output folder: " + pt.dirname(pt.abspath(output_name)))
        print("")
        sys.exit(0)

    tempdir = tempfile.mkdtemp()
    ses = lt.session()
    params = {
        'save_path': tempdir,
        'storage_mode': lt.storage_mode_t(2),
        'paused': False,
        'auto_managed': True,
        'duplicate_is_error': True
    }
    handle = lt.add_magnet_uri(ses, magnet, params)

    print("Downloading Metadata (this may take a while)")
    while (not handle.has_metadata()):
        try:
            sleep(1)
        except KeyboardInterrupt:
            print("Aborting...")
            ses.pause()
            print("Cleanup dir " + tempdir)
            shutil.rmtree(tempdir)
            sys.exit(0)
    ses.pause()
    print("Done")

    torinfo = handle.get_torrent_info()
    torfile = lt.create_torrent(torinfo)

    output = pt.abspath(torinfo.name() + ".torrent")

    if output_name:
        if pt.isdir(output_name):
            output = pt.abspath(pt.join(
                output_name, torinfo.name() + ".torrent"))
        elif pt.isdir(pt.dirname(pt.abspath(output_name))):
            output = pt.abspath(output_name)

    print("Saving torrent file here : " + output + " ...")
    torcontent = lt.bencode(torfile.generate())
    f = open(output, "wb")
    f.write(lt.bencode(torfile.generate()))
    f.close()
    print("Saved! Cleaning up dir: " + tempdir)
    ses.remove_torrent(handle)
    shutil.rmtree(tempdir)

    return output

def main():
    parser = ArgumentParser(description="A command line tool that converts magnet links in to .torrent files")
    parser.add_argument('-m','--magnet', help='The magnet url')
    parser.add_argument('-o','--output', help='The output torrent file name')

    #
    # This second parser is created to force the user to provide
    # the 'output' arg if they provide the 'magnet' arg.
    #
    # The current version of argparse does not have support
    # for conditionally required arguments. That is the reason
    # for creating the second parser
    #
    # Side note: one should look into forking argparse and adding this
    # feature.
    #
    conditionally_required_arg_parser = ArgumentParser(description="A command line tool that converts magnet links in to .torrent files")
    conditionally_required_arg_parser.add_argument('-m','--magnet', help='The magnet url')
    conditionally_required_arg_parser.add_argument('-o','--output', help='The output torrent file name', required=True)

    magnet = None
    output_name = None

    #
    # Attempting to retrieve args using the new method
    #
    args = vars(parser.parse_known_args()[0])
    if args['magnet'] is not None:
        magnet = args['magnet']
        argsHack = vars(conditionally_required_arg_parser.parse_known_args()[0])
        output_name = argsHack['output']
    if args['output'] is not None and output_name is None:
        output_name = args['output']
        if magnet is None:
            #
            # This is a special case.
            # This is when the user provides only the "output" args.
            # We're forcing him to provide the 'magnet' args in the new method
            #
            print ('usage: {0} [-h] [-m MAGNET] -o OUTPUT'.format(sys.argv[0]))
            print ('{0}: error: argument -m/--magnet is required'.format(sys.argv[0]))
            sys.exit()
    #
    # Defaulting to the old of doing things
    # 
    if output_name is None and magnet is None:
        if len(sys.argv) >= 2:
            magnet = sys.argv[1]
        if len(sys.argv) >= 3:
            output_name = sys.argv[2]

    magnet2torrent(magnet, output_name)


if __name__ == "__main__":
    main()
