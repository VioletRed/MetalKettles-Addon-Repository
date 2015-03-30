import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,shutil,urllib2,urllib,re,time,downloader,glob

addon_id        = 'plugin.program.configinstaller'
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

def Index():
    addDir('Install ProZone Config','http://prozone.getxbmc.com/ProConfigs/',0,icon,fanart,'')
    addDir('Install Community Configs','http://prozone.getxbmc.com/CommunityConfigs/',7,icon,fanart,'')
    addDir('Upgrade/Downgrade OpenELEC','http://prozone.getxbmc.com/Builds%20-%20Update%20or%20Downgrade%20HERE/',3,icon,fanart,'')
    
def ConfigList(url):
    link = GetUrl(url)
    match = re.compile('<li><a href="(.+?)"> (.+?)/</a></li>').findall(link)
    for url,name in match:
        if not 'Tutorials' in name:
            url = 'http://prozone.getxbmc.com/ProConfigs/'+url
            addDir(name,url,1,icon,fanart,'')
            
def ComConfigList(url):
    link = GetUrl(url)
    match = re.compile('<li><a href="(.+?)"> (.+?)/</a></li>').findall(link)
    for url,name in match:
        if not 'ftpquota' in name:
            url = 'http://prozone.getxbmc.com/CommunityConfigs/'+url
            addDir(name,url,1,icon,fanart,'')

def Upgrade(url):
    link = GetUrl(url)
    match = re.compile('<li><a href="(.+?)"> (.+?)/</a></li>').findall(link)
    for url,name in match:
        if not 'ftpquota' in name:
            url = 'http://prozone.getxbmc.com/Builds%20-%20Update%20or%20Downgrade%20HERE/'+url
            addDir(name,url,4,icon,fanart,'')
 
def DoUpgrade(url):
    base=url
    link = GetUrl(url)
    match = re.compile('<li><a href="(.+?)"> (.+?)</a></li>').findall(link)
    filedir = '/storage/.update/'
    try:
        shutil.rmtree(filedir)
    except: pass
    os.makedirs(filedir, 0755 )
    for url,name in match:
        if not 'Parent' in name:
          if not 'zip' in url:  
            url = base+url
            dp = xbmcgui.DialogProgress()
            dp.create("ProZone Config Installer","Downloading selected OpenELEC build",'', 'Please Wait.....')
            lib=os.path.join(filedir, name)
            downloader.download(url, lib, dp)
    dialog = xbmcgui.Dialog() 
    ret = dialog.yesno('ProZone Config Installer', 'Click Continue to complete installation','Click Cancel to abort installation','','Cancel','Continue')
    if ret == 1:xbmc.executebuiltin('Reboot')
    else:
        shutil.rmtree(filedir) 
        os.makedirs(filedir, 0755 )
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")

def GetFile(url):
    link = GetUrl(url)
    match = re.compile('<li><a href="(.+?)"> (.+?)</a></li>').findall(link)
    for purl,name in match:
        if not 'Parent' in name:
          if not 'ftpquota' in name:
            url=url+purl
            addDir(name,url,2,icon,fanart,'')
        
def InstallConfig(name,url):
    if 'tar' in url:
        if not 'Parent' in name:
            filedir = '/storage/.restore/'
            try:
                shutil.rmtree(filedir)
            except: pass
            os.makedirs(filedir, 0755 )
            dp = xbmcgui.DialogProgress()
            dp.create("ProZone Config Installer","Downloading Selected Config",'', 'Please Wait.....')
            lib=os.path.join(filedir, name)
            downloader.download(url, lib, dp)
        dialog = xbmcgui.Dialog() 
        ret = dialog.yesno('ProZone Config Installer', 'Click Continue to complete installation','Click Cancel to abort installation','','Cancel','Continue')
        if ret == 1:xbmc.executebuiltin('Reboot')
        else:
            shutil.rmtree(filedir) 
            os.makedirs(filedir, 0755 )
            xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
    else:GetFile(url)

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
elif mode==7:ComConfigList(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

