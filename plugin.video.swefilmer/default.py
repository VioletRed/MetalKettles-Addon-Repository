# -*- coding: utf-8 -*-
import swefilmer
import sys
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmc
from navigation import Navigation

swe = swefilmer.Swefilmer(xbmc, xbmcplugin, xbmcgui, xbmcaddon)
navigation = Navigation(xbmc, xbmcplugin, xbmcgui, xbmcaddon, swe, sys.argv[0],
                        sys.argv[1], sys.argv[2])
navigation.dispatch()
