import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,simplejson,os
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

from metahandler import metahandlers
 
addon_id = 'plugin.video.putlocker'
selfAddon = xbmcaddon.Addon(id=addon_id)
metaget = metahandlers.MetaData(preparezip=False)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.PNG'))
artpath = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
xbmc.executebuiltin('Container.SetViewMode(500)')

def CATEGORIES():
        xbmc.executebuiltin('Container.SetViewMode(500)')
        addDir2('Featured','http://putlocker.bz/featured/1',1,artpath+'movies.png','',fanart)
        addDir2('Genres','url',2,artpath+'genres.png','',fanart)
        addDir2('Years','url',3,artpath+'year2.png','',fanart)
        addDir2('A - Z','url',4,artpath+'alphabet.png','',fanart)
        addDir2('Search','url',5,artpath+'search.png','',fanart)    

def GETMOVIES(url):
        xbmc.executebuiltin('Container.SetViewMode(500)')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('td width="20%" valign="top" style="padding-top: 5px; padding-left: 5px; padding-right: 5px;padding-bottom: 10px;"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" ').findall(link)
        for url,name,thumb in match:
		addDir(name,url,100,thumb)
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        CheckForNextPage(link)
        
def GENRES(url):
        xbmc.executebuiltin('Container.SetViewMode(500)')
        addDir2('Action','http://putlocker.bz/genre/action/1',1,artpath+'action.png','',fanart)
        addDir2('Adventure','http://putlocker.bz/genre/adventure/1',1,artpath+'adventure.png','',fanart)
        addDir2('Animation','http://putlocker.bz/genre/animation/1',1,artpath+'animation.png','',fanart)
        addDir2('Biography','http://putlocker.bz/genre/biography/1',1,artpath+'biography.png','',fanart)
        addDir2('Comedy','http://putlocker.bz/genre/comedy/1',1,artpath+'comedy.png','',fanart)
        addDir2('Crime','http://putlocker.bz/genre/crime/1',1,artpath+'crime.png','',fanart)
        addDir2('Documentary','http://putlocker.bz/genre/documentary/1',1,artpath+'documentary.png','',fanart)
        addDir2('Drama','http://putlocker.bz/genre/drama/1',1,artpath+'drama.png','',fanart)
        addDir2('Family','http://putlocker.bz/genre/family/1',1,artpath+'family.png','',fanart)
        addDir2('Fantasy','http://putlocker.bz/genre/fantasy/1',1,artpath+'fantasy.png','',fanart)
        addDir2('History','http://putlocker.bz/genre/history/1',1,artpath+'history.png','',fanart)
        addDir2('Horror','http://putlocker.bz/genre/horror/1',1,artpath+'horror.png','',fanart)
        addDir2('Musical','http://putlocker.bz/genre/musical/1',1,artpath+'musical.png','',fanart)
        addDir2('Mystery','http://putlocker.bz/genre/mystery/1',1,artpath+'mystery.png','',fanart)
        addDir2('Romance','http://putlocker.bz/genre/romance/1',1,artpath+'romance.png','',fanart)
        addDir2('Sci-Fi','http://putlocker.bz/genre/sci-fi/1',1,artpath+'sci-fi.png','',fanart)
        addDir2('Sport','http://putlocker.bz/genre/sport/1',1,artpath+'sport.png','',fanart)
        addDir2('Thriller','http://putlocker.bz/genre/thriller/1',1,artpath+'thriller.png','',fanart)
        addDir2('War','http://putlocker.bz/genre/war/1',1,artpath+'war.png','',fanart)
        addDir2('Western','http://putlocker.bz/genre/western/1',1,artpath+'western.png','',fanart)
 
def YEARS(url):
        xbmc.executebuiltin('Container.SetViewMode(500)')
        addDir2('2013','http://putlocker.bz/year/2013/1',1,artpath+'year2.png','',fanart)
        addDir2('2012','http://putlocker.bz/year/2012/1',1,artpath+'year2.png','',fanart)
        addDir2('2011','http://putlocker.bz/year/2011/1',1,artpath+'year2.png','',fanart)
        addDir2('2010','http://putlocker.bz/year/2010/1',1,artpath+'year2.png','',fanart)
        addDir2('2009','http://putlocker.bz/year/2009/1',1,artpath+'year2.png','',fanart)
        addDir2('2008','http://putlocker.bz/year/2008/1',1,artpath+'year2.png','',fanart)
        addDir2('2007','http://putlocker.bz/year/2007/1',1,artpath+'year2.png','',fanart)
        addDir2('2006','http://putlocker.bz/year/2006/1',1,artpath+'year2.png','',fanart)
        addDir2('2005','http://putlocker.bz/year/2005/1',1,artpath+'year2.png','',fanart)
        addDir2('2004','http://putlocker.bz/year/2004/1',1,artpath+'year2.png','',fanart)
        addDir2('2003','http://putlocker.bz/year/2003/1',1,artpath+'year2.png','',fanart)
        addDir2('2002','http://putlocker.bz/year/2002/1',1,artpath+'year2.png','',fanart)
        addDir2('2001','http://putlocker.bz/year/2001/1',1,artpath+'year2.png','',fanart)
        addDir2('2000','http://putlocker.bz/year/2000/1',1,artpath+'year2.png','',fanart)
        addDir2('1999','http://putlocker.bz/year/1999/1',1,artpath+'year2.png','',fanart)
        addDir2('1998','http://putlocker.bz/year/1998/1',1,artpath+'year2.png','',fanart)
        addDir2('1997','http://putlocker.bz/year/1997/1',1,artpath+'year2.png','',fanart)
        addDir2('1996','http://putlocker.bz/year/1996/1',1,artpath+'year2.png','',fanart)
        addDir2('1995','http://putlocker.bz/year/1995/1',1,artpath+'year2.png','',fanart)
        addDir2('1994','http://putlocker.bz/year/1994/1',1,artpath+'year2.png','',fanart)
        addDir2('1993','http://putlocker.bz/year/1993/1',1,artpath+'year2.png','',fanart)
 
