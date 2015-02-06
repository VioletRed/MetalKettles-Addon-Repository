import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,random

AddonID ='plugin.video.DSVideos'
artpath = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID + '/resources/'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
faq = 'https://raw.githubusercontent.com/metalkettle/MetalKettles-Addon-Repository/master/donotdelete/ASFAQ'
ADDON=xbmcaddon.Addon(id='plugin.video.DSVideos')


def Index():
    addDir('Help Videos','http://gdata.youtube.com/feeds/api/users/CrazyH2008/uploads?start-index=1&alt=rss',1,artpath+'HelpVideos.png',fanart)
    addLink('News','http://www.droidsticks.co.uk/feed/',5,artpath+'News.png',fanart)
    addLink('Twitter Feed','url',3,artpath+'TwitterFeed.png',fanart)
    addLink('FAQs','url',4,artpath+'FAQ.png',fanart)
    setView('movies', 'MAIN')

def ytube():
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    link = link.replace('\n','').replace('  ','')
    print link
    response.close()
    match = re.compile("<media\:player url='http\://www.youtube.com/watch\?v=(.+?)&amp;feature=youtube_gdata_player'/>.+?<media\:title type='plain'>(.+?)</media\:title>",re.DOTALL).findall(link)
    for ytid,title in match:
        img = 'https://i.ytimg.com/vi/'+ytid+'/mqdefault.jpg'
        addLink(title,ytid,2,img,fanart,'')
    match = re.compile("http://gdata.youtube.com/feeds/api/users/CrazyH2008/uploads\?start-index=(.+?)\&alt=rss").findall(url)[0]
    page = int(match)+25
    npimg = xbmc.translatePath(os.path.join('special://home/addons/'+AddonID+'/resources', 'np.jpg'))
    newurl = 'http://gdata.youtube.com/feeds/api/users/CrazyH2008/uploads?start-index='+str(page)+'&alt=rss'
    addDir('Next Page',newurl,1,npimg,fanart,'')
    setView('movies', 'MAIN')

def PlayStream(url,iconimage):
    playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % url
    ok=True
    xbmc.Player ().play(playback_url)
    
def Twitter():
        text = ''
        twit = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?563513261841076224'
        req = urllib2.Request(twit)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link = link.replace('/n','')
        link = link.decode('utf-8').encode('utf-8').replace('&#39;','\'').replace('&#10;',' - ').replace('&#x2026;','')
        match=re.compile("<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)[1:]
        for status, dte in match:
            dte = dte[:-15]
            dte = '[COLOR blue][B]'+dte+'[/B][/COLOR]'
            text = text+dte+'\n'+status+'\n'+'\n'
        showText('@Droidsticks', text)
    
def FAQ():
    req = urllib2.Request(faq)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile("<query>(.+?)<query>.+?<result>(.+?)<result>",re.DOTALL).findall(link)
    text=''
    for query, result in match:
        query = '[COLOR blue][B]'+query+'[/B][/COLOR]'
        text = text+query+'\n'+result+'\n'+'\n'
    showText('[COLOR blue][B]FAQs[/B][/COLOR]', text)

def News(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.compile("<item><title>(.+?)</title><link>.+?><pubDate>(.+?) \+0000</pubDate>",re.DOTALL).findall(link)
    disc = '[COLOR red][B]For full details of any of these news articles please visit http://www.droidsticks.co.uk/news/[/B][/COLOR]'
    text=disc+'\n'+'\n'
    for news, newsdate in match:
        query = '[COLOR blue][B]'+newsdate+'[/B][/COLOR]'
        text = text+query+'\n'+news+'\n'+'\n'
    showText('[COLOR blue][B]DroidSticks News[/B][/COLOR]', text)

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def showText(heading, text):
    id = 10147
    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(500)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(500)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass
        
def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if ADDON.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )

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

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
    
def addDir(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

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

print "Mode: "+str(mode);print "URL: "+str(url);print "Name: "+str(name);print "IconImage: "+str(iconimage)
   
if mode==None or url==None or len(url)<1:Index()
elif mode==1:ytube()
elif mode==2:PlayStream(url,iconimage)
elif mode==3:Twitter()
elif mode==4:FAQ()
elif mode==5:News(url)


       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
