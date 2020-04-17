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

with open('prelimdata.json','r',encoding='utf8') as af:
    dataf = json.load(af)

print(len(dataf))

unique = []
cnt = 0
for i in dataf:
    i.pop('artistName')
    i.pop('trackName')
    i.pop('msPlayed')
    try:
        rdate = i['info']['Release Date']
        if (re.search(r'19[0-9][0-9]$|20[0-2][0-9]$',rdate)):
            rdate = rdate[-4:]
        elif (re.match(r'19[0-9][0-9]|20[0-2][0-9]',rdate)):
            rdate = rdate[0:4]
        else:
            rdate = rdate
            print('Failed  -  '+str(rdate))
        i['info']['Release Date'] = rdate
        unique.append(i['id'])
    except KeyError:
        print('Failure 1')
        pass

print('Total: '+str(len(unique)))
uniquedict = dict.fromkeys(unique)
print('Unique: '+str(len(uniquedict)))

for keyid in uniquedict:
    try:
        if ((cnt%50)==0):
            print(cnt)
        ft = sp.audio_features(keyid)
        uniquedict[keyid] = {'Danceability':ft[0]['danceability'],'Energy':ft[0]['energy'],'Key':ft[0]['key'],'Loudness':ft[0]['loudness'],'Mode':ft[0]['mode'],'Speechiness':ft[0]['speechiness'],'Acousticness':ft[0]['acousticness'],'Instrumentalness':ft[0]['instrumentalness'],'Liveness':ft[0]['liveness'],'Valence':ft[0]['valence'],'Tempo':ft[0]['tempo'],'Time Signature':ft[0]['time_signature']}
        sleep(0.012)
        cnt+=1
    except KeyError:
        print('Failure 2')
        pass

for j in dataf:
    try:
        keyid2 = j['id']
        j['features'] = uniquedict[keyid2]
    except KeyError:
        print('Failure 3')
        pass

with open('finaljason.json','w',encoding='utf8') as f3:
    json.dump(dataf,f3,indent=4)
