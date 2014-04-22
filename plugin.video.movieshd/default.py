import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from metahandler import metahandlers

addon_id = 'plugin.video.movieshd'
selfAddon = xbmcaddon.Addon(id=addon_id)
metaget = metahandlers.MetaData(preparezip=False)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.PNG'))
artpath = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
xbmc.executebuiltin('Container.SetViewMode(500)')

def CATEGORIES():
        xbmc.executebuiltin('Container.SetViewMode(500)')
        addDir2('Recently Added','http://movieshd.eu/?filtre=date&cat=0',1,artpath+'movies.png','',fanart)
        addDir2('Most Viewed','http://movieshd.eu/?filtre=views&cat=0',1,artpath+'movies.png','',fanart)
        addDir2('Highest Rated','http://movieshd.eu/?filtre=rate&cat=0',1,artpath+'movies.png','',fanart)
        addDir2('Genres','url',2,artpath+'genres.png','',fanart)
        addDir2('Search','url',3,artpath+'search.png','',fanart)
        xbmc.executebuiltin('Container.SetViewMode(500)')

def GETMOVIES(url,name):
        xbmc.executebuiltin('Container.SetViewMode(500)')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #match=re.compile('<div class="cover"><a href="(.+?)" title="(.+?)"><img src="(.+?)" alt').findall(link)
        match=re.compile('<a href="(.+?)" title="(.+?)">').findall(link)
        for url,name in match:
                name2 = name.decode("ascii","ignore").replace('&#8217;','').replace('&amp;','')
                addDir(name2,url,100,'',len(match),isFolder=False)
        match=re.compile('<a class="next page-numbers" href="(.+?)">Next videos &raquo;</a>').findall(link)
        print match
        if len(match)>0:
                addDir('Next Page>>',match[0],1,artpath+'nextpage.png',len(match),isFolder=True)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmc.executebuiltin('Container.SetViewMode(500)')

def GENRES(url):
        xbmc.executebuiltin('Container.SetViewMode(500)')
        addDir2('Action','http://movieshd.eu/watch-online/category/action/',1,artpath+'action.png','',fanart)
        addDir2('Adventure','http://movieshd.eu/watch-online/category/adventure/',1,artpath+'adventure.png','',fanart)
        addDir2('Animation','http://movieshd.eu/watch-online/category/animation/',1,artpath+'animation.png','',fanart)
        addDir2('Biography','http://movieshd.eu/watch-online/category/biography/',1,artpath+'biography.png','',fanart)
        addDir2('Comedy','http://movieshd.eu/watch-online/category/comedy/',1,artpath+'comedy.png','',fanart)
        addDir2('Crime','http://movieshd.eu/watch-online/category/crime/',1,artpath+'crime.png','',fanart)
        addDir2('Drama','http://movieshd.eu/watch-online/category/drama/',1,artpath+'drama.png','',fanart)
        addDir2('Family','http://movieshd.eu/watch-online/category/family/',1,artpath+'family.png','',fanart)
        addDir2('Fantasy','http://movieshd.eu/watch-online/category/fantasy/',1,artpath+'fantasy.png','',fanart)
        addDir2('History','http://movieshd.eu/watch-online/category/history/',1,artpath+'history.png','',fanart)
        addDir2('Horror','http://movieshd.eu/watch-online/category/horror/',1,artpath+'horror.png','',fanart)
        addDir2('Music','http://movieshd.eu/watch-online/category/music/',1,artpath+'musical.png','',fanart)
        addDir2('Mystery','http://movieshd.eu/watch-online/category/mystery/',1,artpath+'mystery.png','',fanart)
        addDir2('Romance','http://movieshd.eu/watch-online/category/romance/',1,artpath+'romance.png','',fanart)
        addDir2('Sci-Fi','http://movieshd.eu/watch-online/category/sci-fi/',1,artpath+'sci-fi.png','',fanart)
        addDir2('Sports','http://movieshd.eu/watch-online/category/sports/',1,artpath+'sport.png','',fanart)
        addDir2('Thriller','http://movieshd.eu/watch-online/category/thriller/',1,artpath+'thriller.png','',fanart)
        addDir2('War','http://movieshd.eu/watch-online/category/war/',1,artpath+'war.png','',fanart)
        addDir2('Western','http://movieshd.eu/watch-online/category/western/',1,artpath+'western.png','',fanart)
        xbmc.executebuiltin('Container.SetViewMode(500)')

def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Movies HD')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://movieshd.eu/?s='+ search_entered
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        GETMOVIES(url,name)
        xbmc.executebuiltin('Container.SetViewMode(500)')


def PLAYLINK(name,url):
        # Request MoviesHD page
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        # Find videomega reference and request video page from there.
        match=re.compile("'text/javascript'>ref='(.+?)';width.*iframe").findall(link)
        if (len(match) < 1):
            return
        videomega_url = "http://videomega.tv/iframe.php?ref=" + match[0]
        req = urllib2.Request(videomega_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        # Finally, find the actual filename
        match=re.compile("document.write.unescape.\"(.+?)\"").findall(link)
        if (len(match) < 1):
            return
        encoded=match[0]
        link = urllib.unquote(encoded)
        match=re.compile("file: \"(.+?)\",flash").findall(link)
        if (len(match) < 1):
            return
        stream_url = match[0]
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
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
        xbmc.executebuiltin('Container.SetViewMode(500)')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        xbmc.executebuiltin('Container.SetViewMode(500)')
        return ok


def addDir(name,url,mode,iconimage,itemcount,isFolder=True):
        xbmc.executebuiltin('Container.SetViewMode(500)')
        splitName=name.partition('(')
        simplename=""
        simpleyear=""
        if len(splitName)>0:
            simplename=splitName[0]
            simpleyear=splitName[2].partition(')')
            if len(simpleyear)>0:
                simpleyear=simpleyear[0]
        meta = metaget.get_meta('movie', simplename ,simpleyear)
        print meta
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
        xbmc.executebuiltin('Container.SetViewMode(500)')
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
elif mode==2: GENRES(url)
elif mode==3: SEARCH()
elif mode==100: PLAYLINK(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

