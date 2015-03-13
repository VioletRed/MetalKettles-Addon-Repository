import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,json,base64

AddonID ='plugin.video.mksports'
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
    
def menu():
    addDir('MK Sports Original Collection','url',1,icon,fanart)
    addDir('BVLS 2013','url',2,icon,fanart)
    
def MKSports():
    channelurl='http://www.softmagnate.com/CMS-Server-Pak-Hind-HD/getJson.php'
    response=Get_url(channelurl)
    link=json.loads(response)
    for field in link:
        categoryName= field['categoryName'].encode("utf-8")
        channelLink= field['channelLink'].encode("utf-8")
        channelName=field['channelName'].encode("utf-8")
        if categoryName == 'Sports' or categoryName == 'Sports HD' or categoryName == 'Sports Time TV' or categoryName == 'Bein Sports' or categoryName == 'OTE Sports' or categoryName == 'Football' or categoryName == 'Cricket World Cup 2015' or categoryName == 'Sports Full HD':

            if not "3pm" in channelName:
                addLink(channelName,channelLink,100,icon,fanart)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)

def BVLS():
    addDir('Daily Schedule','http://bvls2013.com/index.html',4,icon,fanart)
    addLink('Stream 1','http://bvls2013.com/stream1.html',3,icon,fanart)
    addLink('Stream 2','http://bvls2013.com/stream2.html',3,icon,fanart)
    addLink('Stream 3','http://bvls2013.com/stream3.html',3,icon,fanart)
    addLink('Stream 4','http://bvls2013.com/stream4.html',3,icon,fanart)
    addLink('Stream 5','http://bvls2013.com/stream5.html',3,icon,fanart)
    addLink('Stream 6','http://bvls2013.com/stream6.html',3,icon,fanart)
    addLink('Stream 7','http://bvls2013.com/stream7.html',3,icon,fanart)
    addLink('Stream 8','http://bvls2013.com/stream8.html',3,icon,fanart)
    addLink('Stream 9','http://bvls2013.com/stream9.html',3,icon,fanart)
    addLink('Stream 10','http://bvls2013.com/stream10.html',3,icon,fanart)

def GetBVLSStream(name,url):
    link = Get_url(url)
    match=re.compile('src="(.+?)" id="myfr"').findall(link)[0]
    link = Get_url(match)
    match=re.compile("file\s*\:\s*window.atob\('(.+?)'\)").findall(link)[0]
    temp_url = base64.b64decode(match)
    veetleId = getVeetleIdByUrl(temp_url)
    url = 'plugin://plugin.video.veetle/?channel='+veetleId
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name + " - " + url, iconImage=icon, thumbnailImage=icon)
    listitem.setInfo("Video", {"Title":name})
    listitem.setProperty('mimetype', 'video/x-msvideo')
    listitem.setProperty('IsPlayable', 'true')
    playlist.add(url,listitem)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    xbmcPlayer.play(playlist)

def getVeetleIdByUrl(url):
    _regex_getM3u = re.compile("http://(.*?)/flv/(.*?)/1.flv", re.DOTALL)
    streamId = _regex_getM3u.search(url).group(2)
    return streamId

def BVLSSched(url):
    link = Get_url(url)
    datestr=re.compile('<span style="text-decoration: underline;"><b>(.+?)</b></span></span></div>').findall(link)[0]
    datestr = "[B][COLOR gold]"+datestr+"[/COLOR][/B]"
    addLink(datestr,'url','mode',icon,fanart)
    match=re.compile('12px;">(.+?)</span></p>.+?#000000">(.+?)</span></b></p>.+?<p><a href=".+?">(.+?)</a></p>',re.DOTALL).findall(link)
    for timestr, name, stream in match:
        name = timestr + " == " + name + " (" + stream + ")"
        addLink(name,'url','mode',icon,fanart)

def Get_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
def Play(name,url):  
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
    xbmc.Player().play(url, liz, False)
    return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
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
description=None

try:url=urllib.unquote_plus(params["url"])
except:pass
try:name=urllib.unquote_plus(params["name"])
except:pass
try:mode=int(params["mode"])
except:pass
try:iconimage=urllib.unquote_plus(params["iconimage"])
except:pass
print "Mode: "+str(mode);print "URL: "+str(url);print "Name: "+str(name);print "IconImage: "+str(iconimage)

if mode==None or url==None or len(url)<1:menu()
elif mode==1:MKSports()
elif mode==2:BVLS()
elif mode==3:GetBVLSStream(name,url)
elif mode==4:BVLSSched(url)




elif mode==100:Play(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
