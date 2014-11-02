import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil,urlresolver
from resources.libs.common_addon import Addon

SiteName='Boiler Room 1.0.0'
addon_id = 'plugin.audio.boilerroom'
addon = Addon('plugin.audio.boilerroom', sys.argv)
baseurl = 'http://boilerroom.tv/'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.PNG'))

def Index():
         #addDir('Live','http://boilerroom.tv/live/',3,icon,'',fanart)
         #addDir('Program','http://boilerroom.tv/live/',1,icon,'',fanart)
         addDir('Archive','http://boilerroom.tv/archive/',1,icon,'',fanart)
         addDir('Cities','http://boilerroom.tv/cities/',2,icon,'',fanart)

def GetLinks(url):
        link = open_url(url)
        np=re.compile('<a href="(.+?)" >Next Page &raquo;</a>').findall(link)
        match=re.compile('<a href="(.+?)" class="recording recording-container brtv-recording-resize" style="background:url(.+?) no-repeat center center; background-size:cover">\n  <div class="dark-fade"></div>\n  <span class="recording-date">(.+?)</span>\n    <h1 class="recording-title group">\n    <i class="play-recording ic-play-fill left"></i>\n    <div class="facts left">\n      <span>(.+?)</span>\n      <span class="recording-length">(.+?)</span>').findall(link)
        for url,imgurl,recdate,dj,rec in match:
                dj = dj.decode("ascii","ignore").replace('#039;','').replace('\u266b ','').replace('\u266b','').replace('#038;','').replace('&#8217;','').replace('&#8220;','').replace('&#8221;','')
                dj = '[COLOR cyan]%s[/COLOR]'%dj
                img = imgurl.replace('(','').replace(')','')
                djdesc = dj+' - '+recdate+' - '+rec
                addDir2(djdesc,url,100,img,'',fanart)
        for nexturl in np:
                addDir("[COLOR gold]Next Page..[/COLOR]",nexturl,1,'','',fanart)

def GetCities(url):
        link = open_url(url)
        match=re.compile('<li class="other-city">\n          <a href="(.+?)">(.+?)</a>').findall(link)
        for url,city in match:
                addDir(city,url,1,icon,'',fanart)

def GetLive(url):
        link = open_url(url)
        match=re.compile('<a href="(.+?)" itemprop="url">\n    <aside class=".+?">.+?</aside>\n    <aside class=".+?">Live</aside>\n    <span class="main_image">\n      <img src="(.+?)" itemprop="photo" />\n    </span>\n    <span class="info">\n      <span class="description">(.+?)</span>').findall(link)
        for url,img,desc in match:
                addDir2(desc,url,200,icon,'',fanart)

def PLAYLIVE(url):
         link = open_url(url)
         match=re.compile('ng-src="(.+?)"').findall(link)
         for url in match:
                 url = 'http:' + url
                 newurl = url.split('?',2)[0]
                 newurl = 'http://www.youtube.com/watch?v=1uy80YYvdjo'
         resolved_url = urlresolver.HostedMediaFile(newurl).resolve()
         playlist = xbmc.PlayList(1)
         playlist.clear()
         listitem = xbmcgui.ListItem(name, iconImage='DefaultVideo.png')
         listitem.setInfo("Video", {"Title":name})
         listitem.setProperty('mimetype', 'video/x-msvideo')
         listitem.setProperty('IsPlayable', 'true')
         playlist.add(resolved_url,listitem)
         xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
         xbmcPlayer.play(playlist)
                
        
               

############################ STANDARD  #####################################################################################
        
def PLAYLINK(url,img,dj):
         link = open_url(url)
         match=re.compile('<meta property="twitter:player" content="(.+?)" />').findall(link)
         for url in match:
                 newurl = 'http:' + url
                 if 'youtube' in newurl:
                         ytid = newurl.split('/',4)[4].split('?',1)[0]
                         newurl='http://www.youtube.com/watch?v='+ytid              
         resolved_url = urlresolver.HostedMediaFile(newurl).resolve()
         playlist = xbmc.PlayList(1)
         playlist.clear()
         listitem = xbmcgui.ListItem(name, iconImage='DefaultVideo.png')
         listitem.setInfo("Video", {"Title":name})
         listitem.setProperty('mimetype', 'video/x-msvideo')
         listitem.setProperty('IsPlayable', 'true')
         playlist.add(resolved_url,listitem)
         xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
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
               
def addDir(name,url,mode,iconimage,description,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir2(name,url,mode,iconimage,description,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
 
 
params=get_params(); url=None; name=None; mode=None; site=None; img=None; dj=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: img=urllib.unquote_plus(params["img"])
except: pass
try: dj=urllib.unquote_plus(params["dj"])
except: pass

 
print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name); print "Img: "+str(img)
 
if mode==None or url==None or len(url)<1: Index()
                                    
elif mode==1: GetLinks(url)
elif mode==2: GetCities(url)
elif mode==3: GetLive(url)
elif mode==100: PLAYLINK(url,img,dj)
elif mode==200: PLAYLIVE(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
