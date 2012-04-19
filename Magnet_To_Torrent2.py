'''
Created on Apr 19, 2012
@author: dan

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
 
if __name__ == '__main__':
    import libtorrent as lt
    import time
 
    TorrentFilePath = "/home/dan/torrentfiles/" + str(time.time()) + "/"
    TorrentFilePath2 = "/home/dan/torrentfiles/" + str(time.time()) + "/" + str(time.time()) + ".torrent"
    ses = lt.session()
    #ses.listen_on(6881, 6891)
    params = {
        'save_path': TorrentFilePath,
        'duplicate_is_error': True}
    link = "magnet:?xt=urn:btih:599e3fb0433505f27d35efbe398225869a2a89a9&dn=ubuntu-10.04.4-server-i386.iso&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.ccc.de%3A80"
    handle = lt.add_magnet_uri(ses, link, params)
    #ses.start_dht()
    print 'saving torrent file here : ' + TorrentFilePath2 + " ..."
    while (not handle.has_metadata()):
        time.sleep(.1)
 
    torinfo = handle.get_torrent_info()
 
    fs = lt.file_storage()
    for file in torinfo.files():
        fs.add_file(file)
    torfile = lt.create_torrent(fs)
    torfile.set_comment(torinfo.comment())
    torfile.set_creator(torinfo.creator())
 
    f = open(TorrentFilePath2 + "torrentfile.torrent", "wb")
    f.write(lt.bencode(torfile.generate()))
    f.close()
    print 'saved and closing...'
 
#Uncomment to Download the Torrent:
#    print 'starting torrent download...'
 
#    while (handle.status().state != lt.torrent_status.seeding):
#        s = handle.status()
#        time.sleep(55)
#        print 'downloading...'


'''
Created on Apr 19, 2012
@author: dan

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
