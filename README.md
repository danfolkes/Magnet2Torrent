# Magnet2Torrent

A command line tool that converts magnet links in to .torrent files.

### This project is mostly abandoned. I will still merge most pull requests.

## Requirements
* python
* python-libtorrent (libtorrent-rasterbar version 0.16 or later)

## Install python-libtorrent on Ubuntu
`sudo apt-get install python-libtorrent -y`

## Install python-libtorrent on macOS
`brew install libtorrent-rasterbar --with-python`

## Install python-libtorrent on Fedora
`sudo dnf install rb_libtorrent-python2`

## How to Use
`python Magnet_To_Torrent2.py <magnet link> [torrent file]`

### Example
`python Magnet_To_Torrent2.py -m "magnet:?xt=urn:btih:49fbd26322960d982da855c54e36df19ad3113b8&dn=ubuntu-12.04-desktop-i386.iso&tr=udp%3A%2F%2Ftracker.openbittorrent.com" -o ubunut12-04.iso`

## Licenses
All code is licensed under the [GPL version 3](http://www.gnu.org/licenses/gpl.html)
