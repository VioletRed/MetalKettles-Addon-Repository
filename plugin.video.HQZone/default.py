#-*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon, xbmcplugin, urllib, re, string, os, time
from t0mm0.common.net import Net as net

#HQ Zone - Original Coding by Mash2k3 All credit to MASH2k3 - XBMC Standalone Addon By mFuk.

addon_id 	= 'plugin.video.HQZone'
local 		= xbmcaddon.Addon(id=addon_id)
hqzonepath 	= local.getAddonInfo('path')
art 		= hqzonepath+'/images'
selfAddon 	= xbmcaddon.Addon(id=addon_id)
prettyName	= 'HQZone'
user 		= selfAddon.getSetting('hqusername')
passw 		= selfAddon.getSetting('hqpassword')
datapath 	= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
cookie_file = os.path.join(os.path.join(datapath,'Cookies'), 'hqzone.cookies')
Dir 		= xbmc.translatePath(os.path.join('special://home/addons/plugin.video.HQZone', ''))
fanartimage	= Dir+'fanart.jpg'
mashpath 	= selfAddon.getAddonInfo('path')
fav 		= False

#set paths
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
            search = keyb.getText()
            username=search
            keyb = xbmc.Keyboard('', 'Enter Password:')
            keyb.doModal()
            if (keyb.isConfirmed()):
                search = keyb.getText()
                password=search
                selfAddon.setSetting('hqusername',username)
                selfAddon.setSetting('hqpassword',password)
#		setCookie('http://www.hqzone.tv/forums/view.php?pg=live')

def addDir(name,url,mode,iconimage,plot='',fanart='',index=False):
    return addDirX(name,url,mode,iconimage,plot,fanart,addToFavs=0,replaceItems=False,index=index)

def addLink(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage=art+'/link.png', thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image', fanartimage)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)	

def addPlayL(name,url,mode,iconimage,plot,fanart,dur,genre,year,secName='',secIcon=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)
    surl=urllib.quote_plus(u)
    dname=removeColoredText(name)
    mi=[('Add to [COLOR=FFa11d21][B]ONTapp.tv[/B][/COLOR]', 'XBMC.RunPlugin(%s?mode=1501&plot=%s&name=%s&url=%s&iconimage=%s)' % (sys.argv[0] ,secName,dname,surl, secIcon))]
    return addDirX(name,url,mode,iconimage,plot,fanart,dur,genre,year,isFolder=0)

def VIEWSB():
    if selfAddon.getSetting("auto-view") == "true":
        if selfAddon.getSetting("home-view") == "0":
                xbmc.executebuiltin("Container.SetViewMode(50)")
        elif selfAddon.getSetting("home-view") == "1":
                xbmc.executebuiltin("Container.SetViewMode(50)")
        return

def removeColoredText(text):
    return re.sub('\[COLOR.*?\[/COLOR\]','',text,re.I|re.DOTALL).strip()
	
def MAIN():
    setCookie('http://www.hqzone.tv/forums/view.php?pg=live')
    response = net().http_GET('http://www.hqzone.tv/forums/view.php?pg=live')
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    addDir('[COLOR green]View Schedule[/COLOR]','http://www.hqzone.tv/forums/calendar.php?c=1&do=displayweek',6,art+'/hqzone.png')
    match=re.findall('(?sim)<h4 class="panel_headin.+?">([^<]+?)</h4><ul>(.+?)</ul>',link)
    for name,links in match[0:3]:
        if 'Channels' == name:
            name='V.I.P Member Streams'
        addDir(name,links,2,art+'/hqzone.png') #Main Channels
#    addLink('[COLOR red]VOD[/COLOR]','','') #Video On Demand
    match=re.findall('(?sim)<h4 class="panel_headin.+?">([^<]+?)</h4><ul>(.+?)</ul>',link)
    for name,links in match[3:]:
        if 'Channels' == name:
            name='V.I.P Member Streams'
        addDir(name,links,4,art+'/hqzone.png') #VIP
 
def LISTMENU(murl):
    match=re.findall('(?sim)<li><a href="([^"]+?)" target="I1">([^<]+?)</a></li>',murl)
    if not match:
        match=re.findall('(?sim)<a href="([^"]+?)" target="I1"><img src="([^"]+?)"',murl)
    for url,name in match:
        url = 'http://www.hqzone.tv/forums/'+url
        addPlayL(name,url,5,'','','','','','')
 
 #Display the VOD TV section
def LISTMENU2(murl):
    match=re.findall('(?sim)<li><a href="([^"]+?)" target="I1">([^<]+?)</a></li>',murl)
    for url,name in match:
        url = 'http://www.hqzone.tv/forums/'+url
        addDir(name,url,3,art+'/hqzone.png') #default image for VOD section
 
def LISTCONTENT(murl,thumb):
    setCookie(murl)
    response = net().http_GET(murl)
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.findall('(?sim)sources: \[\{ file: "([^"]+?)" \}\],title: "([^"]+?)"',link)
    for url,name in match:
        addPlayL(name,url,5,'','','','','','')

def Play(resolved_url, addon_id, video_type, title, season, episode, year, watch_percent=0.9, watchedCallback=None, watchedCallbackwithParams=None, imdb_id=None):
    player = Player()    
    common.addon.log('-' + HELPER + '- -' + resolved_url)
    player.set(addon_id, video_type, title, season, episode, year, watch_percent, watchedCallback, watchedCallbackwithParams, imdb_id)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, xbmcgui.ListItem(path=resolved_url))
    return player
		
