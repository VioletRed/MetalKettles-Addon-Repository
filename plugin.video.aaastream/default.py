# -*- coding: utf-8 -*-
aaastreamversion = "aaastream Version 1.9.1"
import urllib, sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, time, base64
import re,urllib2
import xbmcplugin,random,urlparse,urlresolver
from t0mm0.common.addon import Addon
from metahandler import metahandlers
from addon.common.net import Net

PlaylistUrl = "http://aaastream.com"
AddonID = 'plugin.video.aaastream'
Addon = xbmcaddon.Addon(AddonID)
localizedString = Addon.getLocalizedString
localisedTranslate = 'aHR0cDovL2tvZGkueHl6L2RpcmVjdC5waHA='
localisedMoLink = 'aHR0cDovL2tvZGkueHl6L21vdmllcy5waHA='
LocalisedLa = 'aHR0cDovL3d3dy5tb3ZpZTI1LmxhLw=='
Playdp = 5
net = Net()
AddonName = Addon.getAddonInfo("name")
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.aaastream/fanart.jpg'))
artpath = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.aaastream/resources/art/'))
icon = Addon.getAddonInfo('icon')
addonDir = Addon.getAddonInfo('path').decode("utf-8")
LibCommon = len(PlaylistUrl)
libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
import common
TodaysDate = str(time.strftime ('%y/%m/%d'))
#xbmcgui.Dialog().ok(str(), '') 
metaget = metahandlers.MetaData(preparezip=False)
metaset = 'true'
custurl1 = str(base64.decodestring(LocalisedLa))

 
addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ).decode("utf-8"), AddonID)
if not os.path.exists(addon_data_dir):
	os.makedirs(addon_data_dir)
	
	
playlistsFile = os.path.join(addonDir, "playLists.txt")
tmpListFile = os.path.join(addonDir, 'tempList.txt')
favoritesFile = os.path.join(addonDir, 'favorites.txt')
if  not (os.path.isfile(favoritesFile)):
	f = open(favoritesFile, 'w') 
	f.write('[]') 
	f.close() 

# husham cant code for sh*t lol! 
def Categories():
    Playdp = str(len(PlaylistUrl))
    url = base64.decodestring(localisedTranslate)
    AddDir("[COLOR white][B] CLICK HERE TO UPDATE AAA STREAM[/B][/COLOR]", "Update" ,50,os.path.join(addonDir, "resources", "images", "update-icon.png"))
    AddDir("[COLOR white][B] YOUR FAVOURITE CHANNELS HERE[/B][/COLOR]", "favorites" ,30 ,os.path.join("http://www.iconarchive.com/download/i6066/custom-icon-design/pretty-office-3/add-to-favorites.ico"))   
    AddDir("[COLOR yellow][B] AAASTREAM MOVIES[/B][/COLOR]",'movies',44 ,"http://s5.postimg.org/ycy0pxt9j/appmovies.jpg")
    AddDir("[COLOR yellow][B] AAASTREAM TV SHOWS[/B] (SOON)[/COLOR]",'TV',0 ,"http://s5.postimg.org/ycy0pxt9j/appmovies.jpg")    
    AddDir("[COLOR yellow]This is Version 1.9.1[/COLOR]", "Update" ,99 ,"http://s5.postimg.org/9469649rb/appgraphic.jpg")
    
    playlistsFile = os.path.join(addonDir,"playLists.txt")
    DownloaderClass(url,playlistsFile)
	
    list = common.ReadList(playlistsFile)
    for item in list:
		mode = int(Playdp) + 26 if item["url"].find("youtube") > 0 else 2
		name = common.GetEncodeString(item["name"])
		AddDir("[COLOR blue]{0}[/COLOR]".format(name) ,item["url"], mode, "http://s5.postimg.org/9469649rb/appgraphic.jpg")

