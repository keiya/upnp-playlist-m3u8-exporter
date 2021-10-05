import upnpclient
import pprint
pp = pprint.PrettyPrinter(indent=4)
import xml.etree.ElementTree as ET
import sys

requested_count = 100000

if len(sys.argv) < 3:
  print("python3 upnp.py http(s)://host:port playlist.m3u8")
  exit(1)
d = upnpclient.Device("{}/DeviceDescription.xml".format(sys.argv[1]))
s = d.services

def parse_playlists(xml):
  # parsing playlists
  playlists = []
  root = ET.fromstring(xml)
  for container in root.findall("./"):
    container_attr = container.attrib
    title_elm = container.find(".//dc:title", namespaces={'dc': 'http://purl.org/dc/elements/1.1/'})
    title = title_elm.text
    result = { 'id': container_attr['id'], 'title': title }
    playlists.append(dict(result))
  return playlists

def parse_songs(xml):
  songs = []
  root = ET.fromstring(xml)
  for item in root.findall("./{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}item"):
    item_attr = item.attrib
    title_elm = item.find(".//dc:title", namespaces={'dc': 'http://purl.org/dc/elements/1.1/'})
    creator_elm = item.find(".//dc:creator", namespaces={'dc': 'http://purl.org/dc/elements/1.1/'})
    resources = [{"meta": res.attrib, "url": res.text} for res in item.findall(".//{urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/}res")]
    result = { 'id': item_attr['id'], 'title': title_elm.text, 'creator': creator_elm.text, 'resources': resources}
    songs.append(dict(result))
  return songs

# + root : ObjectID = 0 
# +--+ Playlists : ObjectID = 0/0 
#    +--- Playlist 1 : ObjectID = 0/0/0
#    +--- Playlist 2 : ObjectID = 0/0/1
#    +--- Playlist 3 : ObjectID = 0/0/2
#         ...
#    +--- Playlist n : ObjectID = 0/0/n
# +--- Media Library : ObjectID = 0/1 
# +--- Playback Stream : ObjectID = 0/2
browsed_playlists = s[0].actions[0](ObjectID="0/0", BrowseFlag="BrowseDirectChildren", Filter="*", StartingIndex=0, RequestedCount=requested_count, SortCriteria="")
playlists = parse_playlists(browsed_playlists['Result'])

print("Enter the playlist ID you want to generate: [e.g. 0/0/1 ]")
for p in playlists:
  print("{} = {}".format(p['id'], p['title']))
id = input()

browsed_playlist = s[0].actions[0](ObjectID=id, BrowseFlag="BrowseDirectChildren", Filter="*", StartingIndex=0, RequestedCount=requested_count, SortCriteria="")
songs = parse_songs(browsed_playlist['Result'])

#pp.pprint(songs)

def duration_to_sec(formatted_duration):
  hour, minute, second = formatted_duration.split(":")
  return round(int(hour) * 3600 + int(minute) * 60 + float(second))

with open(sys.argv[2],'w') as fh:
  fh.write("#EXTM3U\n")
  for song in songs:
    duration = duration_to_sec(song['resources'][0]['meta']['duration'])
    extinf = "#EXTINF:{},{} - {}".format(duration, song["creator"], song["title"])
    line = '\n'.join([extinf, song['resources'][0]['url']])
    fh.write(line + "\n")
  print("exported to {}".format(sys.argv[2]))
