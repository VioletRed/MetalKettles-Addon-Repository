import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os,random
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net as net

addon_id = 'plugin.video.erotik'
selfAddon = xbmcaddon.Addon(id=addon_id)
metaget = metahandlers.MetaData(preparezip=False)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.PNG'))
base = 'http://www.ero-tik.com/index.html'
        
def CATEGORIES():
        req = urllib2.Request(base)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        addDir2('[COLOR gold]New Videos[/COLOR]',base,1,icon,'',fanart)
        match=re.compile('<li class=""><a href="(.+?)" class="">(.+?)</a></li>').findall(link)
        mk = 1
        for url, cat in match:
                if mk < 19:
                        addDir2(cat,url,2,icon,'',fanart)
                mk=mk+1
     
def GETMOVIES(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class=".+?"><span class=".+?"><img src="(.+?)" alt="(.+?)" width=".+?"><span class=".+?"></span></span></a>').findall(link)
        for url,img,name in match:
                addLink(name,url,100,img,fanart,'')
        xbmc.executebuiltin('Container.SetViewMode(500)')
                
def GETMOVIESCATS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" class=".+?"><span class=".+?"><img src="(.+?)" alt="(.+?)" width=".+?"><span class=".+?"></span></span></a>').findall(link)
        for url,img,name in match:
                addLink(name,url,100,img,fanart,'')
        try:
                match=re.compile('<a href="(.+?)">&raquo;</a>').findall(link)[0]
                addDir2('Next Page >>',match,2,icon,'',fanart)
        except:pass
        xbmc.executebuiltin('Container.SetViewMode(500)')

def PLAYLINK(name,url):
        req = urllib2.Request(url)
        print 'here'
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('src="http://videomega.tv/validatehash.php\?hashkey=(.+?)"').findall(link)[0]
        videomega_id_url = "http://videomega.tv/validatehash.php?hashkey="+ match
        req = urllib2.Request(videomega_id_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('var ref="(.+?)";').findall(link)
        vididresolved = match[0]
        videomega_url = 'http://videomega.tv/iframe.php?ref='+vididresolved
        req = urllib2.Request(videomega_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        url = re.compile('document.write.unescape."(.+?)"').findall(link)[0]
        url = urllib.unquote(url)
        stream_url = re.compile('file: "(.+?)"').findall(url)[0]
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player ().play(stream_url, liz, False)

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

def addDir2(name,url,mode,iconimage,description,fanart):
        xbmc.executebuiltin('Container.SetViewMode(50)')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
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
print params

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: GETMOVIES(url,name)
elif mode==2: GETMOVIESCATS(url,name)
elif mode==100: PLAYLINK(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

