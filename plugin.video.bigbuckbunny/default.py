import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil
from resources.libs.common_addon import Addon
addon_id = 'plugin.video.bigbuckbunny'
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.PNG'))

def INDEX():
        addDir('1080p','url',1,'http://www.bigbuckbunny.org/wp-content/uploads/dl_1080p.jpg','',fanart)
        addDir('720p','url',2,'http://www.bigbuckbunny.org/wp-content/uploads/dl_720p.jpg','',fanart)
        addDir('480p','url',3,'http://www.bigbuckbunny.org/wp-content/uploads/dl_480p.jpg','',fanart)

def ten(url):
        addLink('[B][COLOR gold]MP4[/COLOR][/B]                 1080p Surround','http://blender-mirror.kino3d.org/peach/bigbuckbunny_movies/big_buck_bunny_1080p_surround.avi',4,'http://www.bigbuckbunny.org/wp-content/uploads/dl_1080p.jpg','',fanart)
        addLink('[B][COLOR gold]H.264[/COLOR][/B]              1080p','http://blender-mirror.kino3d.org/peach/bigbuckbunny_movies/big_buck_bunny_1080p_h264.mov',4,'http://www.bigbuckbunny.org/wp-content/uploads/dl_1080p.jpg','',fanart)
        addLink('[B][COLOR gold]MSMP4[/COLOR][/B]          1080p Stereo','http://blender-mirror.kino3d.org/peach/bigbuckbunny_movies/big_buck_bunny_1080p_stereo.avi',4,'http://www.bigbuckbunny.org/wp-content/uploads/dl_1080p.jpg','',fanart)

def seven(url):
        addLink('[B][COLOR gold]MP4[/COLOR][/B]                 720p Surround','http://blender-mirror.kino3d.org/peach/bigbuckbunny_movies/big_buck_bunny_720p_surround.avi',4,'http://www.bigbuckbunny.org/wp-content/uploads/dl_720p.jpg','',fanart)
        addLink('[B][COLOR gold]H.264[/COLOR][/B]              720p','http://blender-mirror.kino3d.org/peach/bigbuckbunny_movies/big_buck_bunny_720p_h264.mov',4,'http://www.bigbuckbunny.org/wp-content/uploads/dl_720p.jpg','',fanart)
        addLink('[B][COLOR gold]MSMP4[/COLOR][/B]          720p Stereo','http://blender-mirror.kino3d.org/peach/bigbuckbunny_movies/big_buck_bunny_720p_stereo.avi',4,'http://www.bigbuckbunny.org/wp-content/uploads/dl_720p.jpg','',fanart)

def four(url):
        addLink('[B][COLOR gold]MP4[/COLOR][/B]                 420p Surround','http://blender-mirror.kino3d.org/peach/bigbuckbunny_movies/big_buck_bunny_480p_h264.mov',4,'http://www.bigbuckbunny.org/wp-content/uploads/dl_480p.jpg','',fanart)
        addLink('[B][COLOR gold]H.264[/COLOR][/B]              420p','http://blender-mirror.kino3d.org/peach/bigbuckbunny_movies/big_buck_bunny_480p_h264.mov',4,'http://www.bigbuckbunny.org/wp-content/uploads/dl_480p.jpg','',fanart)
        addLink('[B][COLOR gold]MSMP4[/COLOR][/B]          420p Stereo','http://blender-mirror.kino3d.org/peach/bigbuckbunny_movies/big_buck_bunny_480p_stereo.avi',4,'http://www.bigbuckbunny.org/wp-content/uploads/dl_480p.jpg','',fanart)

def PLAYLINK(name,url):
                playlist = xbmc.PlayList(1)
                playlist.clear()
                listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
                listitem.setInfo("Video", {"Title":name})
                listitem.setProperty('mimetype', 'video/x-msvideo')
                listitem.setProperty('IsPlayable', 'true')
                playlist.add(url,listitem)
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
 
if mode==None or url==None or len(url)<1: INDEX()
elif mode==1: ten(url)
elif mode==2: seven(url)
elif mode==3: four(url)
elif mode==4: PLAYLINK(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