#aaastream New security key U1R1A6P4R9I3C1K
def MOVIES():
        AddDir("[COLOR white][B] YOUR FAVOURITE CHANNELS HERE[/B][/COLOR]", "favorites" ,30 ,os.path.join("http://www.iconarchive.com/download/i6066/custom-icon-design/pretty-office-3/add-to-favorites.ico")) 
        AddDir("[COLOR yellow][B]AAASTREAM Movies[/B][/COLOR]",str(base64.decodestring(localisedMoLink)),43 ,"http://s5.postimg.org/ycy0pxt9j/appmovies.jpg")
        AddDir('[COLOR yellow][B]Top 9[/B][/COLOR]',custurl1,51,"http://s5.postimg.org/ycy0pxt9j/appmovies.jpg")
        AddDir('[COLOR yellow][B]Featured[/B][/COLOR]',custurl1+'featured-movies/',52,"http://s5.postimg.org/ycy0pxt9j/appmovies.jpg")
        AddDir('[COLOR yellow][B]New Releases[/B][/COLOR]',custurl1+'new-releases/',52,"http://s5.postimg.org/ycy0pxt9j/appmovies.jpg")
        AddDir('[COLOR yellow][B]Latest Added[/B][/COLOR]',custurl1+'latest-added/',52,"http://s5.postimg.org/ycy0pxt9j/appmovies.jpg")
        AddDir('[COLOR yellow][B]Latest HD[/B][/COLOR]',custurl1+'latest-hd-movies/',52,"http://s5.postimg.org/ycy0pxt9j/appmovies.jpg")
        AddDir('[COLOR yellow][B]Most Viewed[/B][/COLOR]',custurl1+'most-viewed/',52,"http://s5.postimg.org/ycy0pxt9j/appmovies.jpg")
        
		
def DownloaderClass(url,dest):
    dp = xbmcgui.DialogProgress()
    dp.create("AAA Stream","Downloading")
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
 
def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        print percent
        dp.update(percent)
    except:
        percent = 100
        dp.update(percent)
    if dp.iscanceled(): 
        print "DOWNLOAD CANCELLED" # need to get this part working
        dp.close()

def TOP9(url):
#        xbmcgui.Dialog().ok(str(url), '') 
        EnableMeta = metaset
        match=re.compile('<div class=pic_top_movie><a href="(.+?)" title=".+?"><img src=".+?" alt="(.+?)\(([\d]{4})\)"',re.DOTALL).findall(net.http_GET(url).content)
        for url,name,icon in match:
                name = CLEAN(name)
                AddDir(name,custurl1+url,66,icon)

def INDEX(url):
        links = net.http_GET(url).content
        links=links.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        match=re.compile(str(base64.decodestring('PGRpdiBjbGFzcz0ibW92aWVfcGljIj48YSBocmVmPSIoLis/KSIgIHRhcmdldD0iX3NlbGYiIHRpdGxlPSIoLis/KSI+KC4rPyk8aW1nIHNyYz0iKC4rPykiIHdpZHRoPSIxMzAiIGhlaWdodD0iMTkwIiBhbHQ9IiguKz8pcmVwZWF0LXg7Ij48L2xpPg==')),re.DOTALL).findall(links)
        nextpage=re.compile('<font color=\'#FF3300\'>.+?</font>&nbsp;<a href=\'(.+?)\' >.+?</a>').findall(links)
        for url,name,iconimage2,iconimage3,iconimage4 in match:
                name = CLEAN(name)
                AddDir(name,custurl1+url,66,iconimage2)


        if nextpage:
                print nextpage
                url = str(nextpage)
                print url
                url = url.replace('[u\'','')
                url = url.replace(']','')
                url = url.replace('\'','')
                print url
                AddDir('[B][COLOR yellow]Next Page >>>[/COLOR][/B]',custurl1+url,52,'')