def AZ(url):
        xbmc.executebuiltin('Container.SetViewMode(500)')
        AZurl = ('http://putlocker.bz/a-z/')
        req = urllib2.Request(AZurl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        azlist=re.compile('<a href="(.+?)" title="(.+?)" style="text-decoration:none;').findall(link)
        for url,name in azlist:
                name2 = name.split(' ',1)
                print name2
                if name2[0]=='0-9': name2[0]='num'
                addDir2(name,url,1,artpath+name2[0]+'.png','',fanart)
        
def SEARCH():
    xbmc.executebuiltin('Container.SetViewMode(500)')
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Putlocker.bz')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
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
                        if inc > 4:        
                            addDir(name,url,100,thumb)
                        inc+=1
    
def VIDEOLINKS(url,name):
        xbmc.executebuiltin('Container.SetViewMode(500)')
	req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        links=re.compile('<a.+?href="(.+?)".+?title=".+?">Version .+?<\/a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.+?').findall(link)
        for url in links:
                hostname=re.compile('http://(.+?)/').findall(url)
                hoster = str(hostname[0]).replace('www.','')
		if hoster=='putlocker.bz' :
                        PLAYLINKMainServer(name,url)
                else:
                        if urlresolver.HostedMediaFile(url).valid_url():
                                addDir (hoster,url,200,icon,'',fanart)
                	
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

def PLAYLINKMainServer(name,url):
        req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('proxy.link=movs[*](.*?)&').findall(link)
        newurl=decodeURL(match[0]);
        mydata=[('isslverify','true'),('iagent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8'),('url',newurl),('ihttpheader','true')]    #The first is the var name the second is the value
	mydata=urllib.urlencode(mydata)
	path='http://static2.movsharing.com/pluginss/plugins_player.php'
	req=urllib2.Request(path, mydata)
	req.add_header("Content-type", "application/x-www-form-urlencoded")
	link=urllib2.urlopen(req).read()
        response.close()
	match=re.compile('{"url":"http:\/\/(.*?)",".*?"type":"(.*?)"}').findall(link)
        indexurl=0;
        vformat=selfAddon.getSetting( "VideoFromat" ) 
	vformatid=len(match)-1
        if vformat=="0":
		vformatid=0
	elif vformat=="1":
		vformatid=1
	elif vformat=="2":
		vformatid=2
        if vformatid>len(match)-1:
		vformatid=len(match)-1
        newurl=match[vformatid][0];
	print vformatid
	newurl='http://'+newurl;
        playlist = xbmc.PlayList(1)
	playlist.clear()
	listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
	listitem.setInfo("Video", {"Title":''})
	listitem.setProperty('IsPlayable', 'true')
	print newurl
	playlist.add(newurl,listitem)
	xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
	xbmcPlayer.play(playlist)
	exit()

def m_array_index(arr, searchItem):
    for i,x in enumerate(arr):
        for j,y in enumerate(x):
            if y == searchItem:
                return i
    return -1

def decodeURL(movieurl):
	UnEncrypKey="001000003100000000000030000020011200000000200000310000";
	indexer=0;
	newurl="";
	magicCode = int(movieurl[len(movieurl)-4:len(movieurl)],10);
	movieurl=movieurl[0:len(movieurl)-4];
        var7=0;
	while indexer<len(movieurl):
		var7=var7+2;
		currentChar = movieurl[indexer:indexer+4];
		currentChar = int(currentChar,16);
		currentChar = (currentChar - magicCode - (var7*var7) -16)/3
		currentChar=currentChar-int(UnEncrypKey[((indexer/4) % len(UnEncrypKey))],10);
		if currentChar>0:
			newurl=newurl+chr(currentChar)
		else:
			indexer=len(movieurl);
		indexer=indexer+4;
	return newurl;


def CheckForNextPage(page):
    xbmc.executebuiltin('Container.SetViewMode(500)')
    if '">Next</a>' in page:
        try:
            NextPage=page.split('">Next</a>')[0].split('href="')[-1].split('"')[0]
            if len(NextPage) > 0:
                addDir2("Next Page",NextPage,mode,artpath+'nextpage.png','',fanart) 
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
               
def addDir2(name,url,mode,iconimage,description,fanart):
        xbmc.executebuiltin('Container.SetViewMode(500)')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
 
 
def addDir(name,url,mode,iconimage,isFolder=True):
        xbmc.executebuiltin('Container.SetViewMode(500)')
        splitName=name.partition('(')
	simplename=""
	simpleyear=""
	if len(splitName)>0:
		simplename=splitName[0]
		simpleyear=splitName[2].partition(')')
		if len(simpleyear)>0:
			simpleyear=simpleyear[0]
        meta = metaget.get_meta('movie', simplename ,simpleyear)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels= meta )
        contextMenuItems = []
        contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
        else: liz.setProperty('fanart_image', fanart)
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
print params

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: GETMOVIES(url)
elif mode==2: GENRES(url)
elif mode==3: YEARS(url)
elif mode==4: AZ(url)
elif mode==5: SEARCH()
elif mode==100: VIDEOLINKS(url,name)
elif mode==200: PLAYLINK(name,url)
elif mode==400: PLAYLINKMainServer(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
