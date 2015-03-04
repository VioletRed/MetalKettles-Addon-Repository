import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil,urlresolver,random
from resources.libs.common_addon import Addon

addon_id        = 'plugin.video.dijentertainments'
addon           = Addon(addon_id, sys.argv)
fanart          = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon            = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
baseurl         = 'https://raw.githubusercontent.com/djjohnnyb15/dij-entertainments/master/Directory/dij_entertainments_Directory.xml'

def GetList():
        link=open_url(baseurl)
        fanart=re.compile('<fanart>(.+?)</fanart>').findall(link)[0]
        match= re.compile('<name>(.+?)</name>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>',re.DOTALL).findall(link)
        for name,url,thumb in match:
            if '@' not in name:
                    addDir(name,url,1,thumb,fanart)
        addLink('','url','mode',icon,fanart)
        addLink('Twitter Feed','url',2,icon,fanart)

def GetContent(url,iconimage):
        link=open_url(url)
        try:fanart=re.compile('<fanart>(.+?)</fanart>').findall(link)[0]
        except:pass
        if '<dir>' in link:
            match= re.compile('<name>(.+?)</name>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>',re.DOTALL).findall(link)
            for name,url,thumb in match:
                addDir(name,url,1,thumb,fanart)      
        elif '<item>' in link:
            match= re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>',re.DOTALL).findall(link)
            for name,url,thumb in match:
                addDir(name,url,1,thumb,fanart)
        else:PLAYLINK(url,iconimage)

def PLAYLINK(url,iconimage):
            resolved_url = urlresolver.HostedMediaFile(url).resolve()
            playlist = xbmc.PlayList(1)
            playlist.clear()
            listitem = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
            listitem.setInfo("Video", {"Title":name})
            listitem.setProperty('mimetype', 'video/x-msvideo')
            listitem.setProperty('IsPlayable', 'true')
            playlist.add(resolved_url,listitem)
            xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
            xbmcPlayer.play(playlist)
            quit()
            
def TWITTER():
        text = ''
        twit = 'https://script.google.com/macros/s/AKfycbyBcUa5TlEQudk6Y_0o0ZubnmhGL_-b7Up8kQt11xgVwz3ErTo/exec?573185581745889283'
        link = open_url(twit)
        link = link.replace('/n','')
        link = link.decode('utf-8').encode('utf-8').replace('&#39;','\'').replace('&#10;',' - ').replace('&#x2026;','')
        match=re.compile("<title>(.+?)</title>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)[1:]
        for status, dte in match:
            status = status.encode('ascii', 'ignore')
            dte = dte[:-15]
            dte = '[COLOR blue][B]'+dte+'[/B][/COLOR]'
            text = text+dte+'\n'+status+'\n'+'\n'
        showText('[COLOR blue][B]@dijentertainmen[/B][/COLOR]', text)
        quit()

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
                                     
def open_url(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

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
 
print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
 
if mode==None or url==None or len(url)<1: GetList()
elif mode==1:GetContent(url,iconimage)
elif mode==2:TWITTER()



xbmcplugin.endOfDirectory(int(sys.argv[1]))