def VIDEOLINKS(name,url):
#       xbmcgui.Dialog().ok(str(url), url)
        EnableMeta = metaset
        iconimage = ''
        name2 = name
        links2 = net.http_GET(url).content
        links2 = links2.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('\'','')
				  
        match2=re.compile('<h1 >Links - Quality(.+?)</h1>').findall(links2)
        match=re.compile('<li id="playing_button" onclick="go_to((.+?),(.+?));" class="').findall(links2)
        if match2:
                quality = str(match2).replace('[','').replace(']','').replace("'",'').replace(' ','').replace('u','')
        else:
                quality = 'Not Specified'
        List=[]; ListU=[]; c=0
        for blank3,name,url in match:
                url = url.replace(')','')
                c=c+1; List.append('Link ['+str(c)+'] '); ListU.append(url)
        dialog=xbmcgui.Dialog()
        rNo=dialog.select('AAA STREAM Select A Host Quality = %s'%quality, List)
        if rNo>=0:
                rName=List[rNo]
                rURL=ListU[rNo]
#                PLAYLINK(name2,rURL,'')
                STREAM(name2,rURL,'')
        else:
                pass

def STREAM(name,url,thumb):
        name2 = name
        url2 = url
        print url2
        try:
                req = urllib2.Request(url2)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                streamlink = urlresolver.resolve(urllib2.urlopen(req).url)
                addLinkMovies(name2,streamlink,thumb)
        except:
                Notify('small','Sorry Link Removed:', 'Please try another one.',9000)

      
def addLinkMovies(name,url,iconimage):
        download_enabled = 'False'
        print url
        ok=True
        try: addon.resolve_url(streamlink)
        except: pass
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo('Video', infoLabels={ "Title": name } )
        ###Download Context Menu
        contextMenuItems = []
        if download_enabled == 'true':
                contextMenuItems = []
                contextMenuItems.append(('Download', 'XBMC.RunPlugin(%s?mode=9&name=%s&url=%s)' % (sys.argv[0], name, urllib.quote_plus(url))))
                liz.addContextMenuItems(contextMenuItems, replaceItems=True)
                ########################
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok
		
def AddDirMovies(name,url,mode,iconimage,types,year):
        ok=True
        type = types
        fimg = fanart

        infoLabels = {'title':name}
        try: img = infoLabels['cover_url']
        except: img = iconimage
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=img)
        liz.setInfo( type="Video", infoLabels= infoLabels)
        liz.setProperty( "Fanart_Image", fimg )
        ###Add to Library and Favorites Context Menu
        contextMenuItems = []
        if mode == 2:
                contextMenuItems = []
                contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
                
                contextMenuItems.append(('Add to Library', 'XBMC.RunPlugin(%s?mode=10&name=%s&url=%s)' % (sys.argv[0], name, urllib.quote_plus(url))))
        
                contextMenuItems.append(('Add to Favorites', 'XBMC.RunPlugin(%s?mode=14&name=%s&url=%s&year=%s)' % (sys.argv[0], name, urllib.quote_plus(url), year)))

                contextMenuItems.append(('Add to Kid Movies', 'XBMC.RunPlugin(%s?mode=47&name=%s&url=%s&year=%s)' % (sys.argv[0], name, urllib.quote_plus(url), year)))
                liz.addContextMenuItems(contextMenuItems, replaceItems=False)

        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        if mode == 20000:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
                ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def Notify(typeq,title,message,times, line2='', line3=''):
     if typeq == 'small':
            smallicon= "http://s5.postimg.org/ycy0pxt9j/appmovies.jpg"
            xbmc.executebuiltin("XBMC.Notification("+title+","+message+","''","+smallicon+")")
     elif typeq == 'big':
            dialog = xbmcgui.Dialog()
            dialog.ok(' '+title+' ', ' '+message+' ', line2, line3)
     else:
            dialog = xbmcgui.Dialog()
            dialog.ok(' '+title+' ', ' '+message+' ')
			
