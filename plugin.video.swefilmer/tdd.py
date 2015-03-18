# -*- coding: utf-8 -*-
from copy import deepcopy
from mocks import Xbmc, Xbmcplugin, Xbmcgui, Xbmcaddon
import navigation
import swefilmer
import unittest
from navigation import Navigation

class FirstTests(unittest.TestCase):
    def setUp(self):
        self.xbmc = Xbmc(Xbmc.LOGERROR)
        self.xbmcplugin = Xbmcplugin(self.xbmc)
        self.xbmcgui = Xbmcgui()
        self.xbmcaddon = Xbmcaddon()

    def test_swefilmer(self):
        swe = swefilmer.Swefilmer(self.xbmc, self.xbmcplugin, self.xbmcgui,
                                  self.xbmcaddon)
        swe.get_url(swefilmer.BASE_URL)

    def test_navigation(self):
        swe = swefilmer.Swefilmer(self.xbmc, self.xbmcplugin, self.xbmcgui,
                                  self.xbmcaddon)
        nav = navigation.Navigation(self.xbmc, self.xbmcplugin, self.xbmcgui,
                                    self.xbmcaddon, swe, 'plugin', '1', '')
        username, password = nav.get_credentials()
        swe.login(username, password)

    def test_traverse_all(self):
        self.xbmcplugin.reset()
        swe = swefilmer.Swefilmer(self.xbmc, self.xbmcplugin, self.xbmcgui,
                                  self.xbmcaddon)
        nav = Navigation(self.xbmc, self.xbmcplugin, self.xbmcgui,
                         self.xbmcaddon, swe, 'plugin', '1', '')
        self.assertEquals(nav.plugin_url, 'plugin')
        self.assertEquals(nav.handle, 1)
        self.assertEquals(nav.params, {})

        # call with no parameters
        nav.dispatch()
        self.traverse_video = True
        self.traverse(self.xbmcplugin.dir_items, [])

    def traverse(self, dir_items, stack):
        print '***** stack: ' + str(stack)
        i = 0
        for (handle, url, listitem, isFolder) in dir_items:
            i += 1
            params = url.split('?')[1]
            if isFolder or (self.traverse_video and url.find('plugin') == 0):
                self.xbmcplugin.reset()
                swe = swefilmer.Swefilmer(self.xbmc, self.xbmcplugin,
                                          self.xbmcgui, self.xbmcaddon)
                nav = Navigation(self.xbmc, self.xbmcplugin, self.xbmcgui,
                                 self.xbmcaddon, swe, 'plugin', '1',
                                 '?' + params)
                if listitem.caption == nav.localize(30301):
                    continue
                stack.append(i)
                print '***** selecting %d: %s' % (i, listitem.caption)
                nav.dispatch()
                new_list = deepcopy(self.xbmcplugin.dir_items)
                self.traverse(new_list, stack)
            else:
                pass
        if len(stack) > 0:
            stack.pop()
        return

if __name__ == '__main__':
    unittest.main()
