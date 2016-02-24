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
from gs.group.member.list.lists import (MostActiveMemberList, ActiveMemberList, AllMemberList, )


class TestMostActiveMemberList(TestCase):
    '''Test the ``MostActiveMemberList`` class'''

    @patch.object(MostActiveMemberList, 'viewTopics', new_callable=PropertyMock)
    @patch.object(MostActiveMemberList, 'topPostingMembers', new_callable=PropertyMock)
    def test_show(self, m_tPM, m_vT):
        'Test that show the list if there are posts and we can see them'
        m_tPM.return_value = ['a list', 'of things', ]
        m_vT.return_value = True
        group = MagicMock()
        request = MagicMock()
        view = MagicMock()
        manager = MagicMock()
        l = MostActiveMemberList(group, request, view, manager)
        r = l.show

        self.assertTrue(r)

    @patch.object(MostActiveMemberList, 'viewTopics', new_callable=PropertyMock)
    @patch.object(MostActiveMemberList, 'topPostingMembers', new_callable=PropertyMock)
    def test_show_no_posts(self, m_tPM, m_vT):
        'Test that we are hidden if there are no posts'
        m_tPM.return_value = []
        m_vT.return_value = True
        group = MagicMock()
        request = MagicMock()
        view = MagicMock()
        manager = MagicMock()
        l = MostActiveMemberList(group, request, view, manager)
        r = l.show

        self.assertFalse(r)

    @patch.object(MostActiveMemberList, 'viewTopics', new_callable=PropertyMock)
    @patch.object(MostActiveMemberList, 'topPostingMembers', new_callable=PropertyMock)
    def test_show_perms(self, m_tPM, m_vT):
        'Test that we are hidden if we lack the perms to see the archive'
        m_tPM.return_value = ['a', 'list', ]
        m_vT.return_value = False
        group = MagicMock()
        request = MagicMock()
        view = MagicMock()
        manager = MagicMock()
        l = MostActiveMemberList(group, request, view, manager)
        r = l.show

        self.assertFalse(r)


class TestActiveMemberList(TestCase):

    @patch.object(ActiveMemberList, 'viewTopics', new_callable=PropertyMock)
    @patch.object(ActiveMemberList, 'recentPostingMembers', new_callable=PropertyMock)
    def test_show(self, m_rPM, m_vT):
        'Test we show the active members if there recent posts and we have the perms'
        m_rPM.return_value = ['a list', 'of things', ]
        m_vT.return_value = True
        group = MagicMock()
        request = MagicMock()
        view = MagicMock()
        manager = MagicMock()
        l = ActiveMemberList(group, request, view, manager)
        r = l.show

        self.assertTrue(r)

    @patch.object(ActiveMemberList, 'viewTopics', new_callable=PropertyMock)
    @patch.object(ActiveMemberList, 'recentPostingMembers', new_callable=PropertyMock)
    def test_show_perms(self, m_rPM, m_vT):
        'Test we hide the active members if we lack the perms'
        m_rPM.return_value = ['a list', 'of things', ]
        m_vT.return_value = False
        group = MagicMock()
        request = MagicMock()
        view = MagicMock()
        manager = MagicMock()
        l = ActiveMemberList(group, request, view, manager)
        r = l.show

        self.assertFalse(r)

    @patch.object(ActiveMemberList, 'viewTopics', new_callable=PropertyMock)
    @patch.object(ActiveMemberList, 'recentPostingMembers', new_callable=PropertyMock)
    def test_show_no_posts(self, m_rPM, m_vT):
        'Test we hide the active members if we lack posts'
        m_rPM.return_value = []
        m_vT.return_value = True
        group = MagicMock()
        request = MagicMock()
        view = MagicMock()
        manager = MagicMock()
        l = ActiveMemberList(group, request, view, manager)
        r = l.show

        self.assertFalse(r)


class TestAllMemberList(TestCase):

    @patch.object(AllMemberList, 'isMember', new_callable=PropertyMock)
    def test_show_member(self, m_iM):
        'Test we show the members if viewer is a member'
        m_iM.return_value = True
        group = MagicMock()
        request = MagicMock()
        view = MagicMock()
        manager = MagicMock()
        l = AllMemberList(group, request, view, manager)
        r = l.show

        self.assertTrue(r)

    @patch.object(AllMemberList, 'isMember', new_callable=PropertyMock)
    @patch.object(AllMemberList, 'visibility', new_callable=PropertyMock)
    def test_show_perms(self, m_v, m_iM):
        m_iM.return_value = False
        m_v().isSecret = False
        group = MagicMock()
        request = MagicMock()
        view = MagicMock()
        manager = MagicMock()
        l = AllMemberList(group, request, view, manager)
        r = l.show

        self.assertTrue(r)

    @patch.object(AllMemberList, 'isMember', new_callable=PropertyMock)
    @patch.object(AllMemberList, 'visibility', new_callable=PropertyMock)
    def test_show_secret(self, m_v, m_iM):
        'Ensure the members are hidden with secret groups'
        m_iM.return_value = False
        m_v().isSecret = True
        group = MagicMock()
        request = MagicMock()
        view = MagicMock()
        manager = MagicMock()
        l = AllMemberList(group, request, view, manager)
        r = l.show

        self.assertFalse(r)