def CLEAN(name):
        name = name.replace('&amp;','&')
        name = name.replace('&#x27;',"'")
        urllib.quote(u'\xe9'.encode('UTF-8'))
        name = name.replace(u'\xe9','e')
        urllib.quote(u'\xfa'.encode('UTF-8'))
        name = name.replace(u'\xfa','u')
        urllib.quote(u'\xed'.encode('UTF-8'))
        name = name.replace(u'\xed','i')
        urllib.quote(u'\xe4'.encode('UTF-8'))
        name = name.replace(u'\xe4','a')
        urllib.quote(u'\xf4'.encode('UTF-8'))
        name = name.replace(u'\xf4','o')
        urllib.quote(u'\u2013'.encode('UTF-8'))
        name = name.replace(u'\u2013','-')
        urllib.quote(u'\xe0'.encode('UTF-8'))
        name = name.replace(u'\xe0','a')
        try: name=messupText(name,True,True)
        except: pass
        try:name = name.decode('UTF-8').encode('UTF-8','ignore')
        except: pass
        return name
		
def AddNewList():
	listName = GetKeyboardText(localizedString(10004).encode('utf-8')).strip()
	if len(listName) < 1:
		return

	method = GetSourceLocation(localizedString(10002).encode('utf-8'), [localizedString(10016).encode('utf-8'), localizedString(10017).encode('utf-8')])	
	#print method
	if method == -1:
		return
	elif method == 0:
		listUrl = GetKeyboardText(localizedString(10005).encode('utf-8')).strip()
	else:
		listUrl = xbmcgui.Dialog().browse(int(1), localizedString(10006).encode('utf-8'), 'myprograms','.plx|.m3u').decode("utf-8")
		if not listUrl:
			return
	
	if len(listUrl) < 1:
		return

	list = common.ReadList(playlistsFile)
	for item in list:
		if item["url"].lower() == listUrl.lower():
			xbmc.executebuiltin('Notification({0}, "{1}" {2}, 5000, {3})'.format(AddonName, listName, localizedString(10007).encode('utf-8'), icon))
			return
	list.append({"name": listName.decode("utf-8"), "url": listUrl})
	if common.SaveList(playlistsFile, list):
		xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}')".format(AddonID))
	
def RemoveFromLists(url):
	list = common.ReadList(playlistsFile)
	for item in list:
		if item["url"].lower() == url.lower():
			list.remove(item)
			if common.SaveList(playlistsFile, list):
				xbmc.executebuiltin("XBMC.Container.Refresh()")
			break

def PLAYLINK(name,url,iconimage):
        link = common.OpenURL(url)
        match=re.compile('hashkey=(.+?)">').findall(link)
        if len(match) == 0:
                match=re.compile("hashkey=(.+?)'>").findall(link)
        if (len(match) > 0):
                hashurl="http://videomega.tv/validatehash.php?hashkey="+ match[0]
                req = urllib2.Request(hashurl,None)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:34.0) Gecko/20100101 Firefox/34.0')
                req.add_header('Referer', url)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                match=re.compile('var ref="(.+?)"').findall(link)[0]
                videomega_url = 'http://videomega.tv/?ref='+match 
        else:
                match=re.compile("javascript'\>ref='(.+?)'").findall(link)[0]
                videomega_url = "http://videomega.tv/?ref=" + match
                
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
        url = re.compile('document.write.unescape."(.+?)"').findall(link)[-1]
        url = urllib.unquote_plus(url)
        print url
        stream_url = re.compile('file *: *"(.+?)"').findall(url)[0]
 # CHECK AAASTREAM SECURITY KEY      
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
		
def PlxCategory(url):
	tmpList = []
	list = common.plx2list(url)
	Playdp = str(len(PlaylistUrl))
	background = list[0]["background"]
	for channel in list[1:]:
		iconimage = "" if not channel.has_key("thumb") else common.GetEncodeString(channel["thumb"])
		name = common.GetEncodeString(channel["name"])
		if channel["type"] == 'playlist':
			AddDir("[COLOR blue][{0}][/COLOR]".format(name) ,channel["url"], 1, iconimage, background=background)
		else:
			AddDir(name, channel["url"], 3, iconimage, isFolder=False, background=background)
			tmpList.append({"url": channel["url"], "image": iconimage, "name": name.decode("utf-8")})
			
	common.SaveList(tmpListFile, tmpList)
			
		
