# -*- coding: utf-8 -*-
import cookielib
import HTMLParser
import os
import re
import time
import urllib
import urllib2
import urlparse

SAVE_FILE = False
BASE_URL = 'http://www.swefilmer.com/'
USERAGENT = ' Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

class Swefilmer:

    class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
        def http_error_302(self, req, fp, code, msg, headers):
            if msg == "Found":
                return fp
            else:
                return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp,
                                                                  code, msg,
                                                                  headers)

        http_error_301 = http_error_303 = http_error_307 = http_error_302


    def __init__(self, xbmc, xbmcplugin, xbmcgui, xbmcaddon):
        self.xbmc = xbmc
        self.xbmcplugin = xbmcplugin
        self.xbmcgui = xbmcgui
        self.xbmcaddon = xbmcaddon
        self.html_parser = HTMLParser.HTMLParser()
        temp = self.xbmc.translatePath(
            os.path.join(self.xbmcaddon.Addon().getAddonInfo('profile').\
                             decode('utf-8'), 'temp'))
        if not os.path.exists(temp):
            os.makedirs(temp)
        cookiejarfile = os.path.join(temp, 'swefilmer_cookies.dat')
        self.cookiejar = cookielib.LWPCookieJar(cookiejarfile)
        if os.path.exists(cookiejarfile):
            self.cookiejar.load()

        cookieprocessor = urllib2.HTTPCookieProcessor(self.cookiejar)
        opener = urllib2.build_opener(Swefilmer.MyHTTPRedirectHandler,
                                      cookieprocessor)
        urllib2.install_opener(opener)

    def get_url(self, url, filename=None, referer=None, data=None):
        """Send http request to url.
        Send the request and return the html response.
        Sends cookies, receives cookies and saves them.
        Resonse html can be saved in file for debugging.
        """
        self.xbmc.log('get_url' + ((' (' + filename + ')')
                                   if filename else '') + ': ' +
                      str(url), level=self.xbmc.LOGDEBUG)
        req = urllib2.Request(url)
        req.add_header('User-Agent', USERAGENT)
        if referer:
            req.add_header('Referer', referer)
        try:
            response = urllib2.urlopen(req, data)
            url = response.geturl()
            html = response.read()
            response.close()
            self.cookiejar.save()
        except urllib2.HTTPError as e:
            self.xbmc.log('get_url: failed: ' + str(e), level=self.xbmc.LOGERROR)
            return None

        if filename and SAVE_FILE:
            filename = self.xbmc.translatePath('special://temp/' + filename)
            file = open(filename, 'w')
            file.write(html)
            file.close()
        return html

    def login(self, username, password):
        """Login to the site.
        First check if cookies from earlier login exist and are not about
        to expire.
        Login has the side effect of getting cookies which are then used in
        subsequent requests to the site.
        """
        # TODO: what if user changes settings for credentials and cookies
        # are intact?
        for cookie in self.cookiejar:
            if cookie.name.find('phpsugar_') > -1:
                if (cookie.expires - time.time())/3600/24 > 0:
                    return True
                break
        self.cookiejar.clear()
        url = BASE_URL + 'login.php'
        form = {'username' : username,
                'pass' : password,
                'remember' : '1',
                'ref' : '',
                'Login' : 'Logga in' }
        data = urllib.urlencode(form)
        data = data.encode('utf-8') # data should be bytes
        html = self.get_url(url, 'login.html', data=data)
        if html.find('<div class="error_msg') > -1:
            return False
        return True

    def convert(self, val):
        if isinstance(val, unicode):
            val = val.encode('utf8')
        elif isinstance(val, str):
            try:
                val.decode('utf8')
            except:
                pass
        return val

    def parameters_string_to_dict(self, str):
        """Parses parameter string and returns dictionary of keys and values.
        """
        params = {}
        if str:
            pairs = str[1:].split("&")
            for pair in pairs:
                split = pair.split('=')
                if (len(split)) == 2:
                    key = self.convert(urllib.unquote_plus(split[0]))
                    value = self.convert(urllib.unquote_plus(split[1]))
                    params[key] = value
        return params

    def unpack(self, p, a, c, k):
        while c > 0:
            c -= 1
            if k[c]:
                p = re.sub('\\b' + self.baseN(c, a) + '\\b', k[c], p)
        return p

    def baseN(self, num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
        return ((num == 0) and numerals[0]) or \
            (self.baseN(num // b, b, numerals).lstrip(numerals[0]) + \
                 numerals[num % b])

    def yazyaz(self, e):
        _keyStr="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        t = ""
        f = 0
        e = re.sub(r"[^A-Za-z0-9\+\/\=]", "", e)
        while f < len(e):
            s = _keyStr.find(e[f])
            f += 1
            o = _keyStr.find(e[f]) if f < len(e) else 0
            f += 1
            u = _keyStr.find(e[f]) if f < len(e) else 0
            f += 1
            a = _keyStr.find(e[f]) if f < len(e) else 0
            f += 1
            n = s<<2|o>>4
            r = (o&15)<<4|u>>2
            i = (u&3)<<6|a
            t = t + chr(n)
            if u != 64: t = t + chr(r)
            if a != 64: t = t + chr(i)
        return t


    def addCookies2Url(self, url):
        c = ''
        for cookie in self.cookiejar:
            if cookie.domain_specified and cookie.domain in url:
                c += cookie.name + '=' + cookie.value + ';'
        if len(c) > 0:
            url += '|Cookie=' + urllib.quote(c)
        return url

    def parse(self, html, part_pattern, url_and_name_pattern,
              img_pattern):
        # check for more pages
        pagination = [
            BASE_URL + x for x in
            re.findall('<div class="fastphp".*<a href="(.+?)">n&auml;sta',
                       html)
            if not 'class="disabled' in x]
        html = re.findall(part_pattern, html, re.DOTALL)
        if not html:
            return []
        htmlParser = HTMLParser.HTMLParser()
        url_and_name = [(x[0], htmlParser.unescape(x[1])) for x in
                        re.findall(url_and_name_pattern, html[0])]
        img = [None]*len(url_and_name)
        if img_pattern:
            img = re.findall(img_pattern, html[0])
            if len(img) != len(url_and_name):
                raise Exception('found ' + str(len(img)) +
                                ' images but ' + str(len(url_and_name)) +
                                ' names!')
        ret = zip(url_and_name, img)
        return ret, pagination

    def scrape_list(self, html):
        return self.parse(
            html,
            part_pattern='<div class="filmcontent">(.+?)<div id="sidebar">',
            url_and_name_pattern=\
                '<div class="movief"><a href="(.+?)">(.+?)</a></div>',
            img_pattern='<img src="(.+?)"[ ]+alt=.+?/></a>\n')

    def scrape_categories(self, html):
        return self.parse(
            html,
            part_pattern="<ul id=['\"]ul_categories['\"]>(.+?)<ul class=['\"]hidden_li['\"]>",
            url_and_name_pattern='<li.+?<a href="(.+?)">(.+?)</a>',
            img_pattern=None)

    def scrape_series(self, html):
        return self.parse(
            html,
            part_pattern="<ul class=['\"]hidden_li['\"]>(.+?)</ul>",
            url_and_name_pattern='<a href="(.+?)">(.+?)</a>',
            img_pattern=None)

    def scrape_video(self, html):
        if html.find('id="restricted_video"') > -1:
            # registered users only, not logged in?
            return None
        name = re.findall('class="filmcontent".+?title="(.+?)"', html,
                          re.DOTALL)
        if not name:
            name = 'unknown'
        else:
            name = name[0]
        description = re.findall(
            '>Beskrivning<.*?<p>(.+?)</p>', html, re.DOTALL)
        self.xbmc.log('scrape_video: description=' + str(description),
                      level=self.xbmc.LOGDEBUG)
        img = re.findall(
            '<div class="filmaltiimg">.*?<img src="(.+?)".*?</div>', html,
            re.DOTALL)
        self.xbmc.log('scrape_video: img=' + str(img),
                      level=self.xbmc.LOGDEBUG)
        players = re.findall('<div id="(.+?)".+?swe.zzz\(\'(.+?)\'', html)
        return name, description, img, self.scrape_video_urls(players)

    def scrape_video_urls(self, players):
        items = []
        for player in players:
            self.xbmc.log('scrape_video_urls: player=' + str(player),
                          level=self.xbmc.LOGDEBUG)
            streams = None
            if player[0].find("trailer") > -1: continue
            html = self.yazyaz(player[1])
            self.xbmc.log('scrape_video_urls: html=' + str(html),
                          level=self.xbmc.LOGDEBUG)
            url = self.html_parser.unescape(re.findall('<iframe .*?src="(.+?)" ', html)[0])
            self.xbmc.log('scrape_video_urls: url=' + str(url),
                          level=self.xbmc.LOGDEBUG)
            document = self.get_url(url, 'document.html')
            if document == None: continue
            if 'docs.google.com' in url:
                streams = self.scrape_googledocs(document)
            elif len(re.findall('jwplayer\(.+?\)\.setup', document)) > 0:
                if len(re.findall('sources: \[(.+?)\]', document)) > 0:
                    streams = self.scrape_video_jwplayer(document)
                else:
                    streams = self.scrape_video_jwplayer2(document)
            else:
                flashvars = re.findall('var flashVars = {(.+?)}', document)
                if len(flashvars) > 0:
                    streams = self.scrape_video_mailru(flashvars[0])
                elif document.find("document.write(unescape(") > -1:
                    streams = self.scrape_video_mega(document)
                else:
                    streams = self.scrape_video_registered(document)
            if streams and len(streams) > 0:
                name = urlparse.urlparse(streams[0][1]).netloc
                items.append((name, streams))
            self.xbmc.log('scrape_video_urls: streams=' + str(streams),
                          level=self.xbmc.LOGDEBUG)
        return items

    def scrape_googledocs(self, html):
        fmt_list = re.findall('"fmt_list":"(.+?)"', html)
        if len(fmt_list) == 0: return None
        formats = fmt_list[0].split(',')
        streams = re.findall('"url_encoded_fmt_stream_map":"(.+?)"',
                             html)[0].split(',')
        urls = [self.addCookies2Url(urllib2.unquote(x).split('\\u0026')[1]
                                    .split('\\u003d')[1]) for x in streams]
        return zip(formats, urls)

    def scrape_video_mailru(self, flashvars):
        url = re.findall('"metadataUrl":"(.+?)"', flashvars)[0]
        self.xbmc.log('scrape_video_mailru: url=' + str(url),
                      level=self.xbmc.LOGDEBUG)
        mailru = self.get_url(url, 'mailru.html')
        self.xbmc.log('scrape_video_mailru: mailru=' + str(mailru),
                      level=self.xbmc.LOGDEBUG)
        videos = re.findall(',"videos":\[{(.+?)}\],', mailru)
        names = re.findall('"key":"(.+?)"', videos[0])
        urls = [self.addCookies2Url(x) for x in re.findall('"url":"(.+?)"', videos[0])]
        return zip(names, urls)

    def scrape_video_jwplayer(self, document):
        sources = re.findall('sources: \[(.+?)\]', document)
        
        names = re.findall('"label":"(.+?)"', sources[0])
        files = re.findall('"file":"(.+?)"', sources[0])
        urls = [x.decode("unicode-escape") for x in
                re.findall('"file":"(.+?)"', sources[0])]
        return zip(names, urls)

    def scrape_video_jwplayer2(self, document):
        oid = re.findall("param\[5\]\s?\+\s?'(.+?)'", document)
        videoId = re.findall("param\[6\]\s?\+\s?'(.+?)'", document)
        hash = re.findall("param\[7\]\s?\+\s?'(.+?)'", document)
        urlQ = 'https://api.vk.com/method/video.getEmbed?oid=' + oid[0] +'&video_id='+videoId[0]+'&embed_hash='+hash[0]+'&callback=callbackFunc'
        documentQ = self.get_url(urlQ, 'embed.html');
        urls = [(x[0], x[1].replace("\/", "/")) for x in re.findall('"url([0-9]+?)":"(.+?)"', documentQ)]
        return urls

    def scrape_video_mega(self, html):
        html = [urllib.unquote(x) for x in re.findall('document.write\(unescape\("(.+?)"', html)]
        #self.xbmc.log("scrape_video_mega: html=" + str(html), level=self.xbmc.LOGDEBUG)
        try:
            url = [re.findall(',[ ]*file:[ ]*"(.+?)"', x)[0] for x in html]
        except:
            self.xbmc.log("scrape_video_mega: parsing failed", level=self.xbmc.LOGWARNING)
            return None
        #self.xbmc.log("scrape_video_mega: url=" + str(url), level=self.xbmc.LOGDEBUG)
        url = self.addCookies2Url(url[2])
        return [('', url)]

    def scrape_video_registered(self, html):
        url = None
        script = re.findall(
            '(<script type=\'text/javascript\'>eval\(function\(.*}\(.*)', html)
        if len(script) > 0:
            pack = re.findall(
                '}\(\'(.+?[^\\\])\',([0-9]+),([0-9]+),\'(.+?)\'\.split',
                script[0])[0]
            unpacked = self.unpack(pack[0], int(pack[1]), int(pack[2]),
                                   pack[3].split('|'))
            url = re.findall('file:"(.+?)"', unpacked)[0]
        else:
            videosrc = re.findall('videoSrc = "(.+?)"', html)
            if videosrc:
                url = videosrc[0]
        if not url: return None
        url = self.addCookies2Url(url)
        return [('', url)]

    def new_menu_html(self):
        url = BASE_URL + 'newvideos.html'
        return self.get_url(url, 'new.html')

    def top_menu_html(self):
        url = BASE_URL + 'topvideos.html'
        return self.get_url(url, 'top.html')

    def favorites_menu_html(self):
        url = BASE_URL + 'favorites.php?a=show'
        return self.get_url(url, 'favorites.html')

    def categories_menu_html(self):
        return self.get_url(BASE_URL, 'categories.html')

    def search_menu_html(self, search_string):
        url = BASE_URL + 'search.php?' + \
            urllib.urlencode({'keywords': search_string})
        return self.get_url(url, 'search.html')

    def menu_html(self, url):
        return self.get_url(url, 'menu.html')

    def video_html(self, url):
        if 'ajax_request' in url:
            url = eval(url.replace('false', 'False').replace('true', 'True'))
        return self.get_url(url, 'video.html')