def PLAYLINK(mname,murl,thumb):
        ok=True
        stream_url = get_link(murl)     
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        infoL={'Title': mname, 'Genre': 'Live'} 
        from resources import playbackengine
        playbackengine.PlayWithoutQueueSupport(resolved_url=stream_url, addon_id=addon_id, video_type='movie', title=mname,season='', episode='', year='',img=thumb,infolabels=infoL, watchedCallbackwithParams='',imdb_id='')
        #wh = watchhistory.WatchHistory('plugin.video.HQZone')
        #if selfAddon.getSetting("whistory") == "true":
        #    wh.add_item(mname+' '+'[COLOR green]'+prettyName+'[/COLOR]', sys.argv[0]+sys.argv[2], infolabels='', img=thumb, fanart='', is_folder=False)
        return ok

def get_link(murl):
    if 'mp4' in murl:
        swf='http://www.hqzone.tv/forums/jwplayer/jwplayer.flash.swf'
        streamer=re.search('(?sim)(rtmp://.+?/vod/)(.+?.mp4)',murl)
        return streamer.group(1)+'mp4:'+streamer.group(2)+' swfUrl='+swf+' pageUrl=http://www.hqzone.tv/forums/view.php?pg=live# token=WY846p1E1g15W7s'
    setCookie(murl)
    response = net().http_GET(murl)
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    m3u8=re.findall('<a href="([^"]+?.m3u8)">',link)
    flash=re.search('file=(.+?)&streamer=(.+?)&dock',link)
    if m3u8:
        return m3u8[0]
    elif flash:
        swf='http://www.hqzone.tv/forums/jwplayer/player.swf'
        return flash.group(2)+' playpath='+flash.group(1)+' swfUrl='+swf+' pageUrl='+murl+' live=true timeout=20 token=WY846p1E1g15W7s'

    else:
        swf='http://www.hqzone.tv/forums/jwplayer/jwplayer.flash.swf'
        streamer=re.findall("file: '([^']+)',",link)[0]
        return streamer.replace('redirect','live')+' swfUrl='+swf+' pageUrl='+murl+' live=true timeout=20 token=WY846p1E1g15W7s'

def Calendar(murl):
    setCookie(murl)
    response = net().http_GET(murl)
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    month=re.findall('(?sim)<h2 class="blockhead">([^<]+?)</h2>',link)
    match=re.findall('(?sim)<h3><span class=".+?">([^<]+?)</span><span class="daynum" style=".+?" onclick=".+?">(\d+)</span></h3><ul class="blockrow eventlist">(.+?)</ul>',link)
    for day,num,data in match:
		addLink('[COLOR yellow]Times are E.S.T / GMT -5 | Follow us on Twitter for latest channel news, updates + more.[/COLOR]','','') 
		addLink('[COLOR blue]'+day+' '+num+' '+month[0]+'[/COLOR]','','')
		match2=re.findall('(?sim)<span class="eventtime">([^<]+?)</span><a href=".+?" title=".+?">([^<]+?)</a>',data)
		for time,title in match2:
			addLink('[COLOR yellow]'+time+'[/COLOR] '+title,'','')

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def addDirX(name,url,mode,iconimage,plot='',fanart='',dur=0,genre='',year='',imdb='',tmdb='',isFolder=True,searchMeta=False,addToFavs=True,
            id=None,fav_t='',fav_addon_t='',fav_sub_t='',metaType='Movies',menuItemPos=None,menuItems=None,down=False,replaceItems=True,index=False):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&plot="+urllib.quote_plus(plot)+"&fanart="+urllib.quote_plus(fanart)+"&genre="+urllib.quote_plus(genre)+"&index="+str(index)
    if not fanart: fanart=fanartimage
    if not iconimage: iconimage=art+'/vidicon.png'
    Commands = []
  
    
    liz=xbmcgui.ListItem(name, iconImage=art+'/vidicon.png', thumbnailImage=iconimage)
    liz.addContextMenuItems( Commands, replaceItems=False)
    if searchMeta:
        liz.setInfo( type="Video", infoLabels=infoLabels )
    liz.setProperty('fanart_image', fanart)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
	
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
              
params=get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
plot=None
genre=None
title=None
season=None
episode=None
location=None
path=None
index=None

try: name=urllib.unquote_plus(params["name"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: mode=int(params["mode"])
except: pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
    iconimage = iconimage.replace(' ','%20')
except: pass
try: plot=urllib.unquote_plus(params["plot"])
except: pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
    fanart = fanart.replace(' ','%20')
except: pass
try: genre=urllib.unquote_plus(params["genre"])
except: pass
try: title=urllib.unquote_plus(params["title"])
except: pass
try: episode=int(params["episode"])
except: pass
try: season=int(params["season"])
except: pass
try: location=urllib.unquote_plus(params["location"])
except: pass
try: path=urllib.unquote_plus(params["path"])
except: pass
try: index=urllib.unquote_plus(params["index"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Thumb: "+str(iconimage)

if mode==None or url==None or len(url)<1:
    MAIN()    
    VIEWSB()        
    
elif mode==2:
    LISTMENU(url)
        
elif mode==3:
    LISTCONTENT(url,iconimage)
        
elif mode==4:
    LISTMENU2(url)
            
elif mode==5:
    PLAYLINK(name,url,iconimage)

elif mode==6:
	Calendar(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))
