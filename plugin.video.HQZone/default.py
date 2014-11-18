import xbmc, xbmcgui, xbmcaddon, xbmcplugin, urllib, re, string, os, time
from t0mm0.common.net import Net as net

addon_id 	= 'plugin.video.HQZone'
art 		= xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
selfAddon 	= xbmcaddon.Addon(id=addon_id)
user 		= selfAddon.getSetting('hqusername')
passw 		= selfAddon.getSetting('hqpassword')
datapath 	= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
cookie_file     = os.path.join(os.path.join(datapath,'Cookies'), 'hqzone.cookies')
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))

CachePath=os.path.join(datapath,'Cache')
try: os.makedirs(CachePath)
except: pass
CookiesPath=os.path.join(datapath,'Cookies')
try: os.makedirs(CookiesPath)
except: pass
TempPath=os.path.join(datapath,'Temp')
try: os.makedirs(TempPath)
except: pass

def setCookie(srDomain):
    import hashlib
    m = hashlib.md5()
    m.update(passw)
    net().http_GET('http://www.hqzone.tv/forums/view.php?pg=live')
    net().http_POST('http://www.hqzone.tv/forums/login.php?do=login',{'vb_login_username':user,'vb_login_password':passw,'vb_login_md5password':m.hexdigest(),'vb_login_md5password_utf':m.hexdigest(),'do':'login','securitytoken':'guest','url':'http://www.hqzone.tv/forums/view.php?pg=live','s':''})
if user == '' or passw == '':
    if os.path.exists(cookie_file):
        try: os.remove(cookie_file)
        except: pass
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno('Hq Zone', 'Please enter your HQZone account details','or register if you dont have an account','at www.HQZone.Tv','Cancel','Login')
    if ret == 1:
        keyb = xbmc.Keyboard('', 'Enter Username or Email')
        keyb.doModal()
        if (keyb.isConfirmed()):
            username = keyb.getText()
            keyb = xbmc.Keyboard('', 'Enter Password:')
            keyb.doModal()
            if (keyb.isConfirmed()):
                password = keyb.getText()
                selfAddon.setSetting('hqusername',username)
                selfAddon.setSetting('hqpassword',password)

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
	
def MainMenu():
    setCookie('http://www.hqzone.tv/forums/view.php?pg=live')
    response = net().http_GET('http://www.hqzone.tv/forums/view.php?pg=live')
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    addDir('[COLOR white][B]-- View Schedule --[/B][/COLOR]','http://www.hqzone.tv/forums/calendar.php?c=1&do=displayweek',6,icon,fanart)
    addLink('[COLOR blue]_________________________[/COLOR]','','',icon,fanart)
    match=re.findall('(?sim)<h4 class="panel_headin.+?">([^<]+?)</h4><ul>(.+?)</ul>',link)
    for name,links in match[0:3]:
        if 'Channels' == name:
            name='[COLOR gold]VIP[/COLOR]'+' Member Streams'
        addDir(name,links,2,icon,fanart) #Main Channels
    addLink('[COLOR blue]_________________________[/COLOR]','','',icon,fanart)
    match=re.findall('(?sim)<h4 class="panel_headin.+?">([^<]+?)</h4><ul>(.+?)</ul>',link)
    for name,links in match[3:]:
        if 'Channels' == name:
            name='[COLOR gold][B}VIP[/B][/COLOR]'+' Member Streams'
        addDir(name,links,4,icon,fanart) #VIP
    addLink('','','',icon,fanart)
    addLink('[COLOR red][I]** NOTE:  If a stream fails to play, the selected channel is likely offline **[/I][/COLOR]','','',icon,fanart)
   
 
def VIPMenu(url):
    match=re.findall('(?sim)<li><a href="([^"]+?)" target="I1">([^<]+?)</a></li>',url)
    if not match:
        match=re.findall('(?sim)<a href="([^"]+?)" target="I1"><img src="([^"]+?)"',url)
    for url,name in match:
        url = 'http://www.hqzone.tv/forums/'+url
        addLink(name,url,5,icon,fanart)

