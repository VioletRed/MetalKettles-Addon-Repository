import urllib,urllib2,re,xbmcplugin,xbmcgui,os
import cookielib
import settings, time
import requests
import json
from t0mm0.common.net import Net
from threading import Thread
from datetime import date
cookie_jar = settings.cookie_jar()
net = Net()
ADDON = settings.addon()
FAV_ARTIST = settings.favourites_file_artist()
FAV_ALBUM = settings.favourites_file_album()
FAV_SONG = settings.favourites_file_songs()
FAV_VIDEO = settings.favourites_file_videos()
FAV_VIDEOARTIST = settings.favourites_file_videoartists()
PLAYLIST_FILE = settings.playlist_file()
MUSIC_DIR = settings.music_dir()
HIDE_FANART = settings.hide_fanart()
QUEUE_SONGS = settings.default_queue()
QUEUE_ALBUMS = settings.default_queue_album()
DOWNLOAD_LIST = settings.download_list()
fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.binaural',  'fanart.jpg'))
art = 'http://kinkin-xbmc-repository.googlecode.com/svn/trunk/zips/plugin.audio.binaural/art/'
iconart = xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.binaural',  'icon.png'))
trans_table = ''.join( [chr(i) for i in range(128)] + [' '] * 128 )
IMVDBAPI = 'MhHzYm6SBfTBfYrhvIoVnSIZ9pE8vIjhZ1RXoYQZ'
APIURL = 'http://imvdb.com/api/v1'


def open_url(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
	
def GET_url(url):
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0'
    header_dict['Host'] = 'www.itemvn.com'
    header_dict['Referer'] = 'http://www.itemvn.com/'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Cache-Control'] = 'max-age=0'
    net.set_cookies(cookie_jar)
    link = net.http_GET(url, headers=header_dict).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)
    return link
	
def get_cookie():
    header_dict = {}
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.2; rv:24.0) Gecko/20100101 Firefox/24.0'
    header_dict['Connection'] = 'keep-alive'
    net.set_cookies(cookie_jar)
    link = net.http_GET('http://musicmp3.ru/', headers=header_dict).content.encode("utf-8").rstrip()
    net.save_cookies(cookie_jar)


def CATEGORIES():
    addDir('Audio','url',1300,art + 'audio.png','')
    addDir('Video','url',1301,art + 'video.png','')
	
def audio():
    addDir('Billboard Hot Singles','http://www.itemvn.com/hot100/',1070,art + 'billboard_hot_singles.png','')
    addDir('Best Selling Albums','http://www.itemvn.com/bestsellers/',1070,art + 'best_selling_albums.png','')
    addDir('Charts','url',101,art + 'billboardcharts.jpg','')
    addDir('Hot Artists','http://www.itemvn.com/topartists/',1070,art + 'hot_artists.png','')
    addDir('Artist A-Z','url',1010,art + 'artists_a-z.png','')
    addDir('Browse Songs','url',1080,art + 'browse_songs.png','')
    addDir('Genres (Just Added)','url',1060,art + 'genres_just_added.png','')
    addDir('Moods - play what you feel','url',1203,art + 'moods.png','')
    addDir('Search','url',1201,art + 'search.png','')
    addDir('Favourites','url',1202,art + 'favourites.png','')
    addDirAudio('Instant Mix Favourite Songs (Shuffle and Play)','url',99,art + 'instant_mix_songs.png','','','','','')
    addDirAudio('Instant Mix Favourite Albums (Shuffle and Play)','url',89,art + 'instant_mix_albums.png','','','','','')
	
def video():
    addDir('Best New Music Videos','http://imvdb.com/picks',1302,art + 'artists.jpg','n')
    addDir('New Releases','http://imvdb.com/new',1302,art + 'artists.jpg','n')
    addDir('Most Viewed Videos','url',1303,art + 'artists.jpg','n')
    addDir('Videos by Release Date','http://imvdb.com/calendar',1307,art + 'artists.jpg','')
    addDir('Videos by Country','http://imvdb.com/country',1311,art + 'artists.jpg','')
    addDir('Genres (Popular/New Releases)','http://imvdb.com/genres',1304,art + 'searchartists.jpg','n')
    addDir('Artist A-Z','url',1312,art + 'artists_a-z.png','')
    addDirVideo('Random Video','http://imvdb.com/random',1320,'','Random','Random','Random','','')
    #addDir('Awards','http://imvdb.com/awards',1315,art + 'searchartists.jpg','')
    addDir('Search','video',1321,art + 'search.png','')
    addDir('Favourite Songs','url',1325,art + 'favourite_songs.png','')
    addDir('Favourite Artists','url',1326,art + 'favourite_artists.png','')
	
def searchvideomenu(name,url):
    addDir('Search Artists/Directors','artist',1322,art + 'searchartists.jpg','')
    addDir('Search Videos','video',1322,art + 'searchalbums.jpg','')
	
