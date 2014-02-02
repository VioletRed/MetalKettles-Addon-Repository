import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,shutil
 
SiteName='UltraBox  [v0.0.6]  [Movies-TV]'
bvtube ='http://boxingvideostube.com/'
saddo = 'http://www.saddoboxing.com/boxing-videos/Boxing/page1.html'
saddobase = 'http://www.saddoboxing.com/boxing-videos/'
addon_id = 'plugin.video.ultrabox'
boxURL = 'http://www.myboxingcoach.com/boxing-skills/'
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
training = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/art/', 'training.jpg'))
saddologo = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/art/', 'saddo.png'))
vbtlogo = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/art/', 'icon2.png'))
logo = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/art/', 'logo.png'))

selfAddon = xbmcaddon.Addon(id=addon_id)

def INDEX():
        addDir('Boxing VideoTube',bvtube,1,vbtlogo,'hihjhkjhkjhjkhkhk')
        addDir('Saddo Boxing',saddo,3,saddologo,'')
        addDir('Ultrabox Mega Search','url',5,logo,'')       
        addDir('Boxing Podcasts','url',6,'http://evepodcasts.com/wp-content/uploads/2012/05/podcast-headphones.png','')
        addDir('Boxing Training','url',9,training,'')
        
def GETBVTUBEFIGHTERS(url):
        link = open_url(url)
        match=re.compile('class="dir">(.+?)\n\t\t<ul>').findall(link)
        for name in match:
                print name
                addDir(name,bvtube,2,vbtlogo,'')

def GETBVTUBEIGHTS(url):
        link = open_url(url)
        match=re.compile('<li><a href="(.+?)">(.+?) vs. (.+?)</a></li>').findall(link)
        for url, fighter, opp in match:
                print url
                if fighter == name:
                       addDir(fighter + ' vs ' + opp,url,50,vbtlogo,'')
def SADDOCATS(url):
        addDir('Browse Saddo Boxing',saddo,4,saddologo,'')
        addDir('Search Saddo Boxing....',saddo,80,saddologo,'')


def SADDOFIGHTS(url):
        link = open_url(url)
        match=re.compile('<h3><a href="(.+?)">(.+?)</a></h3>\n\n      <a href=".+?"><img src="(.+?)"').findall(link)
        for url, name, thumb in match:
            test = url.split ('/',2)
            youtube_id = test[1]
            url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % youtube_id
            addDir(name,url,200,thumb,'')
        match=re.compile('<p class="next_page"><a href="(.+?)">Next Page</a></p>').findall(link)
        for url in match:
               addDir ('[B][COLOR gold]Next Page >>[/COLOR][/B]',saddobase + url,4,saddologo,'')
            
def PLAYBVTUBE(url):
        link = open_url(url)
        match=re.compile('&file=(.+?)&autostart=true&stretching=exactfit').findall(link)
        for url in match:
                PLAYLINK('',url)

def SEARCHSADDO():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'test')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if search_entered == None or len(search_entered)<1:
        end()
    else:
        url = 'http://www.saddoboxing.com/boxing-videos/list.php?q='+ search_entered + '&Submit=GO'
    link = open_url(url)
    match=re.compile('<h3><a href="(.+?)">(.+?)</a></h3>\n\n      <a href=".+?"><img src="(.+?)"').findall(link)
    for url, name, thumb in match:
            test = url.split ('/',2)
            youtube_id = test[1]
            url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % youtube_id
            addDir(name,url,200,thumb,'')
    match=re.compile('<p class="next_page"><a href="(.+?)">Next Page</a></p>').findall(link)
    for url in match:
                    addDir ('[B][COLOR gold]Next Page >>[/COLOR][/B]',saddobase + url,4,saddologo,'')
        
