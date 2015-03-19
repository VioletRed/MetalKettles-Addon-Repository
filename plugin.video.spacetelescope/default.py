import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil
 
SiteName='Space Telescope 0.0.1'
addon_id = 'plugin.video.spacetelescope'
baseurl = 'http://www.spacetelescope.org/videos/'
videobase = 'http://www.spacetelescope.org'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.PNG'))

def INDEX():
        link = open_url(baseurl)
        match=re.compile('<a class=".+?" href="(.+?)" >(.+?)</a>').findall(link)
        for url, cat in match:
                if 'category'in url:
                        cat2 = cat.replace('&#39;','').replace('&amp;','').replace('HD','Best')
                        url = videobase + url
                        addDir(cat2,url,1,icon,'',fanart)

def get_video_list(url):
        link = open_url(url)
        match=re.compile('<td class=".+?" ><a href="(.+?)"><img src="(.+?)" width="122" alt="(.+?)" /></a></td>').findall(link)
        for url, thumb, name in match:
                url = videobase + url
                thumb2 = videobase+thumb
                name2 = name.replace('&#39;','').replace('&amp;','')
                addLink(name2,url,3,thumb2,'',fanart)
        nextpage=re.compile('<span class="paginator_next">&nbsp;<a href="(.+?)">').findall(link)
        for Next_Page in nextpage:
                url = videobase + Next_Page
                addDir('Next Page>>>',url,1,icon,'',fanart)
        
        

############################ STANDARD  #####################################################################################
        
def PLAYLINK(name,url):
        link = open_url(url)
        vid_link=re.compile('<a href="(.+?)" rel="shadowbox;width=640;height=360" title=".+?">Medium Flash</a></span>').findall(link)[0]
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(vid_link,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
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

def addLink(name,url,mode,iconimage,description,fanart):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=icon)
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
 
if mode==None or url==None or len(url)<1: INDEX()
elif mode==1: get_video_list(url)
elif mode==2: get_videos(url)
elif mode==3: PLAYLINK(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