def VODMenu(url):
    match=re.findall('(?sim)<li><a href="([^"]+?)" target="I1">([^<]+?)</a></li>',url)
    for url,name in match:
        url = 'http://www.hqzone.tv/forums/'+url
        addDir(name,url,3,icon,fanart) #default image for VOD section
 
def GetLinks(url,thumb):
    setCookie(url)
    response = net().http_GET(url)
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.findall('(?sim)sources: \[\{ file: "([^"]+?)" \}\],title: "([^"]+?)"',link)
    for url,name in match:
        addLink(name,url,5,icon,fanart)
		
def PlayStream(name,url,thumb):
    #notification('HQ Zone', 'Requesting stream from server', '3000',icon)
    try:
        ok=True
        url = get_link(url)     
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player ().play(url, liz, False)
    except:
        print 'FAIL'
        pass
        
def get_link(url):
    if 'mp4' in url:
        swf='http://www.hqzone.tv/forums/jwplayer/jwplayer.flash.swf'
        streamer=re.search('(?sim)(rtmp://.+?/vod/)(.+?.mp4)',url)
        return streamer.group(1)+'mp4:'+streamer.group(2)+' swfUrl='+swf+' pageUrl=http://www.hqzone.tv/forums/view.php?pg=live# token=WY846p1E1g15W7s'
    setCookie(url)
    response = net().http_GET(url)
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    m3u8=re.findall('<a href="([^"]+?.m3u8)">',link)
    flash=re.search('file=(.+?)&streamer=(.+?)&dock',link)
    if m3u8:
        return m3u8[0]
    elif flash:
        swf='http://www.hqzone.tv/forums/jwplayer/player.swf'
        return flash.group(2)+' playpath='+flash.group(1)+' swfUrl='+swf+' pageUrl='+url+' live=true timeout=20 token=WY846p1E1g15W7s'
    else:
        swf='http://www.hqzone.tv/forums/jwplayer/jwplayer.flash.swf'
        streamer=re.findall("file: '([^']+)',",link)[0]
        return streamer.replace('redirect','live')+' swfUrl='+swf+' pageUrl='+url+' live=true timeout=20 token=WY846p1E1g15W7s'

def Schedule(url):
    setCookie(url)
    response = net().http_GET(url)
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    month=re.findall('(?sim)<h2 class="blockhead">([^<]+?)</h2>',link)
    match=re.findall('(?sim)<h3><span class=".+?">([^<]+?)</span><span class="daynum" style=".+?" onclick=".+?">(\d+)</span></h3><ul class="blockrow eventlist">(.+?)</ul>',link)
    for day,num,data in match:
		addLink('[COLOR yellow]Times are E.S.T / GMT -5 | Follow us on Twitter for latest channel news, updates + more.[/COLOR]','','',icon,fanart) 
		addLink('[COLOR blue]'+day+' '+num+' '+month[0]+'[/COLOR]','','',icon,fanart)
		match2=re.findall('(?sim)<span class="eventtime">([^<]+?)</span><a href=".+?" title=".+?">([^<]+?)</a>',data)
		for time,title in match2:
			addLink('[COLOR yellow]'+time+'[/COLOR] '+title,'','',icon,fanart)
			
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")

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
              
params=get_params(); url=None; name=None; mode=None; path=None; iconimage=None
try: name=urllib.unquote_plus(params["name"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: mode=int(params["mode"])
except: pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: plot=urllib.unquote_plus(params["plot"])
except: pass
try: title=urllib.unquote_plus(params["title"])
except: pass
try: path=urllib.unquote_plus(params["path"])
except: pass

if mode==None or url==None or len(url)<1:MainMenu()            
elif mode==2:VIPMenu(url)      
elif mode==3:GetLinks(url,iconimage)      
elif mode==4:VODMenu(url)          
elif mode==5:PlayStream(name,url,iconimage)
elif mode==6:Schedule(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
