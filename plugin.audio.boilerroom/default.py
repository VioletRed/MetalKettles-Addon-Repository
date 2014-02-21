import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil
from resources.libs.common_addon import Addon

SiteName='Boiler Room 1.0.0'
addon_id = 'plugin.audio.boilerroom'
addon = Addon('plugin.audio.boilerroom', sys.argv)
baseurl = 'http://boilerroom.tv/'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.PNG'))

def Index():
         addDir('Featured',baseurl,1,icon,'',fanart)
         addDir('Archive','http://boilerroom.tv/archive/',1,icon,'',fanart)
         #addDir('Search...',baseurl,3,'','',fanart)

def Featured(url):
        GetLinks(url)

def Featured(url):
        GetLinks(url)

def Search(url):
        search_entered =''
        keyboard = xbmc.Keyboard(search_entered, 'Enter Atist or Song to find')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search_entered = keyboard.getText().replace(' ','%20')
        if search_entered == None or len(search_entered)<1:
                end()
        else:
                url = 'http://boilerroom.tv/?s='+ search_entered
                print url
        link = open_url(url)
        match=re.compile('<div class="result recording">\n\t\t  \t      <a href="(.+?)">\n\t      \t<span class="main_image">\n\t      \t  <img src="(.+?)" />\n\t\t      \t\t      <span class="duration">(.+?)</span>\n\t\t\t  \n\t\t\t  \t\t\t  <i class="icon-play"></i>\n\t\t\t  \t\t    </span>\n\t        <span class="post_type">Recording</span>\n\t        <span class="post_title">(.+?)</span>\n\t        \t        <span class="city">(.+?)</span>\n\t    \t\t        <span class="date">(.+?)</span>\n\t      </a>\n\t      \t    </div>\n\t\t\t\t').findall(link)
        for url, img, dur, djname, city, rel in match:
                while ('ez') not in url:
                    vid = dur + '    ' + djname.replace('#038','').replace(';','') + '  (' + rel + ')  -  ' + city
                    addDir(vid,url,100,img,'',fanart)
        

def GetLinks(url):
        link = open_url(url)
        np=re.compile('<div class="next"><a href="(.+?)" >Older <span class="icon-angle-right"></span></a></div>').findall(link)
        match=re.compile('</article><article class="result recording">.+?<a href="(.+?)">.+?<img src="(.+?)" />.+?<span class="post_title">(.+?)</span>.+?<span class="city">(.+?)</span>.+?<span class="date">(.+?)</span>.+?<span class="duration">(.+?)</span>',re.DOTALL).findall(link)
        for url, img, djname, city, rel, dur in match:
                vid = dur + '    ' + djname.replace('#038','').replace(';','') + '  (' + rel + ')  -  ' + city
                addDir(vid,url,100,img,'',fanart)
        addDir('[B][COLOR gold]Next Page>>>[/COLOR][/B]',np[0],4,'','',fanart)
               

############################ STANDARD  #####################################################################################
        
def PLAYLINK(url):
         link = open_url(url)
         match=re.compile('<meta property="twitter:player" content="//www.youtube.com/embed/(.+?)?enable').findall(link)
         youtube_id = match[0]
         url =  'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid='+ youtube_id
         xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
         xbmcPlayer.play(url)
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
elif mode==1: Featured(url)
elif mode==2: Archive(url)
elif mode==3: Search(url)
elif mode==4: GetLinks(url)
elif mode==100: PLAYLINK(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
