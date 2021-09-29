# M3U8 playlist generator/exporter from UPnP Server
This script accesses the playlists of UPnP Servers such as `foo_upnp` and exports the contents.

## Before Use
Install required package:

```
pip install upnpclient
```

## Usage
Run with `python3 upnp.py [UPnP URL] [filename]`. 
The playlists in the server will be listed. 

```
$ python3 upnp.py http://192.168.0.206:56923 playlist.m3u8
Enter the playlist ID you want to generate: [e.g. 0/0/1 ]
0/0/0 = Default
0/0/1 = GWAVE
0/0/2 = Favorites
0/0/3 = Snarky Puppy
...
0/0/12 = Relax songs
```

Enter the ID of the playlist you want to export and press Enter.

```
0/0/1 [Enter]
```

In the above example, the contents will be output to playlist.m3u8.

```
#EXTINF:568,青葉りんご - Heaven's Fall (zts Remix)
http://192.168.0.206:56923/content/6882630f375cb8be83409c848a47cf46.flac
#EXTINF:473,みとせのりこ - Personalizer
http://192.168.0.206:56923/content/0617be2cfde3c95743770e10abd11e99.flac
#EXTINF:339,SHIHO - Fallin Snow
http://192.168.0.206:56923/content/1266a279c7c872ade4471cce6416cbfc.flac
#EXTINF:303,Rita - Dream Walker
http://192.168.0.206:56923/content/20eeea5fde4981ab4c9c528454e8a4f9.flac
```

## Recommended Profile Settings for Foobar2000's foo_upnp
If the UPnP Server you are connecting to is a Foobar 2000, configure the Foobar 2000 in this way.

- Open Preferences > Tools > UPnP > Server > Streaming Profiles
- Select `foobar2000` in `Select profile to edit`
- Click `New`
    - (Hint: You can copy the foobar2000 profile by loading it and then clicking New. Or use any other profile as a base.)
- Enter `python-requests` for "contain"
- For the other values, set them appropriately for the device that will play the playlist.
- The value set here relates to the format that will be exported.