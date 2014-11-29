import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os,shutil,glob
from resources.libs.common_addon import Addon

addon_id 	= 'plugin.program.oepia'
art 		= xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
selfAddon 	= xbmcaddon.Addon(id=addon_id)
user 		= selfAddon.getSetting('piauser')
passw 		= selfAddon.getSetting('piapass')
fanart          = ''
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
destfol         = '/storage/.config/vpn-config'
ovpnpath        = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/servers', ''))
flag            = '0'

if user <> '' or passw <> '':
    flag = '1'
    
if user == '' or passw == '':
    dialog = xbmcgui.Dialog() 
    ret = dialog.yesno('PIA for OpenELEC', 'Please enter your Private Internet Access account details','','','Cancel','Login')
    if ret == 1:
        keyb = xbmc.Keyboard('', 'Username:')
        keyb.doModal()
        if (keyb.isConfirmed()):
            username = keyb.getText()
            keyb = xbmc.Keyboard('', 'Enter Password:')
            keyb.doModal()
            if (keyb.isConfirmed()):
                password = keyb.getText()
                selfAddon.setSetting('piauser',username)
                selfAddon.setSetting('piapass',password)
                user = selfAddon.getSetting('piauser')
                passw = selfAddon.getSetting('piapass')
                
def Index():
    if flag == '0':
        addDir('Setup Private Internet Access','url',1,icon,'',fanart)
    addDir('Remove Private Internet Access','url',2,icon,'',fanart)
    addDir('Check My IP Location','url',3,icon,'',fanart)

def setup():
    passpath = destfol + '/pass.txt'
    for filename in glob.glob(os.path.join(ovpnpath, '*.*')):
        shutil.copy(filename, destfol)
    auth = open(passpath,'a')
    auth.write(user)
    auth.write('\n')
    auth.write(passw)
    auth.close()
    dialog=xbmcgui.Dialog(); dialog.ok('Setup PIA',"ALL DONE!", 'Please restart XBMC/KODI to take effect')
    quit()

def remove():
    destfol2 = destfol + '/*.*'
    files = glob.glob(destfol2)
    for f in files:
        os.remove(f)
    selfAddon.setSetting('piauser','')
    selfAddon.setSetting('piapass','')
    dialog=xbmcgui.Dialog(); dialog.ok('Remove PIA',"ALL DONE!", 'Please restart XBMC/KODI to take effect')
    xbmc.executebuiltin("XBMC.ActivateWindow(Home)")

def myip():
    url = 'http://www.iplocation.net/'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match = re.compile("<td width='80'>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>.+?</td><td>(.+?)</td>").findall(link)
    inc = 1
    for ip, region, country, isp in match:
        if inc <2: dialog=xbmcgui.Dialog(); dialog.ok('External IP Checker',"[B][COLOR gold]Your IP Address is: [/COLOR][/B] %s" % ip, '[B][COLOR gold]Your IP is based in: [/COLOR][/B] %s' % country)
        inc=inc+1
    quit()
    
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
elif mode==1: setup()
elif mode==2: remove()
elif mode==3: myip()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
