import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon
 
SiteName='Putlocker.bz  [v0.0.1]  [Movies-TV]'
 
def CATEGORIES():
        addDir('Movies Added Today','http://putlocker.bz/today/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Movies Added Yesterday','http://putlocker.bz/yesterday/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Featured','http://putlocker.bz/featured/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Genres','url',2,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Years','url',3,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('AZ','url',4,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Search','url',5,'http://image1.putlocker.bz/images/mainlogo.jpg')    
       
def GETMOVIES(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('td width="20%" valign="top" style="padding-top: 5px; padding-left: 5px; padding-right: 5px;padding-bottom: 10px;"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" ').findall(link)
        for url,name,thumb in match:
                addDir(name,url,100,thumb)
        CheckForNextPage(link)
        
def GENRES(url):
        addDir('Action','http://putlocker.bz/genre/action/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Adventure','http://putlocker.bz/genre/adventure/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Animation','http://putlocker.bz/genre/animation/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Biography','http://putlocker.bz/genre/biography/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Comedy','http://putlocker.bz/genre/comedy/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Crime','http://putlocker.bz/genre/crime/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Documentory','http://putlocker.bz/genre/documentary/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Drama','http://putlocker.bz/genre/drama/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Family','http://putlocker.bz/genre/family/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Fantasy','http://putlocker.bz/genre/fantasy/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('History','http://putlocker.bz/genre/history/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Horror','http://putlocker.bz/genre/horror/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Musical','http://putlocker.bz/genre/musical/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Mystery','http://putlocker.bz/genre/mystery/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Romance','http://putlocker.bz/genre/romance/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Sci-Fi','http://putlocker.bz/genre/sci-fi/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Short','http://putlocker.bz/genre/short/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Sport','http://putlocker.bz/genre/sport/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Thriller','http://putlocker.bz/genre/thriller/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('War','http://putlocker.bz/genre/war/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('Western','http://putlocker.bz/genre/western/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
 
def YEARS(url):
        addDir('2013','http://putlocker.bz/year/2013/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2012','http://putlocker.bz/year/2012/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2011','http://putlocker.bz/year/2011/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2010','http://putlocker.bz/year/2010/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2009','http://putlocker.bz/year/2009/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2008','http://putlocker.bz/year/2008/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2007','http://putlocker.bz/year/2007/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2006','http://putlocker.bz/year/2006/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2005','http://putlocker.bz/year/2005/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2004','http://putlocker.bz/year/2004/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2003','http://putlocker.bz/year/2003/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2002','http://putlocker.bz/year/2002/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2001','http://putlocker.bz/year/2001/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('2000','http://putlocker.bz/year/2000/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('1999','http://putlocker.bz/year/1999/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('1998','http://putlocker.bz/year/1998/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('1997','http://putlocker.bz/year/1997/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('1996','http://putlocker.bz/year/1996/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('1995','http://putlocker.bz/year/1995/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('1994','http://putlocker.bz/year/1994/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
        addDir('1993','http://putlocker.bz/year/1993/1',1,'http://image1.putlocker.bz/images/mainlogo.jpg')
 
def AZ(url):
        AZurl = ('http://putlocker.bz/a-z/')
        req = urllib2.Request(AZurl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        azlist=re.compile('<a href="(.+?)" title="(.+?)" style="text-decoration:none;').findall(link)
        for url,name in azlist:
                addDir(name,url,1,'')
def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Putlocker.bz')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')# sometimes you need to replace spaces with + or %20#
    if search_entered == None or len(search_entered)<1:
        end()
    else:
        url = 'http://putlocker.bz/search/search.php?q=%s'%(search_entered)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('td width="20%" valign="top" style="padding-top: 5px; padding-left: 5px; padding-right: 5px;padding-bottom: 10px;"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" ').findall(link)
    inc = 0
    for url,name,thumb in match:

                        if inc > 5:        
                            addDir(name,url,100,thumb)
                        inc+=1
    
def VIDEOLINKS(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        links=re.compile('rel=".+?" href="(.+?)" target="_blank" title=".+?">Version .+?</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.+?').findall(link)
        for url in links:
                hostname=re.compile('http://(.+?)/').findall(url)
                hoster = str(hostname).replace('www.','')
                if urlresolver.HostedMediaFile(url).valid_url(): addDir (hoster,url,200,'',isFolder=False)
 
def PLAYLINK(name,url):
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        stream_url = urlresolver.HostedMediaFile(url).resolve()
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
        exit()

def CheckForNextPage(page): #I had regex trouble with re.compile() so I just did some oldschool .split()'ing.
    if '">Next</a>' in page:
        try:
            NextPage=page.split('">Next</a>')[0].split('href="')[-1].split('"')[0]
            #print NextPage
            if len(NextPage) > 0:
                addDir("[Next Page...] ",NextPage,mode,'http://image1.putlocker.bz/images/mainlogo.jpg') #Prints [Next] http://....
                #addDir("[Next]",NextPage,mode,'http://image1.putlocker.bz/images/mainlogo.jpg') #Prints [Next]
        except: pass
 
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
elif mode==1: GETMOVIES(url)
elif mode==2: GENRES(url)
elif mode==3: YEARS(url)
elif mode==4: AZ(url)
elif mode==5: SEARCH()
elif mode==100: VIDEOLINKS(url,name)
elif mode==200: PLAYLINK(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
