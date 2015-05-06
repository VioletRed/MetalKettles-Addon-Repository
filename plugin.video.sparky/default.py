import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,json,base64

AddonID ='plugin.video.sparky'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
artpath = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID + '/resources/art/'))
  
def menu():
    addDir('All Channels','0',1,artpath+'all.PNG',fanart)
    addDir('Entertainment','1',1,artpath+'ent.PNG',fanart)
    addDir('Movies','2',1,artpath+'mov.PNG',fanart)
    addDir('Music','3',1,artpath+'mus.PNG',fanart)
    addDir('News','4',1,artpath+'news.PNG',fanart)
    addDir('Sports','5',1,artpath+'sport.PNG',fanart)
    addDir('Documentary','6',1,artpath+'doc.PNG',fanart)
    addDir('Kids Corner','7',1,artpath+'kids.PNG',fanart)
    addDir('Food','8',1,artpath+'food.PNG',fanart)
    addDir('Religious','9',1,artpath+'rel.PNG',fanart)
    addDir('USA Channels','10',1,artpath+'us.PNG',fanart)
    addDir('Others','11',1,artpath+'others.PNG',fanart)
    xbmc.executebuiltin('Container.SetViewMode(500)')
  
def MKSports(url):
    channelurl='http://mobile.desistreams.tv/DesiStreams/index2.php?tag=get_all_channel'
    response=Get_url(channelurl)
    channels=json.loads(response)
    data=channels['channel']
    for item in data:
        name=item['name']
        thumb=item['img']
        stream1=item['stream_url']
        stream2=item['stream_url2']
        stream3=item['stream_url3']
        cat=item['cat_id']
        thumb='http://mobile.desistreams.tv/'+thumb
        if url=='0':
            addLink(name+' - Stream 1',stream1,100,thumb,'')
            addLink(name+' - Stream 2',stream2,100,thumb,'')
            addLink(name+' - Stream 3',stream3,100,thumb,'')
        if cat==url:
            addLink(name+' - Stream 1',stream1,100,thumb,'')
            addLink(name+' - Stream 2',stream2,100,thumb,'')
            addLink(name+' - Stream 3',stream3,100,thumb,'')
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    xbmc.executebuiltin('Container.SetViewMode(500)')

def Get_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Apache-HttpClient/UNAVAILABLE (java 1.4)')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
def Play(name,url):  
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    xbmc.Player().play(url, liz, False)
    return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]    
        return param
           
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass
print "Mode: "+str(mode);print "URL: "+str(url);print "Name: "+str(name);print "IconImage: "+str(iconimage)

if mode==None or url==None or len(url)<1:menu()
elif mode==1:MKSports(url)
elif mode==100:Play(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