def searchvideo(name, url):
    keyboard = xbmc.Keyboard('', name, False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            search_videos(query,url)
			
def search_videos(query,data):
    url = "http://imvdb.com/search?search_term=%s" % query
    link = open_url(url)
    if data == 'artist':
        result = regex_from_to(link, '<h4>Artists, Directors, and Crew:</h4>', '</table>')
        match = re.compile('<tr><td width="50"><a href="(.+?)"><img src="(.+?)" class="border_img" /></a></td><td><a href="(.+?)"><h5><strong>(.+?)</strong></h5></a></td></tr>').findall(result)
        for url,thumb,url1,title in match:
            url = 'http://imvdb.com/' + url
            addDir(title,url,1314,art + 'searchartists.jpg','videoartist')
    else:
        result = regex_from_to(link, '<h4>Videos</h4>', '</table>')
        match = re.compile('<tr><td width="50"><a href="(.+?)"><img class="searchImg" src="(.+?)" /></td><td><a href="(.+?)"><h5>(.+?)</h5><p style="margin-bottom(.+?)">(.+?)</p></a></td></tr>').findall(result)
        for vurl,iconimage,vurl1,song,d1,artist in match:
            title = "[COLOR gold]%s[/COLOR] | [COLOR cyan]%s[/COLOR]" % (artist,song)
            addDirVideo(title,vurl,1320,iconimage,song,artist,'','','')
		
    

	
def video_list(name,url,page):
    link = open_url(url)
    if 'http://imvdb.com/genre' in url:
        all_videos = regex_get_all(link, '<div class="slideNode', 'p class="node_info')
        for a in all_videos:
            if not 'Not Available Online' in a:
                vurl = regex_from_to(a, '<a href="', '"')
                iconimage = regex_from_to(a, '<img class="rack_img" src="', '"').replace('tv.jpg', 'bv.jpg')
                songinfo = regex_from_to(a, '<h3>', '</h3>')
                song = regex_from_to(songinfo, '">', '<').rstrip()
                artistinfo = regex_from_to(a, '<h4>', '</h4>')
                artist = regex_from_to(artistinfo, '">', '<')
                artisturl = regex_from_to(artistinfo, 'href="', '"')
                title = "[COLOR gold]%s[/COLOR] | [COLOR cyan]%s[/COLOR]" % (artist,song)
                addDirVideo(title,vurl,1320,iconimage,song,artist,artisturl,'','')
    else:
        all_videos = regex_get_all(link, '<div class="rack_node', '</div>')
        for a in all_videos:
            if not 'Not Available Online' in a:
                vurl = regex_from_to(a, '<a href="', '"')
                iconimage = regex_from_to(a, '<img class="rack_img" src="', '"').replace('tv.jpg', 'bv.jpg')
                song = regex_from_to(a, 'title="', '">').rstrip()
                artistinfo = regex_from_to(a, '<h4>', '</h4>')
                artist = regex_from_to(artistinfo, '">', '<')
                artisturl = regex_from_to(artistinfo, 'href="', '"')
                title = "[COLOR gold]%s[/COLOR] | [COLOR cyan]%s[/COLOR]" % (artist,song)
                addDirVideo(title,vurl,1320,iconimage,song,artist,artisturl,'','')
			
def most_viewed(name,url):
    addDir('Most Popular New Videos','http://imvdb.com/charts/new?page=',1306,art + 'new_videos.png','1')
    addDir('Most Popular This Week','http://imvdb.com/charts/week?page=',1306,art + 'this_week.png','1')
    addDir('Most Popular This Month','http://imvdb.com/charts/month?page=',1306,art + 'this_month.png','1')
    addDir('Most Popular of All Time','http://imvdb.com/charts/all?page=',1306,art + 'all_time.png','1')
	
def video_genres(name,url):
    link = open_url(url)#
    all_genres = regex_get_all(link, '<div class="glassBox">', '</div>')
    for a in all_genres:
        url = regex_from_to(a, 'href="', '"')
        title = regex_from_to(a, '</i>', '<').lstrip()
        iconimage = regex_from_to(a, 'image: url', '"').replace('(','').replace(')','')
        addDir(title,url,1302,iconimage,'1')
		
def awards(name,url):
    link = open_url(url)#
    match = re.compile('<h4><a href="(.+?)">(.+?)</a></h4>').findall(link)
    for url,title in match:
        iconimage = art + title +'.jpg'
        addDir(title,url,1302,iconimage,'1')
	
def video_date(name,url):
    link = open_url(url)
    match = re.compile('<a class="yearLink well" href="(.+?)">(.+?)</a>	</div>').findall(link)
    for url,title in match:
        addDir(title,url,1308,art + title + '.png','n')
		
def video_date_month(name,url,iconimage):
    link = open_url(url)
    monthdata = regex_from_to(link, '<ul class="sideMenu">', '</ul>')
    match = re.compile('<li><a(.+?)href="(.+?)">(.+?)</a></li>').findall(monthdata)
    for d1,url,title in match:
        url = "%s?page=" % url
        addDir(title,url,1309,iconimage,'1')
		
def video_list_date(name,url,page):
    url1 = "%s%s" % (url,page)
    nextpage = int(page)+1
    link = open_url(url1)
    vidlist = regex_from_to(link, '<table class="', '</table>')
    all_videos = regex_get_all(vidlist, '<tr', '</tr>')
    for a in all_videos:
        try:
            vurl = regex_from_to(a, '<a href="', '"')
            iconimage = regex_from_to(a, '<img src="', '"').replace('tv.jpg', 'bv.jpg')
            song = regex_from_to(a, 'title="', '">').rstrip()
            artistinfo = regex_from_to(a, '<h4>', '</h4>')
            artist = regex_from_to(artistinfo, '">', '<').lstrip()
            artisturl = regex_from_to(artistinfo, 'href="', '"')
            title = "[COLOR gold]%s[/COLOR] | [COLOR cyan]%s[/COLOR]" % (artist,song)
            addDirVideo(title,vurl,1320,iconimage,song,artist,artisturl,'','')
        except:
            pass
    if page != 'n':
        addDir('Next Page >>',url,1309,art + 'topalbums.jpg',str(nextpage))
			
def video_chart_list(name,url,page):
    url1 = "%s%s" % (url,page)
    nextpage = int(page)+1
    link = open_url(url1)
    vidlist = regex_from_to(link, '<table class="', '</table>')
    all_videos = regex_get_all(vidlist, '<tr', '</tr>')
    nitem = len(all_videos)
    for a in all_videos:
        try:
            vurl = regex_from_to(a, '<a href="', '"')
            iconimage = regex_from_to(a, '<img src="', '"')
            song = regex_from_to(a, 'title="', '">').rstrip()
            artistinfo = regex_from_to(a, '<p class="artist_line">', '</td>')
            artistline = regex_from_to(artistinfo, '<p>', '</p>').replace('\n','').replace('\t','')
            artist = regex_from_to(artistline, '">', '<').lstrip()
            artisturl = regex_from_to(artistline, 'href="', '"')
            title = "[COLOR gold]%s[/COLOR] | [COLOR cyan]%s[/COLOR]" % (artist,song)
            addDirVideo(title,vurl,1320,iconimage,song,artist,artisturl,'','')
        except:
            pass
    if nitem == 40:
        addDir('Next Page >>',url,1306,art + 'topalbums.jpg',str(nextpage))
		
def video_artists(name,url):
    alphabet =  ['0-9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
    for a in alphabet:
        addDir(a,a.lower(),1313,art + a.lower() +'.png','1')
		
def artist_videos(name,url):
    link = open_url(url)#<div id="director-credits">
    try:
        artistlst = regex_from_to(link, '<div id="artist-credits"', '</tbody>')
    except:
        try:
            artistlst = regex_from_to(link, '<div id="director-credits"', '</tbody>')
        except:
            artistlst = regex_from_to(link, '<div id="animator-credits"', '</tbody>')
    all_videos = regex_get_all(artistlst, '<tr', '<span><em>Director')
    for a in all_videos:
        vurl = regex_from_to(a, '<a href="', '"')
        iconimage = regex_from_to(a, 'data-src="', '"').replace('tv.jpg', 'bv.jpg')
        songinfo = regex_from_to(a, '<td width="40%"><strong>', 'a>')
        song = regex_from_to(songinfo, '">', '<').rstrip()
        artist = name
        artisturl = url
        title = "[COLOR gold]%s[/COLOR] | [COLOR cyan]%s[/COLOR]" % (artist,song)
        addDirVideo(title,vurl,1320,iconimage,song,artist,artisturl,'','videoartist')
		
def video_artist_list(name,url,iconimage):
    url = 'http://imvdb.com/browse/artists/' + url
    link = open_url(url)
    all_artists = regex_from_to(link, 'ul class="nameList">', '<div id="footer">')
    match = re.compile('<li(.+?)a href="(.+?)">(.+?)</a></li>').findall(all_artists)
    for d1, url, title in match:
        addDir(title,url,1314,iconimage,'n')
		
def video_countries(name,url):
    link = open_url(url)
    match = re.compile('<li><a href="(.+?)"><strong>(.+?)</strong></a></li>').findall(link)
    for url,title in match:
        url = "%s?page=" % url
        addDir(title,url,1309,iconart,'1')
		
def play_video(name,url,iconimage,artist,song,mix,clear):
    link = open_url(url)
    videoid = regex_from_to(link, 'FI.video_source_id = "', '"')
    url = 'plugin://plugin.video.youtube/?action=play_video&videoid=' + videoid
    listitem = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage, path=url)
    xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
    handle = str(sys.argv[1])    
    if handle != "-1":
        listitem.setProperty("IsPlayable", "true")
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
    else:
        xbmcPlayer.play(url, listitem)

      

def moods():
    addDir('Featured Moods','https://www.stereomood.com/tools/ajax_index_tag.php?type=00',1204,art + 'featured_moods.png','')
    addDir('Hot Moods','https://www.stereomood.com/tools/ajax_index_tag.php?type=01',1204,art + 'hot_moods.png','')
    addDir('Popular Moods','https://www.stereomood.com/tools/ajax_index_tag.php?type=02',1204,art + 'popular_moods.png','')
    addDir('Casual Vibes','https://www.stereomood.com/tools/ajax_index_tag.php?type=03',1204,art + 'casual_vibes.png','')
	
def moodlist(url):
    link = open_url(url)
    match = re.compile('"id":"(.+?)","des":"(.+?)","img":"(.+?)","play":(.+?),"hot":(.+?)').findall(link)
    for id,des,thumb,play,hot in match:
        title= des.capitalize()
        iconimage = 'http://stereomood.com/repository/tags/moods/img/%s' % thumb
        url = 'http://www.stereomood.com/mood/%s/playlist.json?save&index=' % urllib.quote(des).replace(' ', '_')
        addDir(title,url,1205,iconimage,"1")
	
def searchmenu(name,url):
    addDir('Search Artists','url',24,art + 'search_artists.png','')
    addDir('Search Albums','url',24,art + 'search_albums.png','')
    addDir('Search Songs','url',24,art + 'search_songs.png','')
	
def favouritesmenu():
    addDir('Favourite Artists','url',63,art + 'favourite_artists.png','')
    addDir('Favourite Albums','url',66,art + 'favourite_albums.png','')
    addDir('Favourite Songs','url',69,art + 'favourite_songs.png','')
	
def genres(url):
    addDir('All Genres','http://www.itemvn.com/justadded/Genre/All/',1050,art + 'all_genres.png','1')
    addDir('Pop','http://www.itemvn.com/justadded/Genre/Pop/',1050,art + 'pop.png','1')
    addDir('Latin','http://www.itemvn.com/justadded/Genre/Latin/',1050,art + 'latin.png','1')
    addDir('Country','http://www.itemvn.com/justadded/Genre/Country/',1050,art + 'country.png','1')
    addDir('Classical','http://www.itemvn.com/justadded/Genre/Classical/',1050,art + 'classical.png','1')
    addDir('Rock','http://www.itemvn.com/justadded/Genre/Rock/',1050,art + 'rock.png','1')
    addDir('Electronic','http://www.itemvn.com/justadded/Genre/Electronic/',1050,art + 'electronic.png','1')
    addDir('Jazz','http://www.itemvn.com/justadded/Genre/Jazz/',1050,art + 'jazz.png','1')
    addDir('New Age','http://www.itemvn.com/justadded/Genre/New Age/',1050,art + 'new_age.png','1')
    addDir('R&B','http://www.itemvn.com/justadded/Genre/R-B/',1050,art + 'r_b.png','1')
    addDir('Alternative','http://www.itemvn.com/justadded/Genre/Alternative/',1050,art + 'alternative.png','1')
    addDir('Blues','http://www.itemvn.com/justadded/Genre/Blues/',1050,art + 'blues.png','1')
    addDir('Soundtrack','http://www.itemvn.com/justadded/Genre/Soundtrack/',1050,art + 'soundtrack.png','1')
    addDir('Hip Hop','http://www.itemvn.com/justadded/Genre/Hip Hop/',1050,art + 'hip_hop.png','1')
    addDir('Metal','http://www.itemvn.com/justadded/Genre/Metal/',1050,art + 'metal.png','1')
    addDir('Soul','http://www.itemvn.com/justadded/Genre/Soul/',1050,art + 'soul.png','1')
    addDir('Christmas','http://www.itemvn.com/justadded/Genre/Christmas/',1050,art + 'christmas.png','1')
    addDir('Rap','http://www.itemvn.com/justadded/Genre/Rap/',1050,art + 'rap.png','1')
    addDir('Indie','http://www.itemvn.com/justadded/Genre/Indie/',1050,art + 'indie.png','1')
    addDir('Folk','http://www.itemvn.com/justadded/Genre/Folk/',1050,art + 'folk.png','1')
    addDir('Teen','http://www.itemvn.com/justadded/Genre/Teen/',1050,art + 'teen.png','1')
    addDir('Dance','http://www.itemvn.com/justadded/Genre/Dance/',1050,art + 'dance.png','1')
    addDir('Punk','http://www.itemvn.com/justadded/Genre/Punk/',1050,art + 'punk.png','1')
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)


def browse_songs(name,url,iconimage):
    sort = ['Spotlight Songs','Popular','Most Discussed','Recent Songs','Top Favourited','Top Rated']
    for s in sort:
        if s == 'Spotlight Songs':
            srt='rf'
        if s == 'Popular':
            srt='mp'
        if s == 'Most Discussed':
            srt='md'
        if s == 'Recent Songs':
            srt='mr'
        if s == 'Top Favourited':
            srt='mf'
        if s == 'Top Rated':
            srt='tr'
        url = "http://www.itemvn.com/browse_songs/?sort=%s" % (srt)
        addDir(s,url,1082,art + s.lower().replace(' ','_') + '.png','1')
	
