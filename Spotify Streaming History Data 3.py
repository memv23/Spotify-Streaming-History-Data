import csv
from itertools import zip_longest
import json

with open('finaljason.json','r',encoding='utf8') as fj:
    datafj = json.load(fj)

print(len(datafj))
print(datafj[0],'\n',datafj[1])

xid=[]
xdate=[]
xartist=[]
xsong=[]
xalbum=[]
xreldate=[]
xpop=[]
xdan=[]
xen=[]
xkey=[]
xloud=[]
xmod=[]
xspe=[]
xaco=[]
xinst=[]
xlive=[]
xval=[]
xtem=[]
xtime=[]

for i in datafj:
    try:
        xid.append(i['id'])
        xdate.append(i['endTime'])
        xartist.append(i['info']['Artist'])
        xsong.append(i['info']['Song'])
        xalbum.append(i['info']['Album'])
        xreldate.append(i['info']['Release Date'])
        xpop.append(i['info']['Popularity'])
        xdan.append(i['features']['Danceability'])
        xen.append(i['features']['Energy'])
        xkey.append(i['features']['Key'])
        xloud.append(i['features']['Loudness'])
        xmod.append(i['features']['Mode'])
        xspe.append(i['features']['Speechiness'])
        xaco.append(i['features']['Acousticness'])
        xinst.append(i['features']['Instrumentalness'])
        xlive.append(i['features']['Liveness'])
        xval.append(i['features']['Valence'])
        xtem.append(i['features']['Tempo'])
        xtime.append(i['features']['Time Signature'])
    except KeyError:
        print('Failure')
        pass

print(len(xid))
print(len(xtime))

x = [xid,xdate,xartist,xsong,xalbum,xreldate,xpop,xdan,xen,xkey,xloud,xmod,xspe,xaco,xinst,xlive,xval,xtem,xtime]
data_x = zip_longest(*x,fillvalue='')

with open('songdatafile.csv','w',encoding='utf8',newline='') as fcx:
    wr = csv.writer(fcx)
    wr.writerow(('ID','Date', 'Artist', 'Song', 'Album', 'Release Date', 'Popularity', 'Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Valence', 'Tempo', 'Time Signature'))
    wr.writerows(data_x)
fcx.close()
