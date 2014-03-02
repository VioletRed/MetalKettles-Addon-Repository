import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil
from resources.libs.common_addon import Addon

addon_id = 'plugin.audio.housemixes'
addon = Addon('plugin.audio.housemixes', sys.argv)
baseurl = 'http://www.house-mixes.com/mixes'
baseurl2 = 'http://www.house-mixes.com'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
genres = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'genres.txt'))

def Index():
         addDir('Featured Mixes','http://www.house-mixes.com/mixes/featured/1/latest',2,icon,'',fanart)
         addDir('Trending Mixes','http://www.house-mixes.com/mixes/trending',2,icon,'',fanart)
         addDir('Popular Mixes','http://www.house-mixes.com/mixes/popular',2,icon,'',fanart)
         addDir('Latest Mixes','http://www.house-mixes.com/mixes',2,icon,'',fanart)
         addDir('Mixes by Genre','url',1,icon,'',fanart)
         addDir('Trending Tracks','http://www.house-mixes.com/tracks/trending',2,icon,'',fanart)
         addDir('Popular Tracks','http://www.house-mixes.com/tracks/popular',2,icon,'',fanart)
         addDir('Latest Tracks','http://www.house-mixes.com/tracks',2,icon,'',fanart)
         addDir('Search','url',50,icon,'',fanart)
         
def latestgenre(url):    
         gens = open(genres, 'r')
         link = gens.read()
         match=re.compile('<a href="(.+?)">(.+?)</a>').findall(link)
         match2 = sorted (match, key=lambda info: info[1]) 
         for url, name in match2:
             url = baseurl2+url
             addDir(name,url,2,icon,'',fanart)

def getmixes(url):
        link = open_url(url)
        match=re.compile('<a href="(.+?)"><img src="(.+?)" alt="(.+?)" class="img-responsive" /></a>').findall(link)
        for url, thumb, name in match:
            name2 = name.decode("ascii","ignore").replace('&#39;','')
            url = baseurl2+url
            addDirPlayable(name2,url,100,thumb,'',fanart)

def Search(url):
        search_entered =''
        keyboard = xbmc.Keyboard(search_entered, 'Enter Atist or Song to find')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search_entered = keyboard.getText().replace(' ','+')
        if search_entered == None or len(search_entered)<1:
                end()
        else:
                url = 'http://www.house-mixes.com/Search?query='+ search_entered
        getmixes(url)
        
############################ STANDARD  #####################################################################################
        
def PLAYLINK(url,name):
         link = open_url(url)
         if 'Media Not Found - May no longer exist' in link:
            notification('House Mixes', 'Media Not Found - May no longer exist', '5000',icon)
         else:
             match=re.compile('<a href="(.+?)" class="player-playpause" id="player-playpause"></a>').findall(link)
             playabletune = match[0].replace('<','').replace('>','').replace(' ','%20')
             print playabletune
             playlist = xbmc.PlayList(1)
             playlist.clear()
             liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage='')
             liz.setInfo('music', {'Title':name})
             liz.setProperty('mimetype', 'audio/mpeg')                
             playlist.add(playabletune, liz)
             xbmcPlayer = xbmc.Player()
             xbmcPlayer.play(playlist)
                                     
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
                                     
def open_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
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
    
def addDirPlayable(name,url,mode,iconimage,description,fanart):
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
 
if mode==None or url==None or len(url)<1: Index()
elif mode==1: latestgenre(url)
elif mode==2: getmixes(url)
elif mode==50: Search(url)
elif mode==100: PLAYLINK(url,name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
