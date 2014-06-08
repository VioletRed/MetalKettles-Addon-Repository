import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,simplejson,os,socket,ssl
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
from metahandler import metahandlers
import decrypter

#socket.setdefaulttimeout(15) 
addon_id = 'plugin.video.putlocker'
selfAddon = xbmcaddon.Addon(id=addon_id)
metaget = metahandlers.MetaData(preparezip=False)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.PNG'))
artpath = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))
xbmc.executebuiltin('Container.SetViewMode(50)')

def CATEGORIES():
        addCat('Featured','http://putlocker.is/featured/1',1,artpath+'movies.png','',fanart)
        addCat('Genres','url',2,artpath+'genres.png','',fanart)
        addCat('Years','url',3,artpath+'year2.png','',fanart)
        addCat('A - Z','url',4,artpath+'alphabet.png','',fanart)
        addCat('Search','url',5,artpath+'search.png','',fanart)
        xbmc.executebuiltin('Container.SetViewMode(50)')

def GETMOVIES(url,name):
        print name
        name2=name
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('td width="20%" valign="top" style="padding-top: 5px; padding-left: 5px; padding-right: 5px;padding-bottom: 10px;"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" ').findall(link)
        inc = 1
        for url,name,thumb in match:
                if name2 == 'Featured':
                        addDir(name,url,400,thumb,len(match),isFolder=False)
                else:
                        if inc > 5:
                                addDir(name,url,400,thumb,len(match),isFolder=False)
                        inc = inc + 1
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin('Container.SetViewMode(50)')
        CheckForNextPage(link)
        
def GENRES(url):
        addCat('Action','http://putlocker.is/genre/action/1',1,artpath+'action.png','',fanart)
        addCat('Adventure','http://putlocker.is/genre/adventure/1',1,artpath+'adventure.png','',fanart)
        addCat('Animation','http://putlocker.is/genre/animation/1',1,artpath+'animation.png','',fanart)
        addCat('Biography','http://putlocker.is/genre/biography/1',1,artpath+'biography.png','',fanart)
        addCat('Comedy','http://putlocker.is/genre/comedy/1',1,artpath+'comedy.png','',fanart)
        addCat('Crime','http://putlocker.is/genre/crime/1',1,artpath+'crime.png','',fanart)
        addCat('Documentary','http://putlocker.is/genre/documentary/1',1,artpath+'documentary.png','',fanart)
        addCat('Drama','http://putlocker.is/genre/drama/1',1,artpath+'drama.png','',fanart)
        addCat('Family','http://putlocker.is/genre/family/1',1,artpath+'family.png','',fanart)
        addCat('Fantasy','http://putlocker.is/genre/fantasy/1',1,artpath+'fantasy.png','',fanart)
        addCat('History','http://putlocker.is/genre/history/1',1,artpath+'history.png','',fanart)
        addCat('Horror','http://putlocker.is/genre/horror/1',1,artpath+'horror.png','',fanart)
        addCat('Musical','http://putlocker.is/genre/musical/1',1,artpath+'musical.png','',fanart)
        addCat('Mystery','http://putlocker.is/genre/mystery/1',1,artpath+'mystery.png','',fanart)
        addCat('Romance','http://putlocker.is/genre/romance/1',1,artpath+'romance.png','',fanart)
        addCat('Sci-Fi','http://putlocker.is/genre/sci-fi/1',1,artpath+'sci-fi.png','',fanart)
        addCat('Sport','http://putlocker.is/genre/sport/1',1,artpath+'sport.png','',fanart)
        addCat('Thriller','http://putlocker.is/genre/thriller/1',1,artpath+'thriller.png','',fanart)
        addCat('War','http://putlocker.is/genre/war/1',1,artpath+'war.png','',fanart)
        addCat('Western','http://putlocker.is/genre/western/1',1,artpath+'western.png','',fanart)
        xbmc.executebuiltin('Container.SetViewMode(50)')
 