def MEGASEARCH(url):
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'test')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
        if search_entered == None or len(search_entered)<1:
                end()
    else:
        url='https://gdata.youtube.com/feeds/api/videos?q=' + search_entered + '&start-index=1&max-results=50&v=2'
        link = open_url(url)
        match=re.compile("label='Sports'/><title>(.+?)</title><content type='application/x-shockwave-flash' src='(.+?)?version=3&amp;f=videos&amp;app=youtube_gdata'/>").findall(link)
        for name, url in match:
                youtubeid = url.split('https://www.youtube.com/v/',2)
                youtube_id = youtubeid[1].replace('?','')
                thumb = 'http://img.youtube.com/vi/'+ youtube_id+ '/0.jpg'
                url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % youtube_id
                print url
                addDir(name,url,200,thumb,'')
                
def PODCASTS(url):
         addDir('ESPN','http://sports.espn.go.com/espnradio/podcast/feeds/itunes/podCast?id=3417454',7,'http://assets.espn.go.com/i/espnradio/podcast/heavyHitting_300.jpg','')
         addDir('Yahoo Sports','http://www.yahoosportsradio.com/media/podcast/mouthpiece.rss',8,'http://findlogo.net/images/Y/yahoo%20sports%20logo.jpg','')

def GETESPN(url):
        link = open_url(url)
        match=re.compile("<title>(.+?)</title>\n                                <link>(.+?)</link>").findall(link)
        for title, mp3 in match:
            url = mp3.replace ('<![CDATA[','').replace(']]>','')
            addDir(title,url,200,'http://assets.espn.go.com/i/espnradio/podcast/heavyHitting_300.jpg','')
            
def GETYAHOO(url):
        link = open_url(url)
        match=re.compile("<title>(.+?)</title>\r\n      <link>(.+?)</link>").findall(link)
        for title, mp3 in match:
            addDir(title,mp3,200,'http://findlogo.net/images/Y/yahoo%20sports%20logo.jpg','')
                
############################ TRAINING ########################################################################################
def home_sections():
        addDir('Footwork',boxURL + 'learn-how-to-box-boxing-footwork/',10,training,'')
        addDir( 'Punching - Head',boxURL + 'learn-how-to-box-punching/',11,training,'')
        addDir('Punching - Body',boxURL + 'boxing-how-to-body-punch-page/',11,training,'')
        addDir('Body Movement',boxURL + 'learn-how-to-box-body-movement/',10,training,'')
        addDir('Defense',boxURL + 'learn-how-to-box-block-punc/',10,training,'')
 
def alt_punch_vids(url):
        html = open_url(url)
        match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(html)
        for url, name in match:
                play_training(url,name)
 
def add_punch_vids(url):
        html = open_url(url)
        match = re.compile('<p><a href="(.+?)">(.+?)</a></p>').findall(html)
        match = match[:-1]
        for url, name in match:
              play_training(url,name)

def play_training(url,name):
        html = open_url(url)
        youtube_id = re.compile('<p><iframe class=".+?" type=".+?" width=".+?" height=".+?" src="http://www.youtube.com/embed/(.{11}\?)').findall(html)
        youtube_id = youtube_id[0]
        url =  'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid={0}'.format(youtube_id)
        name = name.replace('&#8211;', '-')
        addDir(name,url,200,training,'')

############################ STANDARD  #####################################################################################
        
def PLAYLINK(name,url):
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
        exit()


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
               
def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addLink(name,url,iconimage,description,fanart):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty("IsPlayable","true")
        liz.setProperty("fanart_Image",fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
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
 
if mode==None or url==None or len(url)<1: INDEX()
elif mode==1: GETBVTUBEFIGHTERS(url)
elif mode==2: GETBVTUBEIGHTS(url)
elif mode==3: SADDOCATS(url)
elif mode==4: SADDOFIGHTS(url)
elif mode==5: MEGASEARCH(url)
elif mode==6: PODCASTS(url)
elif mode==7: GETESPN(url)
elif mode==8: GETYAHOO(url)
elif mode==9: home_sections()
elif mode==10: alt_punch_vids(url)
elif mode==11: add_punch_vids(url)
elif mode==12: get_videos(url)
elif mode==50: PLAYBVTUBE(url)
elif mode==80: SEARCHSADDO()
elif mode==100: VIDEOLINKS(url,name)
elif mode==200: PLAYLINK(name,url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))
