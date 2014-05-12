import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil
from resources.libs.common_addon import Addon

addon_id = 'plugin.audio.spreaker'
addon = Addon('plugin.audio.spreaker', sys.argv)
apibase = 'http://api.spreaker.com/explore/category/'
apicatend = '/items?&max_per_page=50&page=1'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

def Index():
         addDir('Arts',apibase + 'arts' + apicatend,1,icon,'',fanart)
         addDir('Culture',apibase + 'culture' + apicatend,1,icon,'',fanart)
         addDir('Entertainment',apibase + 'entertainment' + apicatend,1,icon,'',fanart)
         addDir('Hobbies',apibase + 'hobbies' + apicatend,1,icon,'',fanart)
         addDir('Information',apibase + 'information' + apicatend,1,icon,'',fanart)
         addDir('Music',apibase + 'music' + apicatend,1,icon,'',fanart)
         addDir('Science',apibase + 'science' + apicatend,1,icon,'',fanart)
         addDir('Sports',apibase + 'sports' + apicatend,1,icon,'',fanart)
         addDir('Technology',apibase + 'technology' + apicatend,1,icon,'',fanart)
         addDir('[B][COLOR red]LIVE NOW[/COLOR][/B]','http://api.spreaker.com/episodes/live',3,icon,'',fanart)
         addDir('[B][COLOR gold]Search Show[/COLOR][/B]','url',50,icon,'',fanart)

def getshows(url):
         npbase = url
         link = open_url(url)
         thispage=re.compile('"current_page":(.+?),').findall(link)
         tp = int(thispage[0])
         lastpage=re.compile('"last_page":(.+?),').findall(link)
         lp = int(lastpage[0])
         pp = tp+1
         nextpage = npbase[:-1] + str(pp)
         print nextpage
         match=re.compile('"show_id":(.+?),.+?"title":"(.+?)".+?"site_url":"(.+?)".+?"play_url":"(.+?)"',re.DOTALL).findall(link) 
         for showid,name,url,thumb in match:
             url = url.replace('\/','/')
             thumb = thumb.replace('\/','/')
             name2 = name.decode("ascii","ignore").replace('&amp;#039;','').replace('\u266b ','').replace('\u266b','')
             addDir(name2,url,2,thumb,'',fanart,showid)
         if pp > lp:
             pass
         else:
             addDir('[B][COLOR gold]Next Page >>[/COLOR][/B]',nextpage,1,'','',fanart)
               
def getepisodes(url):
        link = open_url(url)
        imgmatch=re.compile('<meta property="og:image" content="(.+?)"/>').findall(link)
        img = imgmatch[0]
        match=re.compile('<a class="btnn_player play" data-episode_id="(.+?)" title="(.+?)"').findall(link)
        for episode, name in match:
            name2 = name.decode("ascii","ignore").replace('&amp;#039;','').replace('\u266b ','').replace('\u266b','')
            playurl = 'http://api.spreaker.com/listen/episode/'+ episode + '/http'
            addDirPlayable(name2,playurl,100,img,'',fanart)
    
def livenow(url):
         link = open_url(url)
         match=re.compile('"episode_id":(.+?),.+?"title":"(.+?)".+?"site_url":"(.+?)".+?"play_url":"(.+?)"',re.DOTALL).findall(link) 
         for episode,name,url,thumb in match:
             url = url.replace('\/','/')
             thumb = thumb.replace('\/','/')             
             name2 = name.decode("ascii","ignore").replace('&amp;#039;','').replace('\u266b ','').replace('\u266b','')
             playurl = 'http://api.spreaker.com/listen/episode/'+ episode + '/http'
             addDirPlayable(name2,playurl,100,thumb,'',fanart)

def searchshow(url):
        search_entered =''
        keyboard = xbmc.Keyboard(search_entered, 'Enter show to find')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search_entered = keyboard.getText().replace(' ','+')
        if search_entered == None or len(search_entered)<1:
                end()
        else:
                url = 'http://api.spreaker.com/show/search/' + search_entered + '?&max_per_page=50&page=1'
                link = open_url(url)
                match=re.compile('"title":"(.+?)".+?"site_url":"(.+?)".+?"play_url":"(.+?)"',re.DOTALL).findall(link) 
                for name,url,thumb in match:
                    url = url.replace('\/','/')
                    thumb = thumb.replace('\/','/')
                    name2 = name.decode("ascii","ignore").replace('&amp;#039;','').replace('\u266b ','').replace('\u266b','')
                    addDir(name2,url,2,thumb,'',fanart)

############################ STANDARD  #####################################################################################
        
def PLAYLINK(url,name):
        name = name.replace('Play','')
        playlist = xbmc.PlayList(1)
        playlist.clear()
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage='')
        liz.setInfo('music', {'Title':name})
        liz.setProperty('mimetype', 'audio/mpeg')                
        playlist.add(url, liz)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)

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
               
def addDir(name,url,mode,iconimage,description,fanart,showid=''):
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
elif mode==1: getshows(url)
elif mode==2: getepisodes(url)
elif mode==3: livenow(url)
elif mode==50: searchshow(url)
elif mode==100: PLAYLINK(url,name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
