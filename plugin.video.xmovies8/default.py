import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os,random,urlparse
from t0mm0.common.addon import Addon
from metahandler import metahandlers

addon_id = 'plugin.video.xmovies8'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
metaget = metahandlers.MetaData(preparezip=False)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
metaset = selfAddon.getSetting('enable_meta')

def CATEGORIES():
        addDir2('Cinema Movies','http://xmovies8.co/tag/hotnew/',1,icon,'',fanart)
        addDir2('New Movies','http://xmovies8.co/author/T9611412/',1,icon,'',fanart)
        addDir2('Movies By Year','http://xmovies8.co/',2,icon,'',fanart)
        addDir2('Movies By Genre','http://xmovies8.co/movie-quality/hd/',4,icon,'',fanart)
        addDir2('Movies By Quality','http://xmovies8.co/',5,icon,'',fanart)
        addDir2('Search','http://xmovies8.co/movie-quality/hd/',3,icon,'',fanart)     
        xbmc.executebuiltin('Container.SetViewMode(50)')
        
def GETYEARS(url):
        link = open_url(url)
        link=link.replace('\n','').replace('  ','')
        match=re.compile('href="(.+?)">(.+?)</a></li>').findall(link)
        addDir2('2015','http://xmovies8.co/category/2015/',1,icon,'',fanart)
        for url,name in match:              
                if 'category' in url:addDir2(name,url,1,icon,'',fanart)
        xbmc.executebuiltin('Container.SetViewMode(50)')
                
def GETGENRES(url):                  
        link = open_url(url)
        link=link.replace('\n','').replace('  ','')
        match=re.compile('<li class="cat-item cat-item-.+?"><a href="(.+?)" >(.+?)</a>').findall(link)
        for url,name in match:
                if 'game-show' in name:name = 'Game Show'
                if 'genre' in url:addDir2(name,url,1,icon,'',fanart)
        xbmc.executebuiltin('Container.SetViewMode(50)')

def GETQUALITY(url): 
        addDir2('CAM','http://xmovies8.co/movie-quality/cam/',1,icon,'',fanart)
        addDir2('DVD RIP','http://xmovies8.co/movie-quality/dvdrip/',1,icon,'',fanart)
        addDir2('HD','http://xmovies8.co/movie-quality/hd/',1,icon,'',fanart)
        xbmc.executebuiltin('Container.SetViewMode(50)')

def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Xmovies8')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://xmovies8.co/?s='+ search_entered
        link = open_url(url)
        match=re.compile('<h2><a href="(.+?)">(.+?)</a></h2>').findall(link)
        for url,name in match:
             addDir(name,url,100,'',len(match))
        if metaset=='true':
                setView('movies', 'MAIN')
        else: xbmc.executebuiltin('Container.SetViewMode(50)')
     
def GETMOVIES(url,name):
        link = open_url(url)
        link=link.replace('\n','').replace('  ','')
        match=re.compile('<a class="thumbnail darken video" title="(.+?)" href="(.+?)">',re.DOTALL).findall(link)
        if len(match)>0:
                items = len(match)
                for name,url in match:
                        name2 = cleanHex(name)
                        if not 'Season' in name2:
                                if not 'SEASON' in name2:
                                        addDir(name2,url,100,'',len(match))
        if len(match)<1:
                match=re.compile('<a class="thumbnail darken video" href="(.+?)" title="(.+?)">',re.DOTALL).findall(link)
                items = len(match)
                for url,name in match:
                        name2 = cleanHex(name)
                        if not 'Season' in name2:
                                if not 'SEASON' in name2:
                                        addDir(name2,url,100,'',len(match))
        try:
                match=re.compile('link rel="next" href="(.+?)"').findall(link)
                url= match[0]
                addDir2('Next Page>>',url,1,icon,'',fanart)
        except: pass
        if metaset=='true':
                setView('movies', 'MAIN')
        else: xbmc.executebuiltin('Container.SetViewMode(50)')

def PLAYLINK(name,url,iconimage):
        link = open_url(url)
        match=re.compile('<a target="_blank" rel="nofollow" href="(.+?)">.+?mp4</a>').findall(link)
        if len(match)>0:
                match = match[-1]
        else:
                match=re.compile('src="http://videomega.tv/cdn.php\?ref=(.+?)\&width=700\&height=430"').findall(link)
                if len(match)<1:
                        match=re.compile('src="http://videomega.tv/iframe.php\?ref=(.+?)"').findall(link)
                videomega_url = "http://videomega.tv/?ref=" + match[0]
                
##RESOLVE##     
                url = urlparse.urlparse(videomega_url).query
                url = urlparse.parse_qs(url)['ref'][0]
                url = 'http://videomega.tv/cdn.php?ref=%s' % url
                referer = videomega_url
                req = urllib2.Request(url,None)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                req.add_header('Referer', referer)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()        
                match = re.compile('<source src="(.+?)" type="video/mp4"/>').findall(link)[0]      
##RESOLVE##
        print match       
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(match,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)

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

def addDir(name,url,mode,iconimage,itemcount,isFolder=False):
        if metaset=='true':
            splitName=name.partition('(')
            simplename=""
            simpleyear=""
            if len(splitName)>0:
                simplename=splitName[0]
                simpleyear=splitName[2].partition(')')
            if len(simpleyear)>0:
                simpleyear=simpleyear[0]
            meta = metaget.get_meta('movie', simplename ,simpleyear)
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels= meta )
            contextMenuItems = []
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            liz.addContextMenuItems(contextMenuItems, replaceItems=True)
            if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
            else: liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
            return ok
        else:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
            return ok
        
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
                
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if selfAddon.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting(viewType) )

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
print params

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: GETMOVIES(url,name)
elif mode==2: GETYEARS(url)
elif mode==3: SEARCH()
elif mode==4: GETGENRES(url)
elif mode==5: GETQUALITY(url)
elif mode==100: PLAYLINK(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

