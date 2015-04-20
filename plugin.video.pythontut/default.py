import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os

addon_id        = 'plugin.video.pythontut'
BaseURL         = 'https://www.thenewboston.com/videos.php?cat=36'
url2            = 'https://www.thenewboston.com/'
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

def CATEGORIES():
        req = urllib2.Request(BaseURL)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class=".+?">(.+?)</a>').findall(link)
        for url,name in match:
                url = url2+url
                num = name[0]
                if num.isdigit():
                        addDir(name,url,2,icon)    

def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        links=re.compile('src="//www.youtube.com/embed/(.+?)"').findall(link)
        for video_id in links:
                playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
                xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(playback_url)

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
 
def addDir(name,url,mode,iconimage,isFolder=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
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
 
if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: GETMOVIES(url)
elif mode==2: VIDEOLINKS(url,name)
elif mode==200: PLAYLINK(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
