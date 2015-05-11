import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,os,re,sys,urllib2
from resources.libs.common_addon import Addon

addon_id = 'plugin.video.highlights'
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.PNG'))

def INDEX():
        addDir(' ','http://89.45.201.242/dude/foot/dl.html',1,'http://89.45.201.242/dude/foot/website/dl.jpg','',fanart)
        addDir(' ','http://89.45.201.242/dude/foot/uefa.html',2,'http://89.45.201.242/dude/foot/website/uefa.jpg','',fanart)
        addDir(' ','http://89.45.201.242/dude/foot/euroqgrupe.html',2,'http://89.45.201.242/dude/foot/website/euroq.png','',fanart)
        xbmc.executebuiltin('Container.SetViewMode(500)')
        
def GETLEAGUES():
        url = 'http://89.45.201.242/dude/foot/dl.html'
        link = open_url(url)
        match = re.compile("<a href=\"(.+?)\"><img src='(.+?)' /></a></div>").findall(link)
        for url,thumb in match:
                url = 'http://89.45.201.242/dude/foot/'+url
                thumb = 'http://89.45.201.242/dude/foot/'+thumb
                addDir(' ',url,3,thumb,'',fanart)
        xbmc.executebuiltin('Container.SetViewMode(500)')

def GETWEEKS(url):
        link = open_url(url)
        match = re.compile("<a href=\"(.+?)\"><img src='(.+?)' /></a>").findall(link)
        for url,thumb in match:
                url = 'http://89.45.201.242/dude/foot/'+url
                thumb = 'http://89.45.201.242/dude/foot/'+thumb
                thumb = thumb.replace(' ','%20')
                addDir(' ',url,4,thumb,'',fanart)
        xbmc.executebuiltin('Container.SetViewMode(500)')

def GETGAMES(url):
        link = open_url(url)
        match = re.compile("<a href=\"(.+?)\"><img src='(.+?)' /></a>").findall(link)
        for url,thumb in match:
                thumb = 'http://89.45.201.242/dude/foot'+thumb
                thumb = thumb.replace(' ','%20').replace('..','')
                addLink(' ',url,2,thumb,'',fanart)
        xbmc.executebuiltin('Container.SetViewMode(500)')











def PLAYLINK(name,url):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player ().play(url, liz, False)
        return ok

def open_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Linux; U; Android 4.1.2; en-gb; GT-I9100 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

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
               
def addDir(name,url,mode,iconimage,description,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,description,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
 
 
params=get_params(); url=None; name=None; mode=None; site=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
 
print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
 
if mode==None or url==None or len(url)<1: GETLEAGUES()
elif mode==2: PLAYLINK(name,url)
elif mode==1: GETLEAGUES(url)
elif mode==3: GETWEEKS(url)
elif mode==4: GETGAMES(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
