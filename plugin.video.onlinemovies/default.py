import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net as net
from metahandler import metahandlers

addon_id = 'plugin.video.onlinemovies'
selfAddon = xbmcaddon.Addon(id=addon_id)
metaget = metahandlers.MetaData(preparezip=False)
addon = Addon(addon_id, sys.argv)
ADDON2=xbmcaddon.Addon(id='plugin.video.onlinemovies')
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
metaset = selfAddon.getSetting('enable_meta')

def CATEGORIES():
        addDir2('Latest Cinema Releases','http://onlinemovies.pro/category/most-popular-new-movies/?filtre=date',1,icon,'',fanart)
        addDir2('Recently Added','http://onlinemovies.pro/category/genre/?filtre=date',1,icon,'',fanart)
        addDir2('Most Viewed','http://onlinemovies.pro/category/genre/?filtre=views',1,icon,'',fanart)
        addDir2('Highest Rated','http://onlinemovies.pro/category/genre/?filtre=rate',1,icon,'',fanart)
        addDir2('HD Movies','http://onlinemovies.pro/category/hd-movies/?filtre=random',1,icon,'',fanart) 
        addDir2('Christmas Movies','http://onlinemovies.pro/category/christmas-movies/',1,icon,'',fanart) 
        addDir2('Search','url',3,icon,'',fanart)
        xbmc.executebuiltin('Container.SetViewMode(50)')
               
def GETMOVIES(url,name):
        link = open_url(url)
        match=re.compile('<a href="(.+?)" title="(.+?)">').findall(link)
        print match
        for url,name in match:
                name2 = cleanHex(name)
                addDir(name2,url,100,'',len(match),isFolder=False)
        try:
                match=re.compile('"nextLink":"(.+?)"').findall(link)
                url= match[0]
                url = url.replace('\/','/')
                addDir('Next Page>>',url,1,artpath+'nextpage.png',len(match),isFolder=True)
        except: pass
        if metaset=='true':
                setView('movies', 'MAIN')
        else: xbmc.executebuiltin('Container.SetViewMode(50)')

def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Online Movies Pro')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://onlinemovies.pro/?s='+ search_entered
        link = open_url(url)
        GETMOVIES(url,name)

def PLAYLINK(name,url,iconimage):
    try:
        link = open_url(url)
        match=re.compile('src="http://videomega.tv/validatehash.php\?hashkey=(.+?)">').findall(link)
        if len(match)==0:
            match=re.compile("src=\'http://videomega.tv/validatehash.php\?hashkey=(.+?)\'>").findall(link)
        videomega_id_url = "http://videomega.tv/validatehash.php?hashkey="+ match[0]           
        link = open_url(videomega_id_url)
        match=re.compile('var ref="(.+?)";').findall(link)
        vididresolved = match[0]
        videomega_url = 'http://videomega.tv/iframe.php?ref='+vididresolved
    except:
        link = open_url(url)
        match=re.compile('ref=(.+?)\&width').findall(link)[0]
        print match
        videomega_url = 'http://videomega.tv/iframe.php?ref='+match
        print videomega_url
    link = open_url(videomega_url)
    url = re.compile('document.write.unescape."(.+?)"').findall(link)[0]
    url = urllib.unquote(url)
    stream_url = re.compile('file: "(.+?)"').findall(url)[0]
    stream_url = urllib.unquote_plus(stream_url)
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
        
def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev>(KHTML, like Gecko) Chrome/<Chrome Rev> Safari/<WebKit Rev>')
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
    if ADDON2.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON2.getSetting(viewType) )

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
elif mode==3: SEARCH()
elif mode==100: PLAYLINK(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