def browse_songs_genre(name,url,iconimage):#http://www.itemvn.com/browse_songs/?sort=tr&genre=&t=t
    addDir('All Genres',"%s&genre=" % url,1081,art + 'all_genres.png','1')
    addDir('Pop',"%s&genre=pop" % url,1081,art + 'pop.png','1')
    addDir('Latin',"%s&genre=latin" % url,1081,art + 'latin.png','1')
    addDir('Country',"%s&genre=country" % url,1081,art + 'country.png','1')
    addDir('Classical',"%s&genre=classical" % url,1081,art + 'classical.png','1')
    addDir('Rock',"%s&genre=rock" % url,1081,art + 'rock.png','1')
    addDir('Electronic',"%s&genre=electronic" % url,1081,art + 'electronic.png','1')
    addDir('Jazz',"%s&genre=jazz" % url,1081,art + 'jazz.png','1')
    addDir('New Age',"%s&genre=newage" % url,1081,art + 'new_age.png','1')
    addDir('R&B',"%s&genre=rb" % url,1081,art + 'r_b.png','1')
    addDir('Alternative',"%s&genre=alternative" % url,1081,art + 'alternative.png','1')
    addDir('Blues',"%s&genre=blues" % url,1081,art + 'blues.png','1')
    addDir('Soundtrack',"%s&genre=soundtrack" % url,1081,art + 'soundtrack.png','1')
    addDir('Hip Hop',"%s&genre=hiphop" % url,1081,art + 'hip_hop.png','1')
    addDir('Metal',"%s&genre=metal" % url,1081,art + 'metal.png','1')
    addDir('Soul',"%s&genre=soul" % url,1081,art + 'soul.png','1')
    addDir('Christmas',"%s&genre=christmas" % url,1081,art + 'christmas.png','1')
    addDir('Rap',"%s&genre=rap" % url,1081,art + 'rap.png','1')
    addDir('Indie',"%s&genre=indie" % url,1081,art + 'indie.png','1')
    addDir('Folk',"%s&genre=folk" % url,1081,art + 'folk.png','1')
    addDir('Teen',"%s&genre=teen" % url,1081,art + 'teen.png','1')
    addDir('Dance',"%s&genre=dance" % url,1081,art + 'dance.png','1')
    addDir('Punk',"%s&genre=punk" % url,1081,art + 'punk.png','1')
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
	
def browse_songs_time(name,url,iconimage):
    addDir('Today',"%s&t=t&page=" % url,1050,art + 'today.png','1')
    addDir('This Week',"%s&t=w&page=" % url,1050,art + 'this_week.png','1')
    addDir('This Month',"%s&t=m&page=" % url,1050,art + 'this_month.png','1')
    addDir('All Time',"%s&t=a&page=" % url,1050,art + 'all_time.png','1')
	
def years(name,url,iconimage):
    cyear = date.today().year
    year = ['2020','2019','2018','2017','2016','2015','2014','2013','2012','2011','2010']
    for y in year:
        url1 = "%s%s/" % (url,y)
        if int(y) <= int(cyear):
            addDir(y,url1,1071,art + y + '.png','1')

def weeks(name,url,iconimage):
    y = int(name)
    cyear = date.today().year
    weeknow = date.today().isocalendar()[1] - 1
    weeks = ['52','51','50','49','48','47','46','45','44','43','42','41','40','39','38','37','36','35','34','33','32','31','30','29','28','27','26','25','24','23','22','21','20','19','18','17','16','15','14','13','12','11','10','9','8','7','6','5','4','3','2','1']
    for w in weeks:
        namewk = "Week-%s" % w
        url1 = "%s%s" % (url,str(namewk))
        url2 = 'http://www.itemvn.com/playlists/hot100/Hot100_%sWeek%s.xml' % (y,w)
        if (y < int(cyear)) or (y == int(cyear) and int(w) <= int(weeknow)):
            if 'topartists' in url:
                addDir(str(namewk),url1,1073,iconimage,'1')
            elif 'hot100' in url:
                addDir(str(namewk),url2,1074,iconimage,'1')
            else:
                addDir(str(namewk),url1,1050,iconimage,'1')

def artisttop(name,url,iconimage):
    link = GET_url(url).replace("'",'"')
    match = re.compile('<a href="(.+?)=(.+?)"><img src="(.+?)" id="listTopArtist(.+?)" class="(.+?)" alt="(.+?)" />').findall(link)
    for au,matchid,thumb,d1,d2,artist in match:
        iconimage = 'http:' + thumb
        artisturl = 'http://www.itemvn.com%s=%s' % (au,matchid)
        addDir(artist, artisturl,1050,iconimage, '1')
	
def song_list(name, url, iconimage):
    link = open_url(url)
    all = regex_get_all(link, '<song>', '</song>')
    for a in all:
        try:
            iconimage = 'http:' + regex_from_to(a, '<cover>', '</cover>')
            songid = regex_from_to(a, "fileName>", "</fileName>")
            title = regex_from_to(a, "<title>", "</title>")
            artist = regex_from_to(a, "<artist>", "</artist>")
        except:
            pass
        addDir(title + ' | ' + artist, "S_" + songid,1100,iconimage, artist)

def artists(url):
    alphabet =  ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U','V', 'W', 'X', 'Y', 'Z']
    for a in alphabet:
        addDir(a, a,1011,art + a.lower() + '.png', '1')

