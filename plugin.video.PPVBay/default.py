import xbmc, xbmcgui, xbmcaddon, xbmcplugin, urllib, re, string, os, time, json, urllib2, cookielib, md5, mknet, socket

addon_id 	= 'plugin.video.PPVBay'
art 		= xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
selfAddon 	= xbmcaddon.Addon(id=addon_id)
user 		= selfAddon.getSetting('username')
passw 		= selfAddon.getSetting('password')
datapath 	= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
cookie_file     = os.path.join(os.path.join(datapath,''), 'PPVcookie.lwp')
net             = mknet.Net()
socket.setdefaulttimeout(60)

def setCookie(srDomain):
    import hashlib
    m = hashlib.md5()
    m.update(passw)
    net.http_GET('http://www.ppvbay.com/forum.php')
    net.http_POST('http://www.ppvbay.com/login.php?do=login',{'vb_login_username':user,'vb_login_password':passw,'vb_login_md5password':m.hexdigest(),'vb_login_md5password_utf':m.hexdigest(),'do':'login','securitytoken':'guest','url':'http://www.ppvbay.com/forum.php','s':''})
    net.save_cookies(cookie_file)
    net.set_cookies(cookie_file)

if user == '' or passw == '':
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno('PPV Bay', 'Please enter your account details','or register if you dont have an account','at http://www.ppvbay.com/','Cancel','Login')
    if ret == 1:
        keyb = xbmc.Keyboard('', 'Enter Username')
        keyb.doModal()
        if (keyb.isConfirmed()):
            username = keyb.getText()
            keyb = xbmc.Keyboard('', 'Enter Password:')
            keyb.doModal()
            if (keyb.isConfirmed()):
                password = keyb.getText()
                selfAddon.setSetting('username',username)
                selfAddon.setSetting('password',password)	
def MainMenu():
    setCookie('http://www.ppvbay.com/forum.php')
    net.set_cookies(cookie_file)
    response = net.http_GET('http://www.ppvbay.com/forum.php')
    if '<li class="welcomelink">Welcome, <a href="member.php?' in response.content: 
        addDir('[COLOR cyan]----Calendar----[/COLOR]','url',3,icon,fanart)
        addLink('','url','mode',icon,fanart)
        addDir('[COLOR cyan]Elite[/COLOR] Channels','http://www.ppvbay.com/view.php?pg=elite',1,icon,fanart)
        addDir('Replays','http://www.ppvbay.com/view.php?pg=replays',1,icon,fanart)
        addLink('','url','mode',icon,fanart)
        addLink('[COLOR blue]Twitter[/COLOR] Feed','url',5,icon,fanart)
        addLink('[COLOR gold]Support[/COLOR]','url',4,icon,fanart)
    else:addLink('[COLOR cyan]Click here to login[/COLOR]','url',6,icon,fanart)
    xbmc.executebuiltin('Container.SetViewMode(50)')

def refresh():
    xbmc.executebuiltin('Container.Refresh')

def StreamMenu(name,url):
    net.set_cookies(cookie_file)
    response = net.http_GET(url)
    link = response.content
    match=re.compile('<a href="(.+?)"><font size="4"><font color="White">(.+?)</font>').findall(link)
    print match
    for url, name in match:
        url= 'http://www.ppvbay.com/'+url
        addLink(name,url,2,icon,fanart)

def PlayStream(url):
    page = url
    net.set_cookies(cookie_file)
    response = net.http_GET(url)
    link = response.content
    if 'mp4' in link:
        swf='http://www.ppvbay.com/player.swf'
        match=re.compile('flashvars="streamer=(.+?)&amp;file=(.+?)&').findall(link)
        for one,two in match:
            url = one + '/' + two + ' swfUrl='+swf+' pageUrl='+page
    else:
        swf='http://www.ppvbay.com/player.swf'
        match=re.compile('flashvars="streamer=(.+?)&amp;file=(.+?)&').findall(link)
        for one,two in match:
            url = one + ' playpath='+ two + ' swfUrl='+swf+' pageUrl='+page+' live=true timeout=10'
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    xbmc.Player ().play(url, liz, False)

def schedule(url):
    net.set_cookies(cookie_file)
    response = net.http_GET('http://www.ppvbay.com/calendar.php?c=1&do=displayweek')
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    month=re.findall('<h2 class="blockhead">([^<]+?)</h2>',link)
    match=re.findall('<h3><span class=".+?">([^<]+?)</span><span class="daynum" style=".+?" onclick=".+?">(\d+)</span></h3><ul class="blockrow eventlist">(.+?)</ul>',link)
    for day,num,data in match:
		addLink('[COLOR cyan][B]'+day+' '+num+'[/B][/COLOR]','url','mode',icon,fanart)
                match2=re.compile('<span class="eventtime">(.+?)</span>.+?title="(.+?)">',re.DOTALL).findall(link)
		for time,title in match2:
                        title = title.replace('amp;','')
			addLink('[COLOR blue]'+time+'[/COLOR] '+title,'url','mode',icon,fanart)
    xbmc.executebuiltin('Container.SetViewMode(51)')
    
def suppop():
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR cyan]Contact Us[/COLOR]', 'Via Our Forun At http://www.ppvbay.com/forum.php ','Via Twitter - @PPVBay','Or Find us on Facebook')    
    
def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass

def twitter():
        text = ''
        twit = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?582961205452648448'
        response = net.http_GET(twit)
        link = response.content
        link = link.replace('/n','')
        link = link.encode('ascii', 'ignore').decode('ascii').decode('ascii').replace('&#39;','\'').replace('&#xA0;','').replace('&#x2026;','').replace('amp;','')
        match=re.compile("<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)[1:]
        for status, dte in match:
            dte = dte[:-15]
            dte = '[COLOR cyan][B]'+dte+'[/B][/COLOR]'
            text = text+dte+'\n'+status+'\n'+'\n'
        showText('[COLOR cyan][B]@PPVBay[/B][/COLOR]', text)

def get_url(url):
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
elif mode==1:StreamMenu(name,url)
elif mode==2:PlayStream(url)
elif mode==3:schedule(url)
elif mode==4:suppop()
elif mode==5:twitter()
elif mode==6:refresh()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
