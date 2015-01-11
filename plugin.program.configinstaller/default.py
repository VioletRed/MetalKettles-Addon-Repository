import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,shutil,urllib2,urllib,re,time,downloader,glob

addon_id        = 'plugin.program.configinstaller'
ADDON           = xbmcaddon.Addon(id=addon_id)
selfAddon       = xbmcaddon.Addon(id=addon_id)
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.PNG'))

def ConfigList():
    link = GetUrl('http://prozone.getxbmc.com/ProConfigs/')
    print link
    match = re.compile('<li><a href="(.+?)"> (.+?)/</a></li>').findall(link)
    print match
    for url,name in match:
        if not 'Tutorials' in name:
            url = 'http://prozone.getxbmc.com/ProConfigs/'+url
            addDir(name,url,1,icon,fanart,'')

def GetFile(url):
    link = GetUrl(url)
    print link
    match = re.compile('<li><a href="(.+?)"> (.+?)</a></li>').findall(link)
    for purl,name in match:
        if not 'Parent' in name:
            url=url+purl
            addLink(name,url,2,icon,fanart,'')
        
def InstallConfig(name,url):
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
    else:xbmc.executebuiltin("XBMC.ActivateWindow(Home)")

def GetUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
        
def InstallConfig2(name,url):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("DroidSticks Wizard","Downloading configuration files",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Just a little while longer :)")
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("DroidSticks Wizard", "All Done", "Enjoy!")
    xbmc.executebuiltin('UpdateLocalAddons')

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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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

if mode==None or url==None or len(url)<1:ConfigList()
elif mode==1:GetFile(url)
elif mode==2:InstallConfig(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))

