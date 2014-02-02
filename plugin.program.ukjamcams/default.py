import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,random,os
 
SiteName='ukjamcams-0.0.6'
BaseURL ='http://www.bbc.co.uk/england/webcams/traffic'
BaseURL2 = 'http://www.bbc.co.uk'

def INDEX():
        req = urllib2.Request(BaseURL)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(link)
        int = 0
        addDir('Three Counties | Beds, Herts and Bucks','http://www.bbc.co.uk/threecounties/travel/jamcams/index.shtml',1,'http://www.clipartsfree.net/vector/large/schoolfreeware_Movie_Camera_Vector_Clipart.png')
        for url,name in match:
            int = int + 1
            if '/jamcams/' or '/webcams/' in url:
                if int > 3:
                    url2 = 'http://www.bbc.co.uk' + url
                    addDir(name,url2,1,'http://www.clipartsfree.net/vector/large/schoolfreeware_Movie_Camera_Vector_Clipart.png')

def GETCAMS(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<p><span><a href="(.+?)">(.+?)</a></span> </p>').findall(link)
        for url,name in match:
                picurl1 = 'http://www.bbc.co.uk' + url + '/serveimage'
                picurl1 += '?%d=%d' % (random.randint(1, 10000), random.randint(1, 10000))
                addDir(name,url,2,picurl1,isFolder=False); #print url

class bigcam(xbmcgui.Window):
        def __init__(self):
            imgControl = xbmcgui.ControlImage(100, 0, 1080, 720, "")
            self.addControl(imgControl)
            imgControl.setImage(ImgUrl)
            

def SHOWPIC():
        My_Window = bigcam()
        My_Window.doModal()
        del My_Window

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
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&site="+str(site)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&img="+urllib.quote_plus(iconimage)
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
try: ImgUrl=urllib.unquote_plus(params["img"])
except: ImgUrl=''
 
print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
 
if mode==None or url==None or len(url)<1: INDEX()
elif mode==1: GETCAMS(url)
elif mode==2: SHOWPIC()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
