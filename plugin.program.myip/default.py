import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon,os
from resources.libs.common_addon import Addon

addon_id = 'plugin.program.myip'
addon = Addon('plugin.program.myip', sys.argv)
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))

#Network
exip = xbmc.getInfoLabel('Network.IPAddress')
gateway = xbmc.getInfoLabel('Network.GatewayAddress')
dns1 = xbmc.getInfoLabel('Network.DNS1Address')
dns2 = xbmc.getInfoLabel('Network.DNS2Address')
fname = xbmc.getInfoLabel('System.FriendlyName').replace('XBMC (','').replace(')','')

#System
systime = xbmc.getInfoLabel('System.Time')
sysdate = xbmc.getInfoLabel('System.Date')
hddused = xbmc.getInfoLabel('System.UsedSpace')
hddfree = xbmc.getInfoLabel('System.FreeSpace')
sysbuild = xbmc.getInfoLabel('System.BuildVersion')
sysbuilddate = xbmc.getInfoLabel('System.BuildDate')
freemem = xbmc.getInfoLabel('System.FreeMemory')
screen = xbmc.getInfoLabel('System.ScreenMode')
lang = xbmc.getInfoLabel('System.Language')
plat = sys.platform

def Index():
    addDir('[B][COLOR gold]Network Information [/COLOR][/B]','url',1,icon,'',fanart)
    addDir('[B][COLOR gold]System Information [/COLOR][/B]','url',2,icon,'',fanart)

def Network():
    url = 'http://www.iplocation.net/'
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match = re.compile("<td width='80'>(.+?)</td><td>(.+?)</td><td>(.+?)</td><td>.+?</td><td>(.+?)</td>").findall(link)
    inc = 1
    for ip, region, country, isp in match:
        if inc <2:
            addDir('[B][COLOR gold]Your External IP Address is: [/COLOR][/B]' + ip,'','',icon,'',fanart)
            addDir('[B][COLOR gold]Your IP is based in: [/COLOR][/B]' + country,'','',icon,'',fanart)
            addDir('[B][COLOR gold]Your Service Provider is:[/COLOR][/B] ' + isp,'','',icon,'',fanart)
            inc = inc+1
    addDir('[B][COLOR gold]Your Internal IP Address is:[/COLOR][/B] ' + exip,'','',icon,'',fanart)
    addDir('[B][COLOR gold]Your Network Friendly Name is:[/COLOR][/B] ' + fname,'','',icon,'',fanart)
    addDir('[B][COLOR gold]Your Network Gateway IP Address is:[/COLOR][/B] ' + gateway,'','',icon,'',fanart)
    addDir('[B][COLOR gold]Your Network DNS 1 Address is:[/COLOR][/B] ' + dns1,'','',icon,'',fanart)
    addDir('[B][COLOR gold]Your Network DNS 2 Address is:[/COLOR][/B] ' + dns2,'','',icon,'',fanart)
       
def System():
    addDir('[B][COLOR gold]Your System Time is:[/COLOR][/B] ' + systime,'','',icon,'',fanart)
    addDir('[B][COLOR gold]Your System Date is:[/COLOR][/B] ' + sysdate,'','',icon,'',fanart)
    addDir('[B][COLOR gold]Your Storage Used Space is:[/COLOR][/B] ' + hddused,'','',icon,'',fanart)
    addDir('[B][COLOR gold]Your Storage Free Space is:[/COLOR][/B] ' + hddfree,'','',icon,'',fanart)
    addDir('[B][COLOR gold]Your Free Memory is:[/COLOR][/B] ' + freemem,'','',icon,'',fanart)
    addDir('[B][COLOR gold]Your Screen Mode is:[/COLOR][/B] ' + screen,'','',icon,'',fanart)
    addDir('[B][COLOR gold]Your System Language is:[/COLOR][/B] ' + lang,'','',icon,'',fanart)
    addDir('[B][COLOR gold]Your Ststem Platform is:[/COLOR][/B] ' + plat,'','',icon,'',fanart)

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
elif mode==1: Network()
elif mode==2: System()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