def PlayUrl(name, url, iconimage=None):
	print '--- Playing "{0}". {1}'.format(name, url)
	listitem = xbmcgui.ListItem(path=url, thumbnailImage=iconimage)
	listitem.setInfo(type="Video", infoLabels={ "Title": name })
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def AddDir(name, url, mode, iconimage, description="", isFolder=True, background=None):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)

	liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": description})
	if background:
		liz.setProperty('fanart_image', background)
	if mode == 1 or mode == 2:
		liz.addContextMenuItems(items = [('{0}'.format(localizedString(10008).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=22)'.format(sys.argv[0], urllib.quote_plus(url)))])
	elif mode == 3:
		liz.setProperty('IsPlayable', 'true')
		liz.addContextMenuItems(items = [('{0}'.format(localizedString(10009).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, name))])
	elif mode == 32:
		liz.setProperty('IsPlayable', 'true')
		liz.addContextMenuItems(items = [('{0}'.format(localizedString(10010).encode('utf-8')), 'XBMC.RunPlugin({0}?url={1}&mode=33&iconimage={2}&name={3})'.format(sys.argv[0], urllib.quote_plus(url), iconimage, name))])
		
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def GetKeyboardText(title = "", defaultText = ""):
	keyboard = xbmc.Keyboard(defaultText, title)
	keyboard.doModal()
	text =  "" if not keyboard.isConfirmed() else keyboard.getText()
	return text

def GetSourceLocation(title, list):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, list)
	return answer
	
def AddFavorites(url, iconimage, name):
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == url.lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, localizedString(10011).encode('utf-8'), icon))
			return
    
	list = common.ReadList(tmpListFile)	
	for channel in list:
		if channel["name"].lower() == name.lower():
			url = channel["url"]
			iconimage = channel["image"]
			break
			
	if not iconimage:
		iconimage = ""
		
	data = {"url": url, "image": iconimage, "name": name.decode("utf-8")}
	
	favList.append(data)
	common.SaveList(favoritesFile, favList)
	xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, localizedString(10012).encode('utf-8'), icon))

def GETMOVIES(url,name):
        link = common.OpenURL(url)
        match=re.compile('href="(.+?)" title="(.+?)">').findall(link)
        items = len(match)
        for url,name in match:
                name2 = AAASTREAM_CODE(name)
                AAASTREAM_Dir(name2,url,100,'',len(match))
        try:
                match=re.compile('"nextLink":"(.+?)"').findall(link)
                url= match[0]
                url = url.replace('\/','/')
                AAASTREAM_Dir('Next Page>>',url,1,artpath+'nextpage.png',items,isFolder=True)
        except: pass
        if metaset=='true':
                setView('movies', 'MAIN')
        else: xbmc.executebuiltin('Container.SetViewMode(50)')

def AAASTREAM_CODE(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
	

def AAASTREAM_Dir(name,url,mode,iconimage,itemcount,isFolder=False):
        if metaset=='true' and LibCommon == 20:
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
            liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels= meta )
            contextMenuItems = []
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            liz.addContextMenuItems(contextMenuItems, replaceItems=True)
            if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
            else: liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
            return ok
        else:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
            return ok
			
