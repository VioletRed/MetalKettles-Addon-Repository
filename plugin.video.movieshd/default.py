import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os,random
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net as net
from metahandler import metahandlers

addon_id = 'plugin.video.movieshd'
selfAddon = xbmcaddon.Addon(id=addon_id)
metaget = metahandlers.MetaData(preparezip=False)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.PNG'))
artpath = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id + '/resources/art/'))

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
        
def CATEGORIES():
        addDir2('Featured','http://movieshd.co/watch-online/category/featured?filtre=date',1,icon,'',fanart)
        addDir2('Recently Added','http://movieshd.co/?filtre=date&cat=0',1,icon,'',fanart)
        addDir2('Most Viewed','http://movieshd.co/?filtre=views&cat=0',1,icon,'',fanart)
        addDir2('Highest Rated','http://movieshd.co/?filtre=rate&cat=0',1,icon,'',fanart)
        addDir2('Genres','url',2,icon,'',fanart)
        addDir2('Bollywood','http://movieshd.co/watch-online/category/bollywood',1,icon,'',fanart) 
        addDir2('Search','url',3,icon,'',fanart)
        addLink('','','',icon,fanart)
        addLink('[COLOR blue]Twitter[/COLOR] Feed','url',4,icon,fanart)

                
def TWITTER():
        text=''
        twit = 'http://twitrss.me/twitter_user_to_rss/?user=movieshd_co'
        twit += '?%d' % (random.randint(1, 1000000000000000000000000000000000000000))
        response = net().http_GET(twit)
        link = response.content
        match=re.compile("<description><!\[CDATA\[(.+?)\]\]></description>.+?<pubDate>(.+?)</pubDate>",re.DOTALL).findall(link)
        for status, dte in match:
            status = status.replace('\n',' ')
            status = status.encode('ascii', 'ignore').decode('ascii').replace('&#x27;','\'').replace('&#xA0;','').replace('&#x2026;','')
            dte = '[COLOR red][B]'+dte+'[/B][/COLOR]'
            dte = dte.replace('+0000','').replace('2014','').replace('2015','')
            text = text+dte+'\n'+status+'\n'+'\n'
        showText('@movieshd_co', text)
        quit()

def GETMOVIES(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href="(.+?)" title="(.+?)">').findall(link)
        for url,name in match:
                name2 = name.decode("ascii","ignore").replace('&#8217;','').replace('&amp;','').replace('&#8211;','').replace('#038;','')
                if not 'razor' in name2:
                        if not 'Rls' in name2:
                                if not 'DCMA' in name2:
                                        if not 'Privacy' in name2:
                                                if not 'FAQ' in name2:
                                                        if not 'Download' in name2:
                                                                addDir(name2,url,100,'',len(match),isFolder=False)
        match=re.compile('<a class="next page-numbers" href="(.+?)">Next videos &raquo;</a>').findall(link)
        if len(match)>0:
                addDir('Next Page>>',match[0],1,artpath+'nextpage.png',len(match),isFolder=True)
        xbmc.executebuiltin('Container.SetViewMode(500)')

def GENRES(url):
        addDir2('Action','http://movieshd.co/watch-online/category/action/',1,artpath+'action.png','',fanart)
        addDir2('Adventure','http://movieshd.co/watch-online/category/adventure/',1,artpath+'adventure.png','',fanart)
        addDir2('Animation','http://movieshd.co/watch-online/category/animation/',1,artpath+'animation.png','',fanart)
        addDir2('Biography','http://movieshd.co/watch-online/category/biography/',1,artpath+'biography.png','',fanart)
        addDir2('Comedy','http://movieshd.co/watch-online/category/comedy/',1,artpath+'comedy.png','',fanart)
        addDir2('Crime','http://movieshd.co/watch-online/category/crime/',1,artpath+'crime.png','',fanart)
        addDir2('Drama','http://movieshd.co/watch-online/category/drama/',1,artpath+'drama.png','',fanart)
        addDir2('Family','http://movieshd.co/watch-online/category/family/',1,artpath+'family.png','',fanart)
        addDir2('Fantasy','http://movieshd.co/watch-online/category/fantasy/',1,artpath+'fantasy.png','',fanart)
        addDir2('History','http://movieshd.co/watch-online/category/history/',1,artpath+'history.png','',fanart)
        addDir2('Horror','http://movieshd.co/watch-online/category/horror/',1,artpath+'horror.png','',fanart)
        addDir2('Music','http://movieshd.co/watch-online/category/music/',1,artpath+'musical.png','',fanart)
        addDir2('Mystery','http://movieshd.co/watch-online/category/mystery/',1,artpath+'mystery.png','',fanart)
        addDir2('Romance','http://movieshd.co/watch-online/category/romance/',1,artpath+'romance.png','',fanart)
        addDir2('Sci-Fi','http://movieshd.co/watch-online/category/sci-fi/',1,artpath+'sci-fi.png','',fanart)
        addDir2('Sports','http://movieshd.co/watch-online/category/sports/',1,artpath+'sport.png','',fanart)
        addDir2('Thriller','http://movieshd.co/watch-online/category/thriller/',1,artpath+'thriller.png','',fanart)
        addDir2('War','http://movieshd.co/watch-online/category/war/',1,artpath+'war.png','',fanart)
        addDir2('Western','http://movieshd.co/watch-online/category/western/',1,artpath+'western.png','',fanart)

def SEARCH():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'Search Movies HD')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered)>1:
        url = 'http://movieshd.co/?s='+ search_entered
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        GETMOVIES(url,name)

