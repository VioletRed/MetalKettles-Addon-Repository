import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os,random,urlparse
from t0mm0.common.addon import Addon
from metahandler import metahandlers

addon_id = 'plugin.video.movieshd'
selfAddon = xbmcaddon.Addon(id=addon_id)
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
metaget = metahandlers.MetaData(preparezip=False)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
artpath = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
metaset = selfAddon.getSetting('enable_meta')

def CATEGORIES():
        addDir2('Featured','http://movieshd.co/watch-online/category/featured?filtre=date',1,icon,'',fanart)
        addDir2('Recently Added','http://movieshd.co/?filtre=date&cat=0',1,icon,'',fanart)
        addDir2('Most Viewed','http://movieshd.co/?filtre=views&cat=0',1,icon,'',fanart)
        addDir2('Highest Rated','http://movieshd.co/?filtre=rate&cat=0',1,icon,'',fanart)
        addDir2('Bollywood','http://movieshd.co/watch-online/category/bollywood',1,icon,'',fanart) 
        addDir2('Disneys Magic','http://movieshd.co/watch-online/category/disneys?display=tube&filtre=date',1,icon,'',fanart) 
        addDir2('Genres','url',2,icon,'',fanart)
        addDir2('Search','url',3,icon,'',fanart)
        addLink('','','',icon,fanart)
        addLink('[COLOR blue]Twitter[/COLOR] Feed','url',4,icon,fanart)
        xbmc.executebuiltin('Container.SetViewMode(50)')
               
def TWITTER():
        text = ''
        twit = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?560774256146272257'
        link = open_url(twit)
        link = link.replace('/n','')
        link = link.decode('utf-8').encode('utf-8').replace('&#39;','\'').replace('&#10;',' - ').replace('&#x2026;','')
        match=re.compile("<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)[1:]
        for status, dte in match:
            dte = dte[:-15]
            dte = '[COLOR blue][B]'+dte+'[/B][/COLOR]'
            text = text+dte+'\n'+status+'\n'+'\n'
        showText('@movieshd_co', text)

def GETMOVIES(url,name):
        link = open_url(url)
        match=re.compile('href="(.+?)" title="(.+?)">').findall(link)
        items = len(match)
        for url,name in match:
                name2 = cleanHex(name)
                addDir(name2,url,100,'',len(match))
        try:
                match=re.compile('"nextLink":"(.+?)"').findall(link)
                url= match[0]
                url = url.replace('\/','/')
                addDir('Next Page>>',url,1,artpath+'nextpage.png',items,isFolder=True)
        except: pass
        if metaset=='true':
                setView('movies', 'MAIN')
        else: xbmc.executebuiltin('Container.SetViewMode(50)')
        
def GENRES(url):
        addDir2('Action','http://movieshd.co/watch-online/category/action/',1,artpath+'action.png','',fanart)
        addDir2('Adventure','http://movieshd.co/watch-online/category/adventure/',1,artpath+'adventure.png','',fanart)
        addDir2('Animation','http://movieshd.co/watch-online/category/animation/',1,artpath+'animation.png','',fanart)
        addDir2('Biography','http://movieshd.co/watch-online/category/biography/',1,artpath+'biography.png','',fanart)
        addDir2('Comedy','http://movieshd.co/watch-online/category/comedy/',1,artpath+'comedy.png','',fanart)
        addDir2('Crime','http://movieshd.co/watch-online/category/crime/',1,artpath+'crime.png','',fanart)
        addDir2('Drama','http://movieshd.co/watch-online/category/drama/',1,artpath+'drama.png','',fanart)
        addDir2('Family','http://movieshd.co/watch-online/category/family/',1,artpath+'family.png','',fanart)
        addDir2('Fantasy','http://movieshd.co/watch-online/category/fantasy/',1,artpath+'fantasy.png','',fanart)
        addDir2('History','http://movieshd.co/watch-online/category/history/',1,artpath+'history.png','',fanart)
        addDir2('Horror','http://movieshd.co/watch-online/category/horror/',1,artpath+'horror.png','',fanart)
        addDir2('Music','http://movieshd.co/watch-online/category/music/',1,artpath+'musical.png','',fanart)
        addDir2('Mystery','http://movieshd.co/watch-online/category/mystery/',1,artpath+'mystery.png','',fanart)
        addDir2('Romance','http://movieshd.co/watch-online/category/romance/',1,artpath+'romance.png','',fanart)
        addDir2('Sci-Fi','http://movieshd.co/watch-online/category/sci-fi/',1,artpath+'sci-fi.png','',fanart)
        addDir2('Sports','http://movieshd.co/watch-online/category/sports/',1,artpath+'sport.png','',fanart)
        addDir2('Thriller','http://movieshd.co/watch-online/category/thriller/',1,artpath+'thriller.png','',fanart)
        addDir2('War','http://movieshd.co/watch-online/category/war/',1,artpath+'war.png','',fanart)
        addDir2('Western','http://movieshd.co/watch-online/category/western/',1,artpath+'western.png','',fanart)
        setView('movies', 'MAIN')

def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Movies HD')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://movieshd.co/?s='+ search_entered
        link = open_url(url)
        GETMOVIES(url,name)

def PLAYLINK(name,url,iconimage):
    
        link = open_url(url)
        match=re.compile('hashkey=(.+?)">').findall(link)
        if len(match) == 0:
                match=re.compile("hashkey=(.+?)'>").findall(link)
        if (len(match) > 0):
                hashurl="http://videomega.tv/validatehash.php?hashkey="+ match[0]
                req = urllib2.Request(hashurl)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                req.add_header('Referer', url)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('var ref="(.+?)"').findall(link)[0]
                print match
                videomega_url = 'http://videomega.tv/?ref='+match 
        else:
                match=re.compile("javascript'\>ref='(.+?)'").findall(link)[0]
                videomega_url = "http://videomega.tv/?ref=" + match
                
##RESOLVE##     
        url = 'http://videomega.tv/cdn.php?ref=%s' % match
        referer = videomega_url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        req.add_header('Referer', referer)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()        
        stream_url = re.compile('<source src="(.+?)" type="video/mp4"/>').findall(link)[0]
        stream_url = stream_url + '|User-Agent: Mozilla/5.0 (Linux; U; Android 4.1.2; en-gb; GT-I9100 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
##RESOLVE##
        
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        playlist.add(stream_url,listitem)
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
            

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
    
def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass
        
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
elif mode==2: GENRES(url)
elif mode==3: SEARCH()
elif mode==4: TWITTER()
elif mode==100: PLAYLINK(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

