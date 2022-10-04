import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import csv

#Authentication
client_credentials_manager = SpotifyClientCredentials(client_id='4b4cb4f8525543959104a2168e29e1c9', client_secret='8ea4d3b6032c4a35ba22999240e6859d')
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#li=["https://open.spotify.com/playlist/50U5BOS6UYRse9xXMobRlR?si=1KC5juHzRbiQFxfwVEJE2A&utm_source=whatsapp","https://open.spotify.com/playlist/2U5naKBJ5DN3oOPbuRiTem","https://open.spotify.com/playlist/6ygDXoR74Bq477kqHwMNrH","https://open.spotify.com/playlist/37i9dQZF1DWZNJXX2UeBij"]
li=["https://open.spotify.com/playlist/4jlbTgG7gqClTD2MjpUDqI","https://open.spotify.com/playlist/37i9dQZF1DX0XUfTFmNBRM","https://open.spotify.com/playlist/37i9dQZF1DX14CbVHtvHRB","https://open.spotify.com/playlist/37i9dQZF1DXd8cOUiye1o2","https://open.spotify.com/playlist/37i9dQZF1DXdpQPPZq3F7n","https://open.spotify.com/playlist/37i9dQZF1DWVq1SXCH6uFn","https://open.spotify.com/playlist/37i9dQZF1DX3txqabhtJQF","https://open.spotify.com/playlist/37i9dQZF1DX8xfQRRX1PDm","https://open.spotify.com/playlist/37i9dQZF1DXa2huSXaKVkW","https://open.spotify.com/playlist/37i9dQZF1DX3NU3NvyoJUz","https://open.spotify.com/playlist/37i9dQZF1DWTUfv2yzHEe7","https://open.spotify.com/playlist/37i9dQZF1DX57WIZsVQSIn","https://open.spotify.com/playlist/37i9dQZF1DX5rOEFf3Iycd","https://open.spotify.com/playlist/37i9dQZF1DWZ2bQuX4pBHH","https://open.spotify.com/playlist/37i9dQZF1DX6q19gm5UQXx","https://open.spotify.com/playlist/37i9dQZF1DX33pLIqKke0L","https://open.spotify.com/playlist/37i9dQZF1DXd1aNMk1xQMv","https://open.spotify.com/playlist/37i9dQZF1DWWiO1wG95aPP","https://open.spotify.com/playlist/37i9dQZF1DWVt4lNGonufn","https://open.spotify.com/playlist/37i9dQZF1DX82F21A3zQhD","https://open.spotify.com/playlist/37i9dQZF1DXaQQFGfFwcj0","https://open.spotify.com/playlist/37i9dQZF1DWVClvVUI87z8","https://open.spotify.com/playlist/37i9dQZF1DWVIEXqkZKKXl","https://open.spotify.com/playlist/37i9dQZF1DX5rZPt6uqhWK"]
track_uris=[]
for k in li:
    link = k
    playlist_URI = link.split("/")[-1].split("?")[0]
#    track_uris += [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]
    r=sp.playlist_tracks(playlist_URI)['total']
    if r>100:
        of=0
        for i in range(0,r,100):
            track_uris += [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI,offset=of)["items"]]
            of+=100
    else:
        track_uris += [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]


first=sp.audio_features(track_uris[0])[0]
first['name']=sp.track(first['id'])['name']
head=first.keys()
"""
lis=[]
for i in track_uris:
    d=sp.audio_features(i)[0]
    d['name']=sp.track(d['id'])['name']
    lis.append(d)

with open('database.csv','w',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f,fieldnames=head)
    writer.writeheader()
    writer.writerows(lis)
"""
lis=[]
for i in track_uris:
    try:
        d=sp.audio_features(i)[0]
        d['name']=sp.track(d['id'])['name']
        lis.append(d)
        print('*')
    except:
        pass
with open('database.csv','a',newline='',encoding='utf-8') as f:
    writer=csv.DictWriter(f)
    writer.writeheader()
    writer.writerows(lis)
