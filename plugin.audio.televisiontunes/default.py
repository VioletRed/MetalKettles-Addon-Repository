import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,xbmcaddon
 
SiteName='TelevisionTunes.com  [v0.0.1]  [Audio]'
BASE0 = 'http://www.televisiontunes.com/'
BASE = 'http://www.televisiontunes.com'

def CATEGORIES():
        AZurl = ('http://TelevisionTunes.com')
        req = urllib2.Request(AZurl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        azlist=re.compile('<li><a href="(.+?)" >(.+?)</a></li>').findall(link)
        addDir('Search','url',2,'')
        for url,name in azlist:
                print BASE
                addDir(name,BASE0 + url,1,'http://www.televisiontunes.com/images/TVGuy-Big2.png')
               
def GETTHEMES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<tr><td><a href="(.+?)">(.+?)</a></td></tr><tr><td>').findall(link)
        for url,name in match:
                addDir(name,url,100,'http://www.televisiontunes.com/images/TVGuy-Big2.png')
        
def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search TelevistionTunes')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')# sometimes you need to replace spaces with + or %20#
    if search_entered == None or len(search_entered)<1:
        end()
    else:
        url = 'http://www.televisiontunes.com/search.php?searWords=' + search_entered + '&Send=Search'
        print url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('&nbsp;<a href="(.+?)">(.+?)</a>').findall(link)
        for url,name in match:
                addDir(name,url,100,'http://www.televisiontunes.com/images/TVGuy-Big2.png') 
    
def TUNELINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        tune=re.compile('mp3: "(.+?)"').findall(link)
        for url in tune:
                fulllink = BASE + url
                nospace = str(fulllink).replace(' ','%20')
                xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
                print fulllink
                print nospace
                xbmcPlayer.play(nospace)
                exit()
 
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
               
def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
 
 
def addDir(name,url,mode,iconimage,isFolder=True):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
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
 
if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: GETTHEMES(url)
elif mode==2: SEARCH()
elif mode==100: TUNELINKS(url,name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