def UpdateMe():
    url = "http://kodi.xyz/updateaaa.php"
    localfile = os.path.join(addonDir,"default.py")
    urllib.urlretrieve(url,localfile)
    url = "http://kodi.xyz/updateaddon.php"
    localfile = os.path.join(addonDir,"addon.xml")
    urllib.urlretrieve(url,localfile)
    url = "http://kodi.xyz/updatecommon.php"
    localfile = os.path.join(libDir,"common.py")
    urllib.urlretrieve(url,localfile)
    AddDir("[COLOR white][B][{0}][/B][/COLOR]".format(localizedString(10019).encode('utf-8')), "Updated" ,99 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"))

def RemoveFavorties(url):
	list = common.ReadList(favoritesFile) 
	for channel in list:
		if channel["url"].lower() == url.lower():
			list.remove(channel)
			break
			
	common.SaveList(favoritesFile, list)
	xbmc.executebuiltin("XBMC.Container.Refresh()")

def m3uCategory(url):	
	tmpList = []
	list = common.m3u2list(url)

	for channel in list:
		name = common.GetEncodeString(channel["display_name"])
		mode = LibCommon + 26 if channel["url"].find("youtube") > 0 else 3
		AddDir(name ,channel["url"], mode, "", isFolder=False)
		tmpList.append({"url": channel["url"], "image": "", "name": name.decode("utf-8")})

	common.SaveList(tmpListFile, tmpList)

def ListFavorites():
	AddDir("[COLOR yellow][B]{0}[/B][/COLOR]".format(localizedString(10013).encode('utf-8')), "favorites" ,34 ,os.path.join(addonDir, "resources", "images", "bright_yellow_star.png"), isFolder=False)
	list = common.ReadList(favoritesFile)
	for channel in list:
		name = channel["name"].encode("utf-8")
		iconimage = channel["image"].encode("utf-8")
		AddDir(name, channel["url"], 32, iconimage, isFolder=False) 

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)

    xbmc.executebuiltin("Container.SetViewMode(true)")		
	
def AddNewFavortie():
	chName = GetKeyboardText("{0}".format(localizedString(10014).encode('utf-8'))).strip()
	if len(chName) < 1:
		return
	chUrl = GetKeyboardText("{0}".format(localizedString(10015).encode('utf-8'))).strip()
	if len(chUrl) < 1:
		return
		
	favList = common.ReadList(favoritesFile)
	for item in favList:
		if item["url"].lower() == url.lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, localizedString(10011).encode('utf-8'), icon))
			return
			
	data = {"url": chUrl, "image": "", "name": chName.decode("utf-8")}
	
	favList.append(data)
	if common.SaveList(favoritesFile, favList):
		xbmc.executebuiltin("XBMC.Container.Update('plugin://{0}?mode=30&url=favorites')".format(AddonID))

def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring) >= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?','')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0].lower()] = splitparams[1]
	return param

	
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass
try:        
	mode = int(params["mode"])
except:
	pass
try:        
	description = urllib.unquote_plus(params["description"])
except:
	pass

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

	
if mode == None or url == None or len(url) < 1:
	Categories()
elif mode == 1:
	PlxCategory(url)
elif mode == 2:
	m3uCategory(url)
elif mode == 3 or mode == 32:
	PlayUrl(name, url, iconimage)
elif mode == 46 and len(url) > 21:
     xbmc.executebuiltin(url)

elif mode == 22:
	RemoveFromLists(url)
elif mode == 50:
	UpdateMe()
elif mode == 31: 
	AddFavorites(url, iconimage, name) 
elif mode == 33:
	RemoveFavorties(url)
elif mode == 34:
	AddNewFavortie()
elif mode == 40:
	common.DelFile(playlistsFile)
	sys.exit()
elif mode == 41:
	common.DelFile(favoritesFile)
elif mode == 43:
	GETMOVIES(url,'Featured')
elif mode == 44:
	MOVIES()
elif mode == 30:
	ListFavorites()
elif mode == 51:	
	TOP9(url)
elif mode == 52:	
	INDEX(url)
elif mode == 66:	
	VIDEOLINKS(name,url)
elif mode == 99:
	Categories()
elif mode == 100 and LibCommon == 20:	
	PLAYLINK(name,url,iconimage)

xbmcplugin.endOfDirectory(int(sys.argv[1]))