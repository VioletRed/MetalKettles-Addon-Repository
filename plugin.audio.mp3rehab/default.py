import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil
from resources.libs.common_addon import Addon

SiteName='MP3Rehab 0.0.1'
addon_id = 'plugin.audio.mp3rehab'
addon = Addon('plugin.audio.mp3rehab', sys.argv)
baseurl = 'http://mp3rehab.com'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.PNG'))

def Index():
         addDir('Top 10 Downloads',baseurl,1,'http://mp3rehab.com/images/Mp3%20Gray.png','',fanart)
         addDir('Search','url',2,'http://mp3rehab.com/images/Mp3%20Gray.png','',fanart)

def Top10(url):
        GetLinks(url)

def Search(url):
        search_entered =''
        keyboard = xbmc.Keyboard(search_entered, 'Enter Atist or Song to find')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search_entered = keyboard.getText().replace(' ','+')
        if search_entered == None or len(search_entered)<1:
                end()
        else:
                url = 'http://mp3rehab.com/'+ search_entered +'-mp3.html'
        showsearch(url)
        
def showsearch(url):
        link = open_url(url)
        match=re.compile('<img class="album_art" src="(.+?)" alt=".+?">\r\n                              \r\n                <a class="headlink" href="(.+?)">\r\n                                      <h2 style="padding: 2px 8px 0 0; margin-bottom: 5px">(.+?)</h2>\r\n').findall(link)
        for art,url,name in match:
                addDir(name.replace('MP3',""),url,100,'http://mp3rehab.com/images/Mp3%20Gray.png','',fanart)
        match=re.compile('<a href="(.+?)" class="button gray right">Next Page</a>').findall(link)
        for np in match:
                addDir('Next Page>>>',np,3,'http://mp3rehab.com/images/Mp3%20Gray.png','',fanart)


def GetLinks(url):
        link = open_url(url)
        match=re.compile('<img class="album_art" src="(.+?)" alt="(.+?)">\r\n                              \r\n                <a class="headlink" href="(.+?)">\r\n').findall(link)
        for art,name, url in match:
                    addDir(name,url,100,art,'',fanart)
               

############################ STANDARD  #####################################################################################
        
def PLAYLINK(url):
         liz=xbmcgui.ListItem(name.replace('.mp3',''), iconImage="http://mp3rehab.com/images/Mp3%20Gray.png", thumbnailImage='http://mp3rehab.com/images/Mp3%20Gray.png')
         link = open_url(url)
         match=re.compile('<a class="filedownload" href="(.+?)" download=".+?" data-file-id=".+?" target="_blank" rel="nofollow"><strong>Download Mp3</strong></a>').findall(link)
         for tune in match:
                music = tune.replace(' ','%20')        
         xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_MPLAYER)
         xbmcPlayer.play(music)
         exit()
                
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

def addLink(name,url,iconimage,description,fanart):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        liz.setProperty("fanart_Image",fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
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
elif mode==1: Top10(url)
elif mode==2: Search(url)
elif mode==3: showsearch(url)
elif mode==100: PLAYLINK(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
