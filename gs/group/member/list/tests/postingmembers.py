# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals, print_function
from mock import (MagicMock, patch, PropertyMock)
from unittest import TestCase
from gs.group.member.list.postingmembers import (RecentPostingUser, TopPostingUser, )


class TestRecentPostingUser(TestCase):
    @patch('gs.group.member.list.postingmembers.MessageQuery')
    @patch('gs.group.member.list.postingmembers.createObject')
    def test_latest(self, m_cO, m_MQ):
        m_MQ().post_search_keyword.return_value = ['a', 'list', 'of', 'posts', ]

        u = RecentPostingUser(MagicMock(), 'person', MagicMock(), MagicMock())
        r = u.latestPost

        self.assertEqual('a', r)  # The first post

    @patch('gs.group.member.list.postingmembers.MessageQuery')
    @patch('gs.group.member.list.postingmembers.createObject')
    def test_latest_none(self, m_cO, m_MQ):
        m_MQ().post_search_keyword.return_value = []

        u = RecentPostingUser(MagicMock(), 'person', MagicMock(), MagicMock())
        with self.assertRaises(ValueError):
            u.latestPost

    @patch.object(RecentPostingUser, 'latestPost', new_callable=PropertyMock)
    def test_postUrl(self, m_lP):
        m_lP.return_value = {'post_id': 'postIdentifier'}

        groupInfo = MagicMock()
        groupInfo.relativeURL = '/groups/example'
        u = RecentPostingUser(MagicMock(), 'person', groupInfo, MagicMock())
        r = u.postUrl

        self.assertIn('postIdentifier', r)


class TestTopPostingUser(TestCase):
    @patch('gs.group.member.list.postingmembers.createObject')
    def test_serchUrl(self, m_cO):
        groupInfo = MagicMock()
        groupInfo.id = 'example'
        m_cO().id = 'person'
        u = TopPostingUser(MagicMock(), 'person', groupInfo, MagicMock(), 5)
        r = u.searchUrl

        self.assertIn('example', r)
        self.assertIn('person', r)