def artists_list(name, url, page):
    nextpage = int(page) + 1
    url1 = 'http://www.itemvn.com/listartist/?letter=%s' % url
    link = GET_url(url1)
    session = regex_from_to(link, 'hiddenSessionToken" value="', '"')
    posturl = 'http://www.itemvn.com/ws/service.asmx/search'
    form_dict = {}
    form_dict['s'] = '%s___itemvnpara______itemvnpara___artistfirstletter___itemvnpara___%s___itemvnpara___%s___itemvnpara___0___itemvnpara___0___itemvnpara___http://www.itemvn.com/justadded/Genre/All/2' % (session,url,page)
    header_dict = {}
    header_dict['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    header_dict['Accept-Language'] = 'en-US,en;q=0.5'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'www.itemvn.com'
    header_dict['Cache-Control'] = 'no-cache'
    header_dict['Pragma'] = 'no-cache'
    header_dict['X-Requested-With'] = 'XMLHttpRequest'
    header_dict['Content-Length'] = '255'
    header_dict['Referer'] = url1
    header_dict['Connection'] = 'keep-alive'
    header_dict['Content-type'] = 'application/json; charset=utf-8'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    req = requests.post(posturl, data=json.dumps(form_dict), headers=header_dict).content
    result = json.loads(req)
    artistdata = result['ST'].encode('utf-8', 'ignore')
    artistids = result['RL']
    all_artist = regex_get_all(artistdata, "<table style='width:100", "</span></span></td>")
    count = -1
    for a in all_artist:
        count = count + 1
        artist = regex_from_to(a, "class='artist' href='#'>", "</a>")
        iconimage = 'http:' + regex_from_to(a, 'src="', '"')
        matchid = re.findall('..........?', artistids)[count]
        artisturl = 'http://www.itemvn.com/artist/?s=%s' % matchid
        addDir(artist, artisturl,1050,iconimage, '1')
    addDir('Next Page >>', url,1011,xbmc.translatePath(os.path.join('special://home/addons/plugin.audio.mp3streams', 'art', name + '.png')), str(nextpage))

def artists_menu(name, url, iconimage, page):
    origurl = url
    if 'justadded' in url or 'browse_songs' in url:
        url = "%s%s" % (url,page)
    if page != 'artists':
        nextpage = int(page) + 1
    link = GET_url(url)
    #try:
        #top_hits = regex_from_to(link, 'hiddenUserID', '<td height="20"')
        #addDir(name + ' - Top Hits', origurl,1100,iconimage, link)
    #except:
        #pass
    if 'browse_songs' in origurl:
        all_albums = regex_from_to(link,'<table id="listSongs', 'input type="submit')
        album = regex_get_all(all_albums, '<td valign="top', '<td style="padding')
    elif 'bestsellers' in origurl:
        all_albums = regex_from_to(link,'<table id="listTopAlbum', '<td class="right_sidebar')
        album = regex_get_all(all_albums, '<table cellpadding', 'album_year')
    else:
        try:
            all_albums = regex_from_to(link,'<table id="tblArtistAlbums', 'table id="grdRelatedArtists"')
        except:
            try:
                all_albums = regex_from_to(link,'<table id="listNewAlbum', 'Pager">Browse')#
            except:
                all_albums = regex_from_to(link,'<table id="listTopSong', '<input type="submit"')
        album = regex_get_all(all_albums, '<table width="1', '</table>')
    for a in album:
        if 'browse_songs' in origurl:
            iconimage = 'http:' + regex_from_to(a, 'data-src="', '"')
            albuminfo = regex_from_to(a, 'class="artist_underline', 'a>')
            albumtitle = regex_from_to(albuminfo, '">', '<')
            try:
                album = albumtitle.split(' - ')[1]
                artist = albumtitle.split(' - ')[0]
            except:
                album = albumtitle
                artist = albumtitle
            albumid = "S_" + regex_from_to(albuminfo, 's=', '">')
        elif not 'bestsellers' in origurl:
            iconimage = 'http:' + regex_from_to(a, 'data-src="', '"')
            albuminfo = regex_from_to(a, 'class="artist_underline', 'a>')
            albumtitle = regex_from_to(albuminfo, '">', '<')
            try:
                album = albumtitle.split(' - ')[1]
                artist = albumtitle.split(' - ')[0]
            except:
                album = albumtitle
                artist = albumtitle
            albumid = regex_from_to(albuminfo, 's=', '">')
            year = regex_from_to(a, "article_writer'>", '<')
        else:
            iconimage = 'http:' + regex_from_to(a, 'img src="', '"')
            albuminfo = regex_from_to(a, 'class="album"', 'a>')
            album = regex_from_to(albuminfo, '">', '<')
            artistinfo = regex_from_to(a, 'class="artist"', 'a>')
            artist = regex_from_to(artistinfo, '">', '<')
            albumtitle = "%s - %s" % (artist, album)
            albumid = regex_from_to(albuminfo, 's=', '">')
        addDir(albumtitle, albumid,1100,iconimage, artist)
    if not 'bestsellers' in origurl and page != 'artists':
        addDir('Next Page >>',origurl,1050,art + 'newalbums.jpg',str(nextpage))
		
def charts():
    addDir('UK Album Chart','http://www.billboard.com/charts/united-kingdom-albums',102,art +'ukalbumchart.jpg','')
    addDir('UK Single Chart - Top 100','http://www.officialcharts.com/singles-chart/',102,art +'uksinglecharttop100.jpg','')
    addDir('BillBoard 200','http://www.billboard.com/charts/billboard-200',102,art +'billboard200.jpg','')
    addDir('Hot 100 Singles','http://www.billboard.com/charts/hot-100',102,art +'hot100singles.jpg','')
    addDir('Country Albums','http://www.billboard.com/charts/country-albums',102,art +'countryalbums.jpg','')
    addDir('HeatSeeker Albums','http://www.billboard.com/charts/heatseekers-albums',102,art +'heatseekeralbums.jpg','')
    addDir('Independent Albums','http://www.billboard.com/charts/independent-albums',102,art +'independentalbums.jpg','')
    addDir('Catalogue Albums','http://www.billboard.com/charts/catalog-albums',102,art +'cataloguealbums.jpg','')
    addDir('Folk Albums','http://www.billboard.com/charts/folk-albums',102,art +'folkalbums.jpg','')
    addDir('Blues Albums','http://www.billboard.com/charts/blues-albums',102,art +'bluesalbums.jpg','')
    addDir('Tastemaker Albums','http://www.billboard.com/charts/tastemaker-albums',102,art +'tastemakeralbums.jpg','')
    addDir('Rock Albums','http://www.billboard.com/charts/rock-albums',102,art +'rockalbums.jpg','')
    addDir('Alternative Albums','http://www.billboard.com/charts/alternative-albums',102,art +'alternativealbums.jpg','')
    addDir('Hard Rock Albums','http://www.billboard.com/charts/hard-rock-albums',102,art +'hardrockalbums.jpg','')
    addDir('Digital Albums','http://www.billboard.com/charts/digital-albums',102,art +'digitalalbums.jpg','')
    addDir('R&B Albums','http://www.billboard.com/charts/r-b-hip-hop-albums',102,art +'randbalbums.jpg','')
    addDir('Top R&B/Hip-Hop Albums','http://www.billboard.com/charts/r-and-b-albums',102,art +'toprandbandhiphop.jpg','')
    addDir('Dance Electronic Albums','http://www.billboard.com/charts/dance-electronic-albums',102,art +'danceandelectronic.jpg','')
	
def chart_lists(name, url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    if "officialcharts" in url:
        all_list = regex_get_all(link, '<tr class="entry">', '</tr>')
        for list in all_list:
            iconimage = regex_from_to(list, '<img src="', '"')
            artist = regex_from_to(list, '<h4>', '</h4>').replace('&#039;',"'")
            title = regex_from_to(list, '<h3>', '</h3>').replace('&#039;',"'")
            addDir(artist.replace('&amp;', '&') + ' - ' + title.replace('&amp;', '&'),'url',26,iconimage,'')
    elif "billboard" in url and '<span class="chart_position' not in link:
        link=link.replace('\n','').replace('\t','')
        match=re.compile('<span class="this-week">(.+?)</span><span class="last-week">(.+?)</span></div><div class="row-image"(.+?)<div class="row-title"><h2>(.+?)</h2><h3><a href="(.+?)" trackaction="Artist Name">(.+?)</a>').findall(link)
        for pos,lw,iconimage,title,artisturl,artist in match:
            text = "%s %s" % (artist, title)
            try:
                iconimage='http://' + regex_from_to(iconimage,'http://','.jpg') + '.jpg'
            except:
                iconimage='http://www.billboard.com/sites/all/themes/bb/images/default/no-album.png'
            if not 'Single' in name and not 'Best Songs of 2014' in text:
                addDir(artist.replace('&amp;', '&') + ' - ' + title.replace('&amp;', '&'),'url',25,iconimage,'')
            elif not 'Best Songs of 2014' in text:
                addDir(artist.replace('&amp;', '&') + ' - ' + title.replace('&amp;', '&'),'url',26,iconimage,'')
    else:
        all_list=regex_get_all(link,'<span class="chart_position','</header>')
        for a in all_list:
            title=regex_from_to(a,'<h1>','</h1>').rstrip()
            try:
                artist=regex_from_to(a,' title="','">').strip()
            except:
                artist=regex_from_to(a,'<p class="chart_info">','</p>').strip()
            try:
                iconimage=regex_from_to(a,'Image" src="','"')
            except:
                iconimage='http://www.billboard.com/sites/all/themes/bb/images/default/no-album.png'
            text = "%s %s" % (artist, title)
            if not 'Single' in name and not 'Best Songs of 2014' in text:
                addDir(artist.replace('&amp;', '&') + ' - ' + title.replace('&amp;', '&'),'url',25,iconimage,'')
            elif not 'Best Songs of 2014' in text:
                addDir(artist.replace('&amp;', '&') + ' - ' + title.replace('&amp;', '&'),'url',26,iconimage,'')
'''
        match = re.compile('"title" : "(.+?)"\r\n.+?"artist" : "(.+?)"\r\n.+?image" : "(.+?)"\r\n.+?"entityId" : ".+?"\r\n.+?"entityUrl" : "(.+?)"').findall(link)
        for title, artist, iconimage, url1 in match:
            text = "%s %s" % (artist, title)
            url='http://www1.billboard.com'+url1+'#'+url1
            if re.search('.gif',iconimage):
                iconimage=""
            if not 'Single' in name:
                addDir(artist.replace('&amp;', '&') + ' - ' + title.replace('&amp;', '&'),'url',25,iconimage,'')
            else:
                addDir(artist.replace('&amp;', '&') + ' - ' + title.replace('&amp;', '&'),'url',26,iconimage,'')
'''
				
def get_song_url(session,url,songid):
    origurl = url
    url = 'http://www.itemvn.com/wsp/service.asmx'
    header_dict = {}
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header_dict['Accept-Language'] = 'en-US,en;q=0.5'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'www.itemvn.com'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Content-type'] = 'text/xml; charset=utf-8'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    xml = '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"> <soap:Body> <mps xmlns="http://www.itemvn.com/"> <t>%s</t> <s>%s</s> <p/> <d>%s</d> </mps> </soap:Body> </soap:Envelope>' % (session, songid, origurl)
    req = requests.post(url, data=xml, headers=header_dict).text
    songurl = regex_from_to(req, '<mpsResult>', '</mpsResult>')
    print songurl
    return songurl
        
    	
def play_album(name, url, iconimage,mix,clear, artist):
    if url.startswith('s_'):
        url=url.upper()
    tophitlink = artist
    urlorig = url
    try:
        artist = artist.replace('%20',' ')
    except:
        pass
    stripartist = "%s - " % artist
    if url.startswith("S_"):
        xurl = 'http://www.itemvn.com/song/?s=%s' % url.replace('S_','')
    elif 'Top hits' in name:
        xurl = urlorig
    else:
        xurl = 'http://www.itemvn.com/album/?s=%s' % url
    browse=False
    playlist=[]
    dialog = xbmcgui.Dialog()
    if mode != 6 and mix != 'mix' and mix != 'queue' and not urlorig.startswith("S_"):
        if dialog.yesno("Bin@ural", 'Browse songs or play full album?', '', '', 'Play Now','Browse'):
            browse=True
    if browse == True:
        dp = xbmcgui.DialogProgress()
        dp.create("Bin@ural",'Adding Tracks')
        dp.update(0)
        if 'Top Hits' not in name:
            link = GET_url(xurl).translate(trans_table)
            session = regex_from_to(link,'hiddenSessionToken" value="', '"')
            albumurl='http://www.itemvn.com' + regex_from_to(link, 'configURL=', '.xml') + '.xml'
            link = open_url(albumurl).translate(trans_table)
            tracks = regex_get_all(link, '<song>', '</song>')
        else:
            session = regex_from_to(tophitlink,'hiddenSessionToken" value="', '"')
            tracks = regex_get_all(tophitlink, '<span id="grdHits', '<td width=')
        nItem=len(tracks)
        trn=0
        for t in tracks:
            trn+=1
            songid = regex_from_to(t, '<fileName>', '</fileName>')
            songname = regex_from_to(t, '<title>', '</title>')
            dur = regex_from_to(t,'<length>', '</length>')
            dur = int(dur)
            album = name.replace(stripartist, '')
            title = "%s. %s" % (trn, songname)
            stored_path = os.path.join(MUSIC_DIR,  artist, album, title + '.mp3')
            stored_path1 = os.path.join(MUSIC_DIR,  artist, album, title + '.wma')
            if os.path.exists(stored_path):
                url = stored_path
            elif os.path.exists(stored_path1):
                url = stored_path1
            else:
                url = get_song_url(session,xurl,songid)
            addDirAudio(title,url,10,iconimage,songname,artist,album,str(dur),'S_'+songid)
            liz=xbmcgui.ListItem(songname, iconImage=iconimage, thumbnailImage=iconimage)
            liz.setInfo('music', {'Title':songname, 'Artist':artist, 'Album':album, 'duration':dur })
            liz.setProperty('mimetype', 'audio/mpeg')
            liz.setProperty("IsPlayable","true")
            liz.setThumbnailImage(iconimage)
            if HIDE_FANART == False:
                liz.setProperty('fanart_image', "")
            playlist.append((url, liz))
            progress = len(playlist) / float(nItem) * 100               
            dp.update(int(progress), 'Adding Track: ',title)
            if dp.iscanceled():
                return
				
    else:
        if mix != 'mix':
            dp = xbmcgui.DialogProgress()
            dp.create("Bin@ural",'Creating Your Playlist')
            dp.update(0)
        pl = get_XBMCPlaylist(clear)
        link = GET_url(xurl).translate(trans_table)
        session = regex_from_to(link,'hiddenSessionToken" value="', '"')
        if urlorig.startswith("S_"):
            songid = urlorig.replace('S_','')
            songname = name.split(' | ')[0]
            dur = ""
            album = "Singles"
            title = songname
            stored_path = os.path.join(MUSIC_DIR,  artist, album, title + '.mp3')
            stored_path1 = os.path.join(MUSIC_DIR,  artist, album, title + '.wma')
            if os.path.exists(stored_path):
                url = stored_path
            elif os.path.exists(stored_path1):
                url = stored_path1
            else:
                url = get_song_url(session,xurl,songid)
            addDirAudio(title,url,10,iconimage,songname,artist,album,str(dur),'S_'+songid)
            liz=xbmcgui.ListItem(songname, iconImage=iconimage, thumbnailImage=iconimage)
            liz.setInfo('music', {'Title':songname, 'Artist':artist, 'Album':album, 'duration':dur })
            liz.setProperty('mimetype', 'audio/mpeg')
            liz.setProperty("IsPlayable","true")
            liz.setThumbnailImage(iconimage)
            if HIDE_FANART == False:
                liz.setProperty('fanart_image', "")
            playlist.append((url, liz))
        else:
            albumurl='http://www.itemvn.com' + regex_from_to(link, 'configURL=', '.xml') + '.xml'
            link = open_url(albumurl).translate(trans_table)
            tracks = regex_get_all(link, '<song>', '</song>')
            nItem=len(tracks)
            trn=0
            for t in tracks:
                trn+=1
                songid = regex_from_to(t, '<fileName>', '</fileName>')
                songname = regex_from_to(t, '<title>', '</title>')
                dur = regex_from_to(t,'<length>', '</length>')
                dur = int(dur)
                album = name.replace(stripartist, '')
                title = "%s. %s" % (trn, songname)
                stored_path = os.path.join(MUSIC_DIR,  artist, album, title + '.mp3')
                stored_path1 = os.path.join(MUSIC_DIR,  artist, album, title + '.wma')
                if os.path.exists(stored_path):
                    url = stored_path
                elif os.path.exists(stored_path1):
                    url = stored_path1
                else:
                    url = get_song_url(session,xurl,songid)
                addDirAudio(title,url,10,iconimage,songname,artist,album,str(dur),'S_'+songid)
                liz=xbmcgui.ListItem(songname, iconImage=iconimage, thumbnailImage=iconimage)
                liz.setInfo('music', {'Title':songname, 'Artist':artist, 'Album':album, 'duration':dur })
                liz.setProperty('mimetype', 'audio/mpeg')
                liz.setProperty("IsPlayable","true")
                liz.setThumbnailImage(iconimage)
                if HIDE_FANART == False:
                    liz.setProperty('fanart_image', "")
                playlist.append((url, liz))
			
                if mix != 'mix':
                    progress = len(playlist) / float(nItem) * 100               
                    dp.update(int(progress), 'Adding to Your Playlist',title)
                    if dp.iscanceled():
                        return

  
        for blob ,liz in playlist:
            try:
                if blob:
                    pl.add(blob,liz)
            except:
                pass
        if clear or (not xbmc.Player().isPlayingAudio()):
            xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER).play(pl)
				
def play_song(url,name,songname,artist,album,iconimage,dur,clear):
    stored_path = os.path.join(MUSIC_DIR,  artist, album, name + '.mp3')
    stored_path1 = os.path.join(MUSIC_DIR,  artist, album, name + '.wma')
    dialog = xbmcgui.Dialog()
    show_name=name
    playlist=[]
    pl = get_XBMCPlaylist(clear)
    if os.path.exists(stored_path):
        url1 = stored_path
    elif os.path.exists(stored_path1):
        url1 = stored_path1
    else:
        url1=str(url)
    liz=xbmcgui.ListItem(show_name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo('music', {'Title':songname, 'Artist':artist, 'Album':album, 'duration':dur})
    liz.setProperty('mimetype', 'audio/mpeg')
    liz.setThumbnailImage(iconimage)
    if HIDE_FANART == True:
        liz.setProperty('fanart_image', "")
    playlist.append((url1, liz))
    for blob ,liz in playlist:
        try:
            if blob:
                pl.add(blob,liz)
        except:
            pass
    if clear or (not xbmc.Player().isPlayingAudio()):
        xbmc.Player().play(pl)
		
def search(name, url):
    keyboard = xbmc.Keyboard('', name, False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
        if len(query) > 0:
            if name == 'Search Artists':
                search_artists(query)
            elif name == 'Search Albums':
                search_albums(query)
            elif name == 'Search Songs':
                search_songs(query,'1')
				
def play_moods(name, url, iconimage,mix,clear,page):
    pageurl = url
    url = url + page
    nextpage = "%s%s" % (url, int(page) + 1)
    nextquery = int(page) + 2
    browse=False
    playlist=[]
    dialog = xbmcgui.Dialog()
    if mode != 6 and mix != 'mix' and mix != 'queue':
        if dialog.yesno("Bin@ural", 'Browse songs or play full album?', '', '', 'Play Now','Browse'):
            browse=True
    if browse == True:
        link = open_url(url).replace('\/','/')
        link2 = open_url(nextpage).replace('\/','/')
        link = link + link2
        match = re.compile('location":"(.+?)","title":"(.+?)","creator":"(.+?)"(.+?)"image":"(.+?)","trackNum":"(.+?)"').findall(link)
        for url,songname,artist,album,iconimage,track in match:
            songname = songname.replace('&amp;', 'and')
            artist = artist.replace('&amp;', 'and')
            album = album.replace('&amp;', 'and')
            trn = track.replace('track','')
            title = "%s - %s" % (artist, songname)
            addDirAudio(title,url,10,iconimage,songname,artist,album,"a",'a')
            liz=xbmcgui.ListItem(songname, iconImage=iconimage, thumbnailImage=iconimage)
            liz.setInfo('music', {'Title':songname, 'Artist':artist, 'Album':album })
            liz.setProperty('mimetype', 'audio/mpeg')
            liz.setProperty("IsPlayable","true")
            liz.setThumbnailImage(iconimage)
            liz.setProperty('fanart_image', fanart)
            playlist.append((url, liz))
				
    else:
        if mix != 'mix':
            dp = xbmcgui.DialogProgress()
            dp.create("Bin@ural",'Creating Your Playlist')
            dp.update(0)
        pl = get_XBMCPlaylist(clear)
        link = open_url(url).replace('\/','/')
        link2 = open_url(nextpage).replace('\/','/')
        link = link + link2
        match = re.compile('location":"(.+?)","title":"(.+?)","creator":"(.+?)"(.+?)"image":"(.+?)","trackNum":"(.+?)"').findall(link)
        nItem=len(match)
        for url,songname,artist,album,iconimage,track in match:
            songname = songname.replace('&amp;', 'and')
            artist = artist.replace('&amp;', 'and')
            album = album.replace('&amp;', 'and')
            trn = track.replace('track','')
            title = "%s - %s" % (artist, songname)
            addDirAudio(title,url,10,iconimage,songname,artist,album,"",'')
            liz=xbmcgui.ListItem(songname, iconImage=iconimage, thumbnailImage=iconimage)
            liz.setInfo('music', {'Title':songname, 'Artist':artist, 'Album':album})
            liz.setProperty('mimetype', 'audio/mpeg')
            liz.setProperty("IsPlayable","true")
            liz.setThumbnailImage(iconimage)
            liz.setProperty('fanart_image', fanart)
            playlist.append((url, liz))
			
            if mix != 'mix':
                progress = len(playlist) / float(nItem) * 100               
                dp.update(int(progress), 'Adding to Your Mood',title)
                if dp.iscanceled():
                    return

  
        for blob ,liz in playlist:
            try:
                if blob:
                    pl.add(blob,liz)
            except:
                pass
        if clear or (not xbmc.Player().isPlayingAudio()):
            xbmc.Player(xbmc.PLAYER_CORE_PAPLAYER).play(pl)
    addDir("Queue Next Page >>",pageurl,1206,iconimage,str(nextquery))
				
def search_artists(query):
    form_dict = {}
    url1 = 'http://www.itemvn.com/listartist/?keyword=%s' % urllib.quote_plus(query)
    link = GET_url(url1)
    session = regex_from_to(link, 'hiddenSessionToken" value="', '"')
    posturl = 'http://www.itemvn.com/ws/service.asmx/search'
    form_dict['s'] = '%s___itemvnpara______itemvnpara___artist___itemvnpara___%s___itemvnpara___1___itemvnpara___1___itemvnpara___0___itemvnpara___http://www.itemvn.com/' % (session,query)
    header_dict = {}
    header_dict['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    header_dict['Accept-Language'] = 'en-US,en;q=0.5'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'www.itemvn.com'
    header_dict['Cache-Control'] = 'no-cache'
    header_dict['Pragma'] = 'no-cache'
    header_dict['X-Requested-With'] = 'XMLHttpRequest'
    header_dict['Content-Length'] = '201'
    header_dict['Referer'] = url1
    header_dict['Connection'] = 'keep-alive'
    header_dict['Content-type'] = 'application/json; charset=utf-8'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    req = requests.post(posturl, data=json.dumps(form_dict), headers=header_dict).content
    result = json.loads(req)
    artistdata = result['ST'].encode('utf-8', 'ignore')
    artistids = result['RL']
    all_artist = regex_get_all(artistdata, "<table style='width:100", "</span></span></td>")
    count = -1
    for a in all_artist:
        count = count + 1
        artist = regex_from_to(a, "class='artist' href='#'>", "</a>")
        iconimage = 'http:' + regex_from_to(a, 'src="', '"')
        matchid = re.findall('..........?', artistids)[count]
        artisturl = 'http://www.itemvn.com/artist/?s=%s' % matchid
        addDir(artist, artisturl,1050,iconimage, 'artists')

def search_albums(query):
    form_dict = {}
    url1 = 'http://www.itemvn.com/listalbum/?keyword=%s' % urllib.quote_plus(query)
    link = GET_url(url1)
    session = regex_from_to(link, 'hiddenSessionToken" value="', '"')
    posturl = 'http://www.itemvn.com/ws/service.asmx/search'
    form_dict['s'] = '%s___itemvnpara______itemvnpara___album___itemvnpara___%s___itemvnpara___1___itemvnpara___1___itemvnpara___0___itemvnpara___http://www.itemvn.com/' % (session,query)
    header_dict = {}
    header_dict['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    header_dict['Accept-Language'] = 'en-US,en;q=0.5'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'www.itemvn.com'
    header_dict['Cache-Control'] = 'no-cache'
    header_dict['Pragma'] = 'no-cache'
    header_dict['X-Requested-With'] = 'XMLHttpRequest'
    header_dict['Content-Length'] = '201'
    header_dict['Referer'] = url1
    header_dict['Connection'] = 'keep-alive'
    header_dict['Content-type'] = 'application/json; charset=utf-8'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    req = requests.post(posturl, data=json.dumps(form_dict), headers=header_dict).content
    result = json.loads(req)
    artistdata = result['ST'].encode('utf-8', 'ignore')
    albumids = result['AL']
    all_artist = regex_get_all(artistdata, "<table style='width:100", "</span></span></td>")
    count = -1
    for a in all_artist:
        count = count + 1
        title = regex_from_to(a, "class='artist_underline' href='#'>", "</a>")
        try:
            artist=title.split(' - ')[0]
        except:
            artist=title
        iconimage = 'http:' + regex_from_to(a, 'src="', '"')
        matchid = re.findall('..........?', albumids)[count]
        artisturl = 'http://www.itemvn.com/artist/?s=%s' % matchid
        addDir(title, matchid,1100,iconimage, artist)
		
def search_songs(query,page):
    form_dict = {}
    if '>>' in query:
        query=query.split(' >> ')[1]
    url1 = 'http://www.itemvn.com/listsong/?keyword=%s&page=%s' % (urllib.quote_plus(query),page)
    nextpage=int(page)+1
    link = GET_url(url1)
    session = regex_from_to(link, 'hiddenSessionToken" value="', '"')
    posturl = 'http://www.itemvn.com/ws/service.asmx/search'
    form_dict['s'] = '%s___itemvnpara______itemvnpara___song___itemvnpara___%s___itemvnpara___%s___itemvnpara___0___itemvnpara___1___itemvnpara___http://www.itemvn.com/' % (session,query,page)
    header_dict = {}
    header_dict['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    header_dict['Accept-Language'] = 'en-US,en;q=0.5'
    header_dict['Accept-Encoding'] = 'gzip, deflate'
    header_dict['Host'] = 'www.itemvn.com'
    header_dict['Cache-Control'] = 'no-cache'
    header_dict['Pragma'] = 'no-cache'
    header_dict['X-Requested-With'] = 'XMLHttpRequest'
    header_dict['Content-Length'] = '201'
    header_dict['Referer'] = url1
    header_dict['Connection'] = 'keep-alive'
    header_dict['Content-type'] = 'application/json; charset=utf-8'
    header_dict['User-Agent'] = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    req = requests.post(posturl, data=json.dumps(form_dict), headers=header_dict).content
    result = json.loads(req)
    artistdata = result['ST'].encode('utf-8', 'ignore')
    albumids = result['SS']
    all_artist = regex_get_all(artistdata, "<table style='width:100", "</span></span></td>")
    count = -1
    for a in all_artist:
        count = count + 1
        title = regex_from_to(a, "class='artist_underline' href='#'>", "</a>")
        try:
            artist=title.split(' - ')[0]
        except:
            artist=title
        iconimage = 'http:' + regex_from_to(a, 'src="', '"')
        matchid = 'S_' + re.findall('..........?', albumids)[count]
        artisturl = 'http://www.itemvn.com/artist/?s=%s' % matchid
        addDir(title, matchid,1100,iconimage, artist)
    addDir('Next page >> ' + query, 'url',26,iconart, str(nextpage))
		

def download_song(url,name,songname,artist,album,iconimage):
    track = songname[:songname.find('.')]
    format = url[-4:]
    artist_path = create_directory(MUSIC_DIR, artist)
    album_path = create_directory(artist_path, album)
    list_data = "%s<>%s<>%s<>%s<>%s%s" % (album_path,artist,album,track,songname,format)	
    local_filename = album_path + '/' + songname + format
    urllib.urlretrieve(url, local_filename)
    notification(artist + ' ' + songname, 'Single download finished', '3000', iconimage)

def download_album(url,name,iconimage,artist):
    stripartist = "%s - " % artist
    xurl = 'http://www.itemvn.com/album/?s=%s' % url
    dialog = xbmcgui.Dialog()
    playlist=[]
    notification(name, 'Download started', '3000', iconimage)
    link = GET_url(xurl).translate(trans_table)
    session = regex_from_to(link,'hiddenSessionToken" value="', '"')
    albumurl='http://www.itemvn.com' + regex_from_to(link, 'configURL=', '.xml') + '.xml'
    link = open_url(albumurl).translate(trans_table)
    tracks = regex_get_all(link, '<song>', '</song>')
    nSong=len(tracks)
    trn=0
    for t in tracks:
        trn+=1
        songid = regex_from_to(t, '<fileName>', '</fileName>')
        songname = regex_from_to(t, '<title>', '</title>')
        dur = regex_from_to(t,'<length>', '</length>')
        dur = int(dur)
        album = name.replace(stripartist, '').replace('/', '')
        title = "%s. %s" % (trn, songname.replace('/', ''))
        url = get_song_url(session,xurl,songid)
        artist_path = create_directory(MUSIC_DIR, artist)
        album_path = create_directory(artist_path, album)
        list_data = "%s<>%s<>%s<>%s<>%s%s" % (album_path,artist,album,trn,title,'.mp3')
        local_filename = album_path + '/' + title + '.mp3'
        urllib.urlretrieve(url, local_filename)
    notification(artist + ' ' + album, 'Album download finished', '3000', iconimage)

		
		
def instant_mix():
    menu_texts = []
    menu_texts.append("All Songs")
    dialog = xbmcgui.Dialog()
    if os.path.isfile(FAV_SONG):
        s = read_from_file(FAV_SONG)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                try:
                    plname = list1[3]
                    if not plname in menu_texts:
                        menu_texts.append(plname)
                except:
                    if not "Ungrouped" in menu_texts:
                        menu_texts.append("Ungrouped")
    menu_id = dialog.select('Select Group', menu_texts)
    if(menu_id < 0):
        return (None, None)
        dialog.close()
    groupname = menu_texts[menu_id]
    shuffleThread = ShuffleSongThread(groupname)
    shuffleThread.start()

class ShuffleSongThread(Thread):
    def __init__(self,groupname):
        self.groupname=groupname
        Thread.__init__(self)

    def run(self):
        groupname=self.groupname        
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        playlist.clear()
        if os.path.isfile(FAV_SONG):
            s = read_from_file(FAV_SONG)
            search_list = s.split('\n')
            for list in search_list:
                if list != '':
                    list1 = list.split('<>')
                    title = list1[0]
                    try:
                        artist=title.split(' - ')[0]
                    except:
                        artist = title
                    albumid = list1[1]
                    iconimage = list1[2]
                    try:
                        plname = list1[3]
                    except:
                        plname = "Ungrouped"
                    if (plname == groupname) or groupname == "All Songs":
                        play_album(title, albumid, iconimage,'mix',False,artist)
                    time.sleep(5)
            playlist.shuffle()
	
def instant_mix_album():
    menu_texts = []
    menu_texts.append("All Albums")
    dialog = xbmcgui.Dialog()
    if os.path.isfile(FAV_ALBUM):
        s = read_from_file(FAV_ALBUM)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                try:
                    plname = list1[3]
                    if not plname in menu_texts:
                        menu_texts.append(plname)
                except:
                    if not "Ungrouped" in menu_texts:
                        menu_texts.append("Ungrouped")
    menu_id = dialog.select('Select Group', menu_texts)
    if(menu_id < 0):
        return (None, None)
        dialog.close()
    groupname = menu_texts[menu_id]
    shuffleThread = ShuffleAlbumThread(groupname)
    shuffleThread.start()

class ShuffleAlbumThread(Thread):
    def __init__(self,groupname):
        self.groupname=groupname
        Thread.__init__(self)

    def run(self):
        groupname=self.groupname        
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        playlist.clear()
        if os.path.isfile(FAV_ALBUM):
            s = read_from_file(FAV_ALBUM)
            search_list = s.split('\n')
            for list in search_list:
                if list != '':
                    list1 = list.split('<>')
                    title = list1[0]
                    try:
                        artist=title.split(' - ')[0]
                    except:
                        artist = title
                    albumid = list1[1]
                    iconimage = list1[2]
                    try:
                        plname = list1[3]
                    except:
                        plname = "Ungrouped"
                    if (plname == groupname) or groupname == "All Albums":
                        play_album(title, albumid, iconimage,'mix',False,artist)
                        playlist.shuffle()
                    time.sleep(15)

def favourite_artists():
    menu_texts = []
    menu_texts.append("All Artists")
    dialog = xbmcgui.Dialog()
    if os.path.isfile(FAV_ALBUM):
        s = read_from_file(FAV_ALBUM)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                try:
                    plname = list1[3]
                    if not plname in menu_texts:
                        menu_texts.append(plname)
                except:
                    if not "Ungrouped" in menu_texts:
                        menu_texts.append("Ungrouped")
    menu_id = dialog.select('Select Group', menu_texts)
    if(menu_id < 0):
        return (None, None)
        dialog.close()
    groupname = menu_texts[menu_id]
    if os.path.isfile(FAV_ARTIST):
        s = read_from_file(FAV_ARTIST)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                url = list1[1]
                iconimage = list1[2]
                try:
                    plname = list1[3]
                except:
                    plname = "Ungrouped"
                if (plname == groupname) or groupname == "All Artists":
                    addDir(title, url,1050,iconimage, 'artists')
       
				
def favourite_albums():
    menu_texts = []
    menu_texts.append("All Albums")
    dialog = xbmcgui.Dialog()
    if os.path.isfile(FAV_ALBUM):
        s = read_from_file(FAV_ALBUM)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                try:
                    plname = list1[3]
                    if not plname in menu_texts:
                        menu_texts.append(plname)
                except:
                    if not "Ungrouped" in menu_texts:
                        menu_texts.append("Ungrouped")
    menu_id = dialog.select('Select Group', menu_texts)
    if(menu_id < 0):
        return (None, None)
        dialog.close()
    groupname = menu_texts[menu_id]
    if os.path.isfile(FAV_ALBUM):
        s = read_from_file(FAV_ALBUM)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                try:
                    artist=title.split(' - ')[0]
                except:
                    artist = title
                albumid = list1[1]
                iconimage = list1[2]
                try:
                    plname = list1[3]
                except:
                    plname = "Ungrouped"
                if (plname == groupname) or groupname == "All Albums":
                    addDir(title, albumid,1100,iconimage, 'qq'+list)
				
def favourite_songs():
    menu_texts = []
    menu_texts.append("All Songs")
    dialog = xbmcgui.Dialog()
    if os.path.isfile(FAV_SONG):
        s = read_from_file(FAV_SONG)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                try:
                    plname = list1[3]
                    if not plname in menu_texts:
                        menu_texts.append(plname)
                except:
                    if not "Ungrouped" in menu_texts:
                        menu_texts.append("Ungrouped")
    menu_id = dialog.select('Select Group', menu_texts)
    if(menu_id < 0):
        return (None, None)
        dialog.close()
    groupname = menu_texts[menu_id]
	
    if os.path.isfile(FAV_SONG):
        s = read_from_file(FAV_SONG)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                try:
                    artist=title.split(' - ')[0]
                    songname=title.split(' - ')[1]
                except:
                    artist = title
                    songname=title
                url = list1[1]
                iconimage = list1[2]
                try:
                    plname = list1[3]
                except:
                    plname = "Ungrouped"
                if (plname == groupname) or groupname == "All Songs":
                    addDirAudio(title,url,1100,iconimage,songname,artist,'',list,'favsong')
					
def favourite_videoartists():
    menu_texts = []
    menu_texts.append("All Artists")
    dialog = xbmcgui.Dialog()
    if os.path.isfile(FAV_VIDEOARTIST):
        s = read_from_file(FAV_VIDEOARTIST)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                try:
                    plname = list1[3]
                    if not plname in menu_texts:
                        menu_texts.append(plname)
                except:
                    if not "Ungrouped" in menu_texts:
                        menu_texts.append("Ungrouped")
    menu_id = dialog.select('Select Group', menu_texts)
    if(menu_id < 0):
        return (None, None)
        dialog.close()
    groupname = menu_texts[menu_id]
    if os.path.isfile(FAV_VIDEOARTIST):
        s = read_from_file(FAV_VIDEOARTIST)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                url = list1[1]
                iconimage = list1[2]
                try:
                    plname = list1[3]
                except:
                    plname = "Ungrouped"
                if (plname == groupname) or groupname == "All Artists":
                    addDir(title,url,1314,iconimage,'artists')
					
def favourite_videos():
    menu_texts = []
    menu_texts.append("All Songs")
    dialog = xbmcgui.Dialog()
    if os.path.isfile(FAV_VIDEO):
        s = read_from_file(FAV_VIDEO)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                try:
                    plname = list1[3]
                    if not plname in menu_texts:
                        menu_texts.append(plname)
                except:
                    if not "Ungrouped" in menu_texts:
                        menu_texts.append("Ungrouped")
    menu_id = dialog.select('Select Group', menu_texts)
    if(menu_id < 0):
        return (None, None)
        dialog.close()
    groupname = menu_texts[menu_id]
	
    if os.path.isfile(FAV_VIDEO):
        s = read_from_file(FAV_VIDEO)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                title = list1[0]
                try:
                    artist=title.split(' - ')[0]
                    songname=title.split(' - ')[1]
                except:
                    artist = title
                    songname=title
                url = list1[1]
                iconimage = list1[2]
                try:
                    plname = list1[3]
                except:
                    plname = "Ungrouped"
                if (plname == groupname) or groupname == "All Songs":
                    title = "[COLOR gold]%s[/COLOR] | [COLOR cyan]%s[/COLOR]" % (artist,songname)
                    addDirVideo(title,url,1320,iconimage,songname,artist,'','','favvid')

def add_favourite(name, url, iconimage, dir, text):
    data = "%s<>%s<>%s" % (name,url,iconimage)
    menu_texts = []
    menu_texts.append("Add New Group")
    dialog = xbmcgui.Dialog()
    if os.path.isfile(dir):
        s = read_from_file(dir)
        search_list = s.split('\n')
        for list in search_list:
            if list != '':
                list1 = list.split('<>')
                try:
                    plname = list1[3]
                    if not plname in menu_texts:
                        menu_texts.append(plname)
                except:
                    pass
    menu_id = dialog.select('Select Group', menu_texts)
    if(menu_id < 0):
        return (None, None)
        dialog.close()
    if (menu_id == 0):
        keyboard = xbmc.Keyboard('', 'Create New Group', False)
        keyboard.doModal()
        if keyboard.isConfirmed():
            query = keyboard.getText()
            if len(query) > 0:
                plname = query
    else:
        plname = menu_texts[menu_id]
    data_add = "%s<>%s" % (data, plname)
    if 'artist' in dir:
        add_to_list(data_add, dir, True)
    else:
        add_to_list(data_add, dir, False)
    notification(name, "[COLOR lime]" + text + "[/COLOR]", '5000', iconimage)
	
def remove_from_favourites(name, url, iconimage,dir, text):
    url=url.replace('qq','')
    splitdata = url.split('<>')
    artist = splitdata[0]
    url1 = splitdata[1]
    thumb = splitdata[2]
    remove_from_list(url, dir)
    notification(name.upper(), "[COLOR orange]" + text + "[/COLOR]", '5000', thumb)

def find_list(query, search_file):
    try:
        content = read_from_file(search_file) 
        lines = content.split('\n')
        index = lines.index(query)
        return index
    except:
        return -1
		
def add_to_list(list, file, refresh):
    if find_list(list, file) >= 0:
        return

    if os.path.isfile(file):
        content = read_from_file(file)
    else:
        content = ""

    lines = content.split('\n')
    s = '%s\n' % list
    for line in lines:
        if len(line) > 0:
            s = s + line + '\n'
    write_to_file(file, s)
    if refresh == True:
        xbmc.executebuiltin("Container.Refresh")
    
def remove_from_list(list, file):
    list = list.replace('<>Ungrouped', '').replace('All Songs', '')
    index = find_list(list, file)
    if index >= 0:
        content = read_from_file(file)
        lines = content.split('\n')
        lines.pop(index)
        s = ''
        for line in lines:
            if len(line) > 0:
                s = s + line + '\n'
        write_to_file(file, s)
        if not 'song' in file and not 'album' in file:
            xbmc.executebuiltin("Container.Refresh")
		
def write_to_file(path, content, append=False, silent=False):
    try:
        if append:
            f = open(path, 'a')
        else:
            f = open(path, 'w')
        f.write(content)
        f.close()
        return True
    except:
        if not silent:
            print("Could not write to " + path)
        return False

def read_from_file(path, silent=False):
    try:
        f = open(path, 'r')
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            print("Could not read from " + path)
        return None
		
def notification(title, message, ms, nart):
    xbmc.executebuiltin("XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")")
		
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


def get_XBMCPlaylist(clear):
    pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    if clear:
        pl.clear()
    return pl
	
def clear_playlist():
    pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    pl.clear()
    notification('Playlist', 'Cleared', '2000', iconart)

	
def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def create_file(dir_path, file_name=None):
    if file_name:
        file_path = os.path.join(dir_path, file_name)
    file_path = file_path.strip()
    if not os.path.exists(file_path):
        f = open(file_path, 'w')
        f.write('')
        f.close()
    return file_path
	
def regex_from_to(text, from_string, to_string, excluding=True):
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r
	
def setView(content, viewType):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]), content)

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage,artist):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&artist="+urllib.quote_plus(artist)
        ok=True
        type1=artist
        artist = artist.replace('qq','')
        suffix = ""
        if artist == "artists":
            list = "%s<>%s" % (str(name),url)
        else:
            if 'qq' in type1:
                spltype1 = type1.split('qq')
                list = "%s<>%s<>%s<>%s" % (str(name).lower(),url,str(iconimage),spltype1[0])
            else:
                list = "%s<>%s<>%s" % (str(name).lower(),url,str(iconimage))
        list = list.replace(',', '')
        
        contextMenuItems = []
        if artist == "videoartist":
            if find_list(list, FAV_VIDEOARTIST) < 0:
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to Favourite Artists[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=1327&iconimage=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from Favourite Artists[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=1328&iconimage=%s)'%(sys.argv[0], name, urllib.quote(url), urllib.quote(iconimage))))
        if artist == "artists":
            if find_list(list, FAV_ARTIST) < 0:
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to Favourite Artists[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=61&iconimage=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from Favourite Artists[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=62&iconimage=%s)'%(sys.argv[0], name, urllib.quote(url), urllib.quote(iconimage))))
        if len(artist)>2 and artist != "videoartist" and 'itemvn' not in url:
            download_album = '%s?name=%s&url=%s&iconimage=%s&artist=%s&mode=202' % (sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage),urllib.quote(artist))  
            contextMenuItems.append(('[COLOR cyan]Download Album[/COLOR]', 'XBMC.RunPlugin(%s)' % download_album))
            if QUEUE_ALBUMS:
                play_music = '%s?name=%s&url=%s&iconimage=%s&mode=7' % (sys.argv[0], urllib.quote(name), url, iconimage)  
                contextMenuItems.append(('[COLOR cyan]Play/Browse Album[/COLOR]', 'XBMC.RunPlugin(%s)' % play_music))
            else:
                queue_music = '%s?name=%s&url=%s&iconimage=%s&mode=6&artist=%s' % (sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage), urllib.quote(artist))  
                contextMenuItems.append(('[COLOR cyan]Queue[/COLOR]', 'XBMC.RunPlugin(%s)' % queue_music))
            if not 'qq' in type1:
                suffix = ""
                contextMenuItems.append(("[COLOR lime]Add to Favourite Albums[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=64&iconimage=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(url), urllib.quote(iconimage))))
            else:
                suffix = ' [COLOR lime]+[/COLOR]'
                contextMenuItems.append(("[COLOR orange]Remove from Favourite Albums[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=65&iconimage=%s)'%(sys.argv[0], urllib.quote(name), urllib.quote(artist), urllib.quote(iconimage))))
        liz=xbmcgui.ListItem(name + suffix, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDirAudio(name,url,mode,iconimage,songname,artist,album,dur,type):
        suffix = ""
        if 'qq' in dur:
            list = "%s<>%s<>%s<>%s<>%s<>%s" % (str(artist),str(album),str(songname).lower(),url,str(iconimage),str(dur).replace('qq',''))
        else:
            list = "%s<>%s<>%s<>%s<>%s" % (str(artist),str(album),str(songname).lower(),url,str(iconimage))
        list = list.replace(',', '')
        artistsong = "%s - %s" % (artist,songname)
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&songname="+urllib.quote_plus(songname)+"&artist="+urllib.quote_plus(artist)+"&album="+urllib.quote_plus(album)+"&dur="+str(dur)+"&type="+str(type)
        ok=True
        download_song = '%s?name=%s&url=%s&iconimage=%s&songname=%s&artist=%s&album=%s&mode=201' % (sys.argv[0], songname, url, iconimage,name,artist,album)  
        contextMenuItems.append(('[COLOR cyan]Download Song[/COLOR]', 'XBMC.RunPlugin(%s)' % download_song))
        if QUEUE_SONGS:
            play_song = '%s?name=%s&url=%s&iconimage=%s&songname=%s&artist=%s&album=%s&dur=%s&mode=18' % (sys.argv[0], urllib.quote(songname), url, iconimage,songname,artist,album,dur)  
            contextMenuItems.append(('[COLOR cyan]Play Song[/COLOR]', 'XBMC.RunPlugin(%s)' % play_song))
        else:
            queue_song = '%s?name=%s&url=%s&iconimage=%s&songname=%s&artist=%s&album=%s&dur=%s&mode=11' % (sys.argv[0], urllib.quote(songname), url, iconimage,songname,artist,album,dur)  
            contextMenuItems.append(('[COLOR cyan]Queue Song[/COLOR]', 'XBMC.RunPlugin(%s)' % queue_song))
        if type != 'favsong':
            suffix = ""
            contextMenuItems.append(("[COLOR lime]Add to Favourite Songs[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=67&iconimage=%s)'%(sys.argv[0], urllib.quote(artistsong), urllib.quote(type), urllib.quote(iconimage))))
        else:
            suffix = ' [COLOR lime]+[/COLOR]'
            contextMenuItems.append(("[COLOR orange]Remove from Favourite Songs[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=68&iconimage=%s)'%(sys.argv[0], urllib.quote(artistsong), urllib.quote(dur), urllib.quote(iconimage))))
        liz=xbmcgui.ListItem(name + suffix, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.setInfo( type="Audio", infoLabels={ "Title": name } )
        if HIDE_FANART == False:
            liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
		
def addDirVideo(name,url,mode,iconimage,songname,artist,album,dur,type):
        suffix = ""
        if 'qq' in dur:
            list = "%s<>%s<>%s<>%s<>%s<>%s" % (str(artist),str(album),str(songname).lower(),url,str(iconimage),str(dur).replace('qq',''))
        else:
            list = "%s<>%s<>%s<>%s<>%s" % (str(artist),str(album),str(songname).lower(),url,str(iconimage))
        list = list.replace(',', '')
        artistsong = "%s - %s" % (artist,songname)
        contextMenuItems = []
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&songname="+urllib.quote_plus(songname)+"&artist="+urllib.quote_plus(artist)+"&album="+urllib.quote_plus(album)+"&dur="+str(dur)+"&type="+str(type)
        ok=True
        if type != 'favvid':
            suffix = ""
            contextMenuItems.append(("[COLOR lime]Add to Favourite Videos[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=1323&iconimage=%s)'%(sys.argv[0], urllib.quote(artistsong), urllib.quote(url), urllib.quote(iconimage))))
        else:
            suffix = ' [COLOR lime]+[/COLOR]'
            contextMenuItems.append(("[COLOR orange]Remove from Favourite Videos[/COLOR]",'XBMC.RunPlugin(%s?name=%s&url=%s&mode=1324&iconimage=%s)'%(sys.argv[0], urllib.quote(artistsong), urllib.quote(url), urllib.quote(iconimage))))
        liz=xbmcgui.ListItem(name + suffix, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        songname=urllib.unquote_plus(params["songname"])
except:
        pass
try:
        artist=urllib.unquote_plus(params["artist"])
except:
        pass
try:
        album=urllib.unquote_plus(params["album"])
except:
        pass
try:
        list=str(params["list"])
except:
        pass
try:
        dur=str(params["dur"])
except:
        pass
try:
        type=urllib.unquote_plus(params["type"])
except:
        pass


if mode==None or url==None or len(url)<1:
    CATEGORIES()
    #get_cookie()
       
elif mode==4:
     charts()
		
		
elif mode==1:
    audio_result(name, url)
	
elif mode ==5:
    if QUEUE_ALBUMS:
        play_album(name, url, iconimage, 'queue', False,artist)
    else:
        play_album(name, url, iconimage, '', True,artist)
	
elif mode ==6:
    play_album(name, url, iconimage,'', False,artist)
	
elif mode ==7:
    play_album(name, url, iconimage,'browse', False,artist)
	
elif mode ==8:
    ADDON.openSettings()
	
elif mode == 10:
    if QUEUE_SONGS:
        play_song(url,name,songname,artist,album,iconimage,dur,False)
    else:
        play_song(url,name,songname,artist,album,iconimage,dur,True)
	
elif mode == 11:
    if url.lower().startswith('s_'):
        play_album(name, url, iconimage,'', False,artist)
    else:
        play_song(url,name,songname,artist,album,iconimage,dur,False)
	
elif mode == 18:
    if url.lower().startswith('s_'):
        play_album(name, url, iconimage, '', True,artist)
    else:
        play_song(url,name,songname,artist,album,iconimage,dur,True)
	
elif mode == 1010:
    artists(url)
	
elif mode == 1011:
    artists_list(name, url,  artist)
	
elif mode == 1050:
    artists_menu(name, url, iconimage, artist)
	
elif mode == 1060:
    genres(url)
	
elif mode == 1070:
    years(name,url,iconimage)
	
elif mode == 1071:
    weeks(name,url,iconimage)
	
elif mode == 1073:
    artisttop(name,url,iconimage)
	
elif mode == 1074:
    song_list(name, url, iconimage)
	
elif mode == 1080:
    browse_songs(name,url,iconimage)
	
elif mode == 1082:
    browse_songs_genre(name,url,iconimage)
	
elif mode == 1081:
    browse_songs_time(name,url,iconimage)
	
elif mode ==1100:
    if QUEUE_ALBUMS:
        play_album(name, url, iconimage, 'queue', False, artist)
    else:
        play_album(name, url, iconimage, '', True, artist)
	
elif mode == 31:
    all_artists(name, url)
	
elif mode == 41:
    sub_dir(name, url,iconimage)
	
elif mode == 22:
    albums(name,url)

elif mode == 12:
    genres(name,url)
	
elif mode == 13:
    all_genres(name, url)
	
elif mode == 14:
    genre_sub_dir(name, url,iconimage)

elif mode == 16:
    genre_sub_dir2(name, url,iconimage)
	
elif mode == 15:
    album_list(name, url)
	
elif mode == 24:
    search(name, url)
	
elif mode == 25:
    search_albums(name)
	
elif mode == 26:
    search_songs(name,"1")
	
elif mode == 27:
    search_artists(name)
	
elif mode == 61:
    add_favourite(name, url, iconimage,  FAV_ARTIST, "Added to Favourites")
		
elif mode == 62:
    remove_from_favourites(name, url,iconimage, FAV_ARTIST, "Removed from Favourites")
		
elif mode == 63:
    favourite_artists()
	
elif mode == 64:
    add_favourite(name, url,iconimage,  FAV_ALBUM, "Added to Favourites")
		
elif mode == 65:
    remove_from_favourites(name, url,iconimage, FAV_ALBUM, "Removed from Favourites")
	
elif mode == 67:
    add_favourite(name, url,iconimage, FAV_SONG, 'Added to Favourites')
	
elif mode == 69:
    favourite_songs()
	
elif mode == 68:
    remove_from_favourites(name, url,iconimage, FAV_SONG, "Removed from Favourites")
	
elif mode == 66:
    favourite_albums()
	
elif mode == 99:
    instant_mix()
	
elif mode == 89:
    instant_mix_album()
	
elif mode == 100:
    clear_playlist()
	
elif mode == 101:
    charts()
	
elif mode == 102:
    chart_lists(name, url)
	
elif mode == 201:
    download_song(url,name,songname,artist,album,iconimage)
	
elif mode == 202:
    download_album(url,name,iconimage,artist)
	
elif mode == 1201:
    searchmenu(name,url)
	
elif mode == 1202:
    favouritesmenu()
	
elif mode == 1203:
    moods()

elif mode == 1204:
    moodlist(url)
	
elif mode == 1205:
    if QUEUE_ALBUMS:
        play_moods(name, url, iconimage, 'queue', False,artist)
    else:
        play_moods(name, url, iconimage, 'queue', True,artist)
		
elif mode == 1206:
        play_moods(name, url, iconimage, 'queue', False,artist)
		
elif mode == 1300:
    audio()
	
elif mode == 1301:
    video()
	
elif mode == 1302:
    video_list(name,url,artist)

elif mode == 1303:
    most_viewed(name,url)
	
elif mode == 1304:
    video_genres(name,url)
	
elif mode == 1306:
    video_chart_list(name,url,artist)
	
elif mode == 1307:
    video_date(name,url)
	
elif mode == 1308:
    video_date_month(name,url,iconimage)
	
elif mode == 1309:
    video_list_date(name,url,artist)
	
elif mode == 1311:
    video_countries(name,url)
	
elif mode == 1312:
    video_artists(name,url)
	
elif mode == 1313:
    video_artist_list(name,url,iconimage)
	
elif mode == 1314:
    artist_videos(name,url)
	
elif mode == 1315:
    awards(name,url)
	
elif mode == 1320:
    play_video(name,url,iconimage,artist,songname,'',True)
	
elif mode == 1321:
    searchvideomenu(name,url)
	
elif mode == 1322:
    searchvideo(name,url)
	
elif mode == 1323:
    add_favourite(name, url,iconimage, FAV_VIDEO, 'Added to Favourites')
	
elif mode == 1325:
    favourite_videos()
	
elif mode == 1326:
    favourite_videoartists()
	
elif mode == 1324:
    remove_from_favourites(name, url,iconimage, FAV_VIDEO, "Removed from Favourites")
	
elif mode == 1327:
    add_favourite(name, url,iconimage, FAV_VIDEOARTIST, 'Added to Favourites')
	
elif mode == 1328:
    remove_from_favourites(name, url,iconimage, FAV_VIDEOARTIST, "Removed from Favourites")

xbmcplugin.endOfDirectory(int(sys.argv[1]))
