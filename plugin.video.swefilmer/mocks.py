# -*- coding: utf-8 -*-
# Mocks for testing
import os
from xml.dom.minidom import parse


class Xbmc(object):
    BACK = 1
    LOGERROR = ['ERROR', 1]
    LOGWARNING = ['WARNING', 2]
    LOGNOTICE = ['NOTICE', 3]
    LOGDEBUG = ['NOTICE', 4]

    def __init__(self, level=LOGERROR):
        self.level = level

    class Keyboard(object):
        def __init__(self, placeholder, header, hidden=False):
            self.placeholder = placeholder
            self.header = header
            self.hidden = hidden

        def doModal(self):
            pass

        def isConfirmed(self):
            return True

        def getText(self):
            return 'bad'

    def log(self, msg, level=LOGNOTICE):
        if level[1] <= self.level[1]:
            print msg

    def translatePath(self, path):
        if 'special://' in path:
            return './' + path.split('special://')[1]
        return path

    class Player(object):
        def play(self, *args, **kwargs):
            print 'playing stream %s (%s)'  % (kwargs['listitem'].infoLabels['Title'], kwargs['item'])
            return Xbmc.BACK


class Xbmcplugin(object):

    def __init__(self, xbmc):
        self.xbmc = xbmc
        self.dir_items = []
        self.succeeded = False

    def addDirectoryItem(self, handle, url, listitem, isFolder, totalItems=None):
        self.dir_items.append((handle, url, listitem, isFolder))
        self.xbmc.log('addDirectoryItem %s - %s' % (listitem.caption,
                                                    str(url)), Xbmc.LOGNOTICE)

    def endOfDirectory(self, handle, succeeded=None, updateListing=None,
                       cacheToDisc=None):
        self.succeeded = succeeded

    def setResolvedUrl(self, handle, succeeded, listitem):
        if succeeded:
            msg = "start playing " + listitem.path
        else:
            msg = "could not find film"
        self.xbmc.log(msg)

    def reset(self):
        self.dir_items = []
        self.succeeded = False

class Xbmcgui(object):
    class ListItem(object):

        def __init__(self, *args, **kwargs):
            if len(args) == 1:
                self.caption = args[0]
            self.properties = {}

        def setInfo(self, type, infoLabels):
            self.type = type
            self.infoLabels = infoLabels

        def setThumbnailImage(self, thumb_url):
            pass

        def setProperty(self, key, value):
            self.properties[key] = value

        def setPath(self, path):
            self.path = path

    class Dialog(object):
        def ok(self, title, msg):
            print '[DIALOG] %s - %s' % (title, msg)
            return Xbmc.BACK

        def select(self, title, alternatives):
            print '[DIALOG SELECT] %s' % title
            print "\n".join(alternatives)
            return 0  # Select first one"


class Xbmcaddon(object):
    class Addon:
        def __init__(self, id=None):
            self.pluginId = id
            self.info = {'path': os.getcwd(), 'profile': os.getcwd()}

            self.settings = {}
            settingsFileName = 'resources/settings.xml'
            if os.path.exists(settingsFileName):
                self.readSettings(settingsFileName)
            localSettingsFileName = 'localSettings.xml'
            if os.path.exists(localSettingsFileName):
                self.readSettings(localSettingsFileName)

            self.strings = {}
            for lang in ['Swedish', 'English']:
                stringsFileName = 'resources/language/' + lang + '/strings.xml'
                if not os.path.exists(stringsFileName): continue
                doc = parse(stringsFileName)
                for el in doc.getElementsByTagName('string'):
                    key = int(el.getAttribute('id'))
                    self.strings[key] = el.childNodes[0].data
                break

            self.readTestConfig()

            self.info = {'path': os.getcwd(), 'profile': os.getcwd()}

        def __del__(self):
            self.writeTestConfig()

        def readSettings(self, fileName):
            doc = parse(fileName)
            for el in doc.getElementsByTagName('setting'):
                typ = el.getAttribute('type')
                key = el.getAttribute('id')
                if el.hasAttribute('value'):
                    value = el.getAttribute('value')
                else:
                    value = el.getAttribute('default')
                if typ == 'sep': continue
                if typ == 'slider':
                    if el.getAttribute('option') == 'int':
                        typ = 'enum'
                if typ == 'enum':
                    self.settings[key] = int(value)
                else:
                    self.settings[key] = value

        def readTestConfig(self):
            testConfig = 'test.config'
            if os.path.exists(testConfig): 
                doc = parse(testConfig)
                for el in doc.getElementsByTagName('setting'):
                    typ = el.getAttribute('type')
                    key = el.getAttribute('id')
                    value = el.getAttribute('value')
                    if typ == 'int':
                        value = int(value)
                    self.setSetting(key, value)

        def writeTestConfig(self):
            testConfig = 'test.config'
            if os.path.exists(testConfig):
                doc = parse(testConfig)
                for el in doc.getElementsByTagName('setting'):
                    key = el.getAttribute('id')
                    if key in self.settings:
                        el.setAttribute('value', str(self.settings[key]))
                file = open(testConfig, 'w')
                file.write(os.linesep.join(
                        [s for s in doc.toprettyxml().splitlines() if s.strip()]) +
                           os.linesep)
                file.close()

        def getLocalizedString(self, stringId):
            if stringId in self.strings:
                return self.strings[stringId]
            else:
                return "string not defined: " + str(stringId)

        def getSetting(self, key):
            if key in self.settings:
                return self.settings[key]
            return None

        def setSetting(self, key, value):
            self.settings[key] = value

        def getAddonInfo(self, key):
            if key in self.info:
                return self.info[key]
            return None
