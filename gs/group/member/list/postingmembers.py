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
from zope.component import createObject
from Products.GSSearch.queries import MessageQuery
from gs.group.member.viewlet import MemberViewlet
from .queries import MembersQuery


class PostingMemberList(MemberViewlet):
    def __init__(self, context, request, view, manager):
        MemberViewlet.__init__(self, context, request, view, manager)
        self.recentPostingMembers = []
        self.topPostingMembers = []

    def update(self):
        if self.viewTopics:
            # If you cannot see the topics you should not see who posted
            self.update_recent_posting_members()
            self.update_top_posting_members()

    def update_recent_posting_members(self):
        mq = MembersQuery()
        ml = mq.posting_authors(self.siteInfo.id, self.groupInfo.id,
                                limit=6)
        for uid in ml:
            pu = RecentPostingUser(self.context, uid, self.groupInfo,
                    self.siteInfo)
            self.recentPostingMembers.append(pu)

    def update_top_posting_members(self):
        mq = MembersQuery()
        tm = mq.top_posting_authors(self.siteInfo.id,
                                   self.groupInfo.id, limit=6)
        for m in tm:
            pu = TopPostingUser(self.context, m['user_id'],
                    self.groupInfo, self.siteInfo, m['post_count'])
            self.topPostingMembers.append(pu)


class RecentPostingUser(object):
    def __init__(self, context, uid, groupInfo, siteInfo):
        userInfo = createObject('groupserver.UserFromId', context, uid)
        self.userInfo = userInfo

        mq = MessageQuery(context)
        t = createObject('groupserver.SearchTextTokens', '')
        posts = mq.post_search_keyword(t, siteInfo.id, [groupInfo.id],
                                       [userInfo.id], 1)
        assert posts, 'No posts for "%s" in %s (%s)' % \
          (uid, groupInfo.name, groupInfo.id)
        self.latestPost = posts[0]

        self.postUrl = '/r/post/%s' % self.latestPost['post_id']

    def __getattr__(self, name):
        return getattr(self.userInfo, name)


class TopPostingUser(object):
    def __init__(self, context, uid, groupInfo, siteInfo, nPosts):
        userInfo = createObject('groupserver.UserFromId', context, uid)
        self.nPosts = nPosts
        d = {'g': groupInfo.id, 'a': userInfo.id, 'p': '1', 't': '0'}
        self.searchUrl = '/s?%s' % urlencode(d)
        self.userInfo = userInfo

    def __getattr__(self, name):
        return getattr(self.userInfo, name)
