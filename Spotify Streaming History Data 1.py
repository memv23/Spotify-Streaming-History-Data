import spotipy
import spotipy.util as util
import json
import re
from time import sleep

token = util.prompt_for_user_token(username="spotify:user:REDACTED",scope="ugc-image-upload playlist-read-collaborative playlist-modify-private playlist-modify-public playlist-read-private user-modify-playback-state user-read-currently-playing user-read-playback-state user-read-private user-read-email user-library-modify user-library-read user-follow-modify user-follow-read user-read-recently-played user-top-read streaming app-remote-control",
    client_id="REDACTED",
    client_secret="REDACTED",
    redirect_uri="https://localhost:8888/callback/")

##token = ''
print(token)

sp = spotipy.Spotify(auth=token)

with open('StreamingHistory.json','r',encoding='utf8') as f:
    data = json.load(f)

endTime = []
artistName = []
trackName = []
msPlayed = []
todel = []

for i in range(len(data)):
    a = data[i]
    if not (((re.search(r"Unknown",a['artistName'])) or (re.search(r"Unknown",a['trackName'])) or (a['msPlayed']<10000))):
        endTime.append(a['endTime'])
        artistName.append(a['artistName'])
        trackName.append(a['trackName'])
        msPlayed.append(a['msPlayed'])
    else:
        todel.append(i)

cnt = 0
for y in todel:
    del data[y-cnt]
    cnt+=1

artist_track = []
for i in data:
    a = i['artistName']+" "+i['trackName']
    artist_track.append(a)

artist_track = dict.fromkeys(artist_track)
print(len(artist_track))

cntr = 0
for art_track in artist_track:
    if ((cntr%50)==0):
        print(cntr)
    cntr+=1
    a = sp.search(art_track,limit=1)
    sleep(0.012)
    if not (a['tracks']['items'] == []):
        b = a['tracks']['items'][0]
        c = {'id':b['id'],'album':b['album']['name'],'popularity':b['popularity'],'release_date':b['album']['release_date']}
        artist_track[art_track] = c

for j in data:
    try:
        art_tr = j['artistName']+" "+j['trackName']
        q = artist_track[art_tr]
        j['info'] = {'Artist':j['artistName'],'Song':j['trackName'],'Album':q['album'],'Release Date':q['release_date'],'Popularity':q['popularity']}
        j['features'] = {}
        j['id'] = q['id']
    except TypeError:
        pass

with open('prelimdata.json','w',encoding='utf8') as f2:
    json.dump(data,f2,indent=4)
