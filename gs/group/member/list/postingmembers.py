# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import
from urllib import urlencode
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from Products.GSSearch.queries import MessageQuery


class ActiveUser(object):

    def __init__(self, group, uid, groupInfo, siteInfo):
        self.group = self.context = group
        self.uid = uid
        self.groupInfo = groupInfo
        self.siteInfo = siteInfo

    @Lazy
    def userInfo(self):
        retval = createObject('groupserver.UserFromId', self.group, self.uid)
        return retval

    def __getattr__(self, name):
        return getattr(self.userInfo, name)


class RecentPostingUser(ActiveUser):
    @Lazy
    def latestPost(self):
        mq = MessageQuery(self.group)
        t = createObject('groupserver.SearchTextTokens', '')
        posts = mq.post_search_keyword(t, self.siteInfo.id, [self.groupInfo.id],
                                       [self.userInfo.id], 1)
        if not posts:
            m = 'No posts for "{0}" in {1} ({2})'
            msg = m.format(self.uid, self.groupInfo.name, self.groupInfo.id)
            raise ValueError(msg)
        retval = posts[0]
        return retval

    @Lazy
    def postUrl(self):
        r = '{groupUrl}/messages/post/{postId}'
        retval = r.format(groupUrl=self.groupInfo.relativeURL,
                            postId=self.latestPost['post_id'])
        return retval


class TopPostingUser(ActiveUser):
    def __init__(self, group, uid, groupInfo, siteInfo, nPosts):
        super(TopPostingUser, self).__init__(group, uid, groupInfo, siteInfo)
        self.nPosts = nPosts

    @Lazy
    def searchUrl(self):
        d = {'g': self.groupInfo.id, 'a': self.userInfo.id, 'p': '1', 't': '0'}
        retval = '/s?{0}'.format(urlencode(d))
        return retval