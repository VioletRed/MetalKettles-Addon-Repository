import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,shutil,urllib2,urllib,re,time,downloader,glob

addon_id        = 'plugin.program.configinstaller'
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

def Index():
    addDir('Install ProZone Config','http://prozone.getxbmc.com/ProConfigs/',0,icon,fanart,'')
    addDir('Upgrade/Downgrade OpenELEC','url',3,icon,fanart,'')
    addDir('KodiWorld.com Videos','http://kodiworld.com/m/videos/home/',5,icon,fanart,'')

def Videos(url):
    try:
        link = GetUrl(url)
        match = re.compile('<div class="sys_file_search_pic" style="(.+?)">.+?<div class="sys_file_search_title"><a href="(.+?)" title="(.+?)">.+?</a></div>.+?<div class="sys_file_search_from"><a href=".+?">(.+?)</a></div>',re.DOTALL).findall(link)
        for img,url,name,poster in match:
            img = re.compile("background\-image\: url\('(.+?)'\)").findall(img)[0]
            print img
            name = name.replace('&amp;','')
            addLink(name+'[I][COLOR blue]    ('+poster+')[/COLOR][/I]',url,6,img,fanart,'')
        page = re.compile('class="active_page">(.+?)</div>').findall(link)[0]
        np = int(page)+1
        np = str(np)
        npurl = 'http://kodiworld.com/m/videos/home/&status=approved&ownerStatus=Array&albumType=bx_videos&page='+np+'&per_page=12'
        addDir("Next Page >>",npurl,5,icon,fanart,'')
    except:pass

def PlayVideo(url,name):
    link = GetUrl(url)
    match = re.compile('<param name="movie" value="http://www.youtube.com/v/(.+?)&').findall(link)[0]
    playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % match
    ok=True
    xbmc.Player ().play(playback_url)
    
def ConfigList(url):
    link = GetUrl(url)
    match = re.compile('<li><a href="(.+?)"> (.+?)/</a></li>').findall(link)
    for url,name in match:
        if not 'Tutorials' in name:
            url = 'http://prozone.getxbmc.com/ProConfigs/'+url
            addDir(name,url,1,icon,fanart,'')

def Upgrade(url):
    addLink('Update To Kodi','http://prozone.getxbmc.com/Update-To-Kodi/',4,icon,fanart,'')
    addLink('Revert To Gotham','http://prozone.getxbmc.com/Revert-To-Gotham/',4,icon,fanart,'')
  
def DoUpgrade(url):
    base=url
    link = GetUrl(url)
    match = re.compile('<li><a href="(.+?)"> (.+?)</a></li>').findall(link)
    print match
    dir = os.path.dirname('/storage/.update/')
    shutil.rmtree(dir) 
    os.makedirs(dir, 0755 )
    for url,name in match:
        if not 'Parent' in name:
            url = base+url
            dp = xbmcgui.DialogProgress()
            dp.create("ProZone Config Installer","Downloading se;ected OpenELEC build",'', 'Please Wait.....')
            lib=os.path.join(dir, name)
            downloader.download(url, lib, dp)
    dialog = xbmcgui.Dialog() 
    ret = dialog.yesno('ProZone Config Installer', 'Click Continue to complete installation','Click Cancel to abort installation','','Cancel','Continue')
    if ret == 1:xbmc.executebuiltin('Reboot')
    else:
        shutil.rmtree(dir) 
        os.makedirs(dir, 0755 )
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")

def GetFile(url):
    link = GetUrl(url)
    match = re.compile('<li><a href="(.+?)"> (.+?)</a></li>').findall(link)
    for purl,name in match:
        if not 'Parent' in name:
            url=url+purl
            addLink(name,url,2,icon,fanart,'')
        
def InstallConfig(name,url):
    if not 'Parent' in name:
        dir = os.path.dirname('/storage/.restore/')
        shutil.rmtree(dir) 
        os.makedirs(dir, 0755 )
        dp = xbmcgui.DialogProgress()
        dp.create("ProZone Config Installer","Downloading Selected Config",'', 'Please Wait.....')
        lib=os.path.join(dir, name)
        downloader.download(url, lib, dp)
    dialog = xbmcgui.Dialog() 
    ret = dialog.yesno('ProZone Config Installer', 'Click Continue to complete installation','Click Cancel to abort installation','','Cancel','Continue')
    if ret == 1:xbmc.executebuiltin('Reboot')
    else:
        shutil.rmtree(dir) 
        os.makedirs(dir, 0755 )
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")

def GetUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link

def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    
def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
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
                            
params=get_params();url=None;name=None;mode=None;iconimage=None;description=None
try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass
try:mode=int(params["mode"])
except:pass
try:description=urllib.unquote_plus(params["description"])
except:pass

if mode==None or url==None or len(url)<1:Index()
elif mode==0:ConfigList(url)
elif mode==1:GetFile(url)
elif mode==2:InstallConfig(name,url)
elif mode==3:Upgrade(url)
elif mode==4:DoUpgrade(url)
elif mode==5:Videos(url)
elif mode==6:PlayVideo(url,name)


xbmcplugin.endOfDirectory(int(sys.argv[1]))