def YEARS(url):
        addCat('2014','http://putlocker.is/year/2014/1',1,artpath+'year2.png','',fanart)
        addCat('2013','http://putlocker.is/year/2013/1',1,artpath+'year2.png','',fanart)
        addCat('2012','http://putlocker.is/year/2012/1',1,artpath+'year2.png','',fanart)
        addCat('2011','http://putlocker.is/year/2011/1',1,artpath+'year2.png','',fanart)
        addCat('2010','http://putlocker.is/year/2010/1',1,artpath+'year2.png','',fanart)
        addCat('2009','http://putlocker.is/year/2009/1',1,artpath+'year2.png','',fanart)
        addCat('2008','http://putlocker.is/year/2008/1',1,artpath+'year2.png','',fanart)
        addCat('2007','http://putlocker.is/year/2007/1',1,artpath+'year2.png','',fanart)
        addCat('2006','http://putlocker.is/year/2006/1',1,artpath+'year2.png','',fanart)
        addCat('2005','http://putlocker.is/year/2005/1',1,artpath+'year2.png','',fanart)
        addCat('2004','http://putlocker.is/year/2004/1',1,artpath+'year2.png','',fanart)
        addCat('2003','http://putlocker.is/year/2003/1',1,artpath+'year2.png','',fanart)
        addCat('2002','http://putlocker.is/year/2002/1',1,artpath+'year2.png','',fanart)
        addCat('2001','http://putlocker.is/year/2001/1',1,artpath+'year2.png','',fanart)
        addCat('2000','http://putlocker.is/year/2000/1',1,artpath+'year2.png','',fanart)
        addCat('1999','http://putlocker.is/year/1999/1',1,artpath+'year2.png','',fanart)
        addCat('1998','http://putlocker.is/year/1998/1',1,artpath+'year2.png','',fanart)
        addCat('1997','http://putlocker.is/year/1997/1',1,artpath+'year2.png','',fanart)
        addCat('1996','http://putlocker.is/year/1996/1',1,artpath+'year2.png','',fanart)
        addCat('1995','http://putlocker.is/year/1995/1',1,artpath+'year2.png','',fanart)
        addCat('1994','http://putlocker.is/year/1994/1',1,artpath+'year2.png','',fanart)
        addCat('1993','http://putlocker.is/year/1993/1',1,artpath+'year2.png','',fanart)
        xbmc.executebuiltin('Container.SetViewMode(50)')
 
def AZ(url):
        AZurl = ('http://putlocker.is/a-z/')
        req = urllib2.Request(AZurl)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        azlist=re.compile('<a href="(.+?)" title="(.+?)" style="text-decoration:none;').findall(link)
        for url,name in azlist:
                name2 = name.split(' ',1)
                if name2[0]=='0-9': name2[0]='num'
                addCat(name,url,1,artpath+name2[0]+'.png','',fanart)
        xbmc.executebuiltin('Container.SetViewMode(50)')
        
def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Putlocker.is')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if search_entered == None or len(search_entered)<1:
        end()
    else:
        url = 'http://putlocker.is/search/search.php?q=%s'%(search_entered)
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    match=re.compile('td width="20%" valign="top" style="padding-top: 5px; padding-left: 5px; padding-right: 5px;padding-bottom: 10px;"><a href="(.+?)" title="(.+?)"><img src="(.+?)" border="0" ').findall(link)
    inc = 0
    for url,name,thumb in match:
                        if inc > 4:        
                            addDir(name,url,400,thumb,len(match),isFolder=False)
                        inc+=1
    xbmc.executebuiltin('Container.SetViewMode(50)')
    
def PLAYLINKMainServer(name,url):
        req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()

	try:
                match=re.compile('plugins=http://static1.movsharing.com/plugin.+?/proxy.swf&proxy.link=movs*(.+?)&').findall(link)
                match = match[0].replace('*','') 
                s= decrypter.decrypter(192,128)
                uncode = s.decrypt(match,'u3332bcCRs2DvUf17rqq','ECB').split('\0')[0]
                req = urllib2.Request(uncode)
                req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('"file":"(.+?)",').findall(link)
                newurl = match[0].replace ('\/','/')
                playlist = xbmc.PlayList(1)
                playlist.clear()
                listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
                listitem.setInfo("Video", {"Title":name})
                listitem.setProperty('mimetype', 'video/x-msvideo')
                listitem.setProperty('IsPlayable', 'true')
                playlist.add(newurl,listitem)
                xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
                xbmcPlayer.play(playlist)
        except:
                match=re.compile('<a rel="nofollow" href="(.+?)" title=').findall(link)
                newurl = match[0]
                print newurl
                resolved_url = urlresolver.HostedMediaFile(newurl).resolve()
                playlist = xbmc.PlayList(1)
                playlist.clear()
                listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
                listitem.setInfo("Video", {"Title":name})
                listitem.setProperty('mimetype', 'video/x-msvideo')
                listitem.setProperty('IsPlayable', 'true')
                playlist.add(resolved_url,listitem)
                xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
                xbmcPlayer.play(playlist)
    
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")

def CheckForNextPage(page):
    if '">Next</a>' in page:
        try:
            NextPage=page.split('">Next</a>')[0].split('href="')[-1].split('"')[0]
            if len(NextPage) > 0:
                addCat("Next Page",NextPage,mode,artpath+'nextpage.png','',fanart) 
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
               
def addCat(name,url,mode,iconimage,description,fanart):
        xbmc.executebuiltin('Container.SetViewMode(50)')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        xbmc.executebuiltin('Container.SetViewMode(50)')
        return ok
 
 
def addDir(name,url,mode,iconimage,itemcount,isFolder=True):
        xbmc.executebuiltin('Container.SetViewMode(50)')
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
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
        xbmc.executebuiltin('Container.SetViewMode(50)')
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
elif mode==1: GETMOVIES(url,name)
elif mode==2: GENRES(url)
elif mode==3: YEARS(url)
elif mode==4: AZ(url)
elif mode==5: SEARCH()
elif mode==400: PLAYLINKMainServer(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
