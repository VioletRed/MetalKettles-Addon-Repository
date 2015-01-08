import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os
from resources.libs.common_addon import Addon

addon_id = 'plugin.audio.televisiontunes'
addon = Addon('plugin.audio.televisiontunes', sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ad = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'ad.png')) 
afb = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'afb.png'))
console = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'console.png'))
tv = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'tv.png'))
football = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'football.png'))

def index():
        addDir('Television Tunes','http://www.televisiontunes.com/',1,tv,'',fanart)
        addDir('Game Theme Songs','http://gamethemesongs.com/',1,console,'',fanart)
        addDir('TV Ad Songs','http://tvadsongs.com/',1,ad,'',fanart)
        addDir('Soccer Songs','http://fcsongs.com/',1,football,'',fanart)
        addDir('Football Music','http://footballfightmusic.com/',4,afb,'',fanart)

def AZ(url):
        if 'television' in url : img = tv
        if 'game' in url : img = console
        if 'tvad' in url : img = ad
        if 'fight' in url : img = afb
        if 'fc' in url : img = football
        base = url
        link = open_url(url)
        azlist=re.compile('<li><a href="(.+?)" >(.+?)</a></li>').findall(link)
        addDir('Search',url,3,img,'',fanart)
        for url,name in azlist:
                addDir(name,base + url,2,img,'',fanart)
               
def GETTHEMES(url,name):
        if 'television' in url : img = tv
        if 'game' in url : img = console
        if 'tvad' in url : img = ad
        if 'fight' in url : img = afb
        if 'fc' in url : img = football
        link = open_url(url)
        match=re.compile('<a href="(.+?)">(.+?)</a></td></tr><tr><td>').findall(link)
        for url,name in match:
                addDirPlayable(name,url,100,img,'',fanart)
                
def afblist(url):
        base = url
        link = open_url(url)
        catlist=re.compile('<a href="(.+?)"><img src="(.+?)" alt="(.+?)" width="150" height="100" border="0" /></a></td>').findall(link)
        for url,thumb,name in catlist:
                thumb2 = base + thumb
                addDir(name,url,2,thumb2,'',fanart)
        
def getafbthemes(url,name):
        link = open_url(url)
        response.close()
        match=re.compile('<a href="(.+?)">(.+?)</a></td></tr>').findall(link)
        for url,name in match:
                addDirPlayable(name,url,100,icon,'',fanart)
        
def SEARCH(url):
    base = url
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search TelevistionTunes')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')# sometimes you need to replace spaces with + or %20#
    if len(search_entered)>1:
        url = base + 'search.php?searWords=' + search_entered + '&Send=Search'
        print url
        link = open_url(url)
        match=re.compile('&nbsp;<a href="(.+?)">(.+?)</a>').findall(link)
        for url,name in match:
                addDirPlayable(name,url,100,icon,'',fanart)
                
    
def TUNELINKS(url,name):
        base ='http://' + url.split('/',3)[2]
        link = open_url(url)
        tune=re.compile('mp3: "(.+?)"').findall(link)
        for url in tune:
                fulllink = base + url
                nospace = str(fulllink).replace(' ','%20')
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        try:
                xbmc.Player ().play(nospace, liz, False)
                return ok
        except:
                pass
 
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

def open_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link
               
def addDir(name,url,mode,iconimage,description,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDirPlayable(name,url,mode,iconimage,description,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
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
 
if mode==None or url==None or len(url)<1: index()
elif mode==1: AZ(url)
elif mode==2: GETTHEMES(url,name)
elif mode==3: SEARCH(url)
elif mode==4: afblist(url)
elif mode==100: TUNELINKS(url,name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