def PLAYLINK(name,url):
        #try:
        req = urllib2.Request(url)
        print 'here'
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('src="http://videomega.tv/validatehash.php\?hashkey=(.+?)">').findall(link)
        if len(match)==0:
            match=re.compile("src=\'http://videomega.tv/validatehash.php\?hashkey=(.+?)\'>").findall(link)
        videomega_id_url = "http://videomega.tv/validatehash.php?hashkey="+ match[0]
        print match
             
        req = urllib2.Request(videomega_id_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('var ref="(.+?)";').findall(link)
        vididresolved = match[0]
        videomega_url = 'http://videomega.tv/iframe.php?ref='+vididresolved
        #except:
        #       req = urllib2.Request(url)
        #       req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        #       response = urllib2.urlopen(req)
        #       link=response.read()
        #       response.close()
        #       match=re.compile("ref=\'(.+?)'").findall(link)
        #       print match
        #       if (len(match) > 0):
        #                videomega_url = "http://videomega.tv/iframe.php?ref=" + match[2]
        #                print videomega_url
        #       if (len(match) == 0):
        #                match=re.compile("frameborder='.+?' src='(.+?)?").findall(link)
        #                videomega_url = match[0]

        req = urllib2.Request(videomega_url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        url = re.compile('document.write.unescape."(.+?)"').findall(link)[0]
        url = urllib.unquote(url)
        stream_url = re.compile('file: "(.+?)"').findall(url)[0]
        liz=xbmcgui.ListItem(name, iconImage=icon,thumbnailImage=icon); liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        xbmc.Player ().play(stream_url, liz, False)

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
        xbmc.executebuiltin('Container.SetViewMode(50)')
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir(name,url,mode,iconimage,itemcount,isFolder=True):
        splitName=name.partition('(')
        simplename=""
        simpleyear=""
        if len(splitName)>0:
            simplename=splitName[0]
            simpleyear=splitName[2].partition(')')
            if len(simpleyear)>0:
                simpleyear=simpleyear[0]
        meta = metaget.get_meta('movie', simplename ,simpleyear)
        print meta
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

def addLink(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
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
elif mode==3: SEARCH()
elif mode==4: TWITTER()
elif mode==100: PLAYLINK(name,url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

