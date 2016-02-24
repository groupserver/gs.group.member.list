# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2016 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals, print_function
from operator import attrgetter
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.group.member.base import (AdminMembers, NormalMembers, InvitedMembers, )
from gs.group.member.viewlet import MemberViewlet
from gs.group.privacy.interfaces import IGSGroupVisibility
from .postingmembers import (RecentPostingUser, TopPostingUser, )
from .queries import MembersQuery
from . import GSMessageFactory as _


class PostingMemberList(MemberViewlet):

    def __init__(self, group, request, view, manager):
        super(PostingMemberList, self).__init__(group, request, view, manager)

    @Lazy
    def membersQuery(self):
        retval = MembersQuery()
        return retval


class AllMemberList(PostingMemberList):
    def __init__(self, group, request, view, manager):
        super(AllMemberList, self).__init__(group, request, view, manager)
        self.title = _('members-tab-title', 'All')

    @Lazy
    def visibility(self):
        retval = IGSGroupVisibility(self.groupInfo)
        return retval

    @Lazy
    def show(self):
        retval = self.isMember or (not self.visibility.isSecret)
        return retval

    def update(self):
        n = NormalMembers(self.context)
        self.normalMembers = sorted(n, key=attrgetter('name'))
        ptnCoach = createObject('groupserver.UserFromId', self.context, n.ptnCoachId)
        self.managers = AdminMembers(self.context)
        admins = [a for a in self.managers]
        admins.append(ptnCoach)
        self.admins = sorted(admins, key=attrgetter('name'))
        self.invitedMembers = sorted(InvitedMembers(self.context), key=attrgetter('name'))


class ActiveMemberList(PostingMemberList):

    def __init__(self, group, request, view, manager):
        super(ActiveMemberList, self).__init__(group, request, view, manager)
        self.title = _('recent-tab-title', 'Recently active')

    @Lazy
    def recentPostingMembers(self):
        retval = []
        ml = self.membersQuery.posting_authors(self.siteInfo.id, self.groupInfo.id, limit=6)
        for uid in ml:
            pu = RecentPostingUser(self.context, uid, self.groupInfo, self.siteInfo)
            retval.append(pu)
        return retval

    @Lazy
    def show(self):
        retval = self.viewTopics and self.recentPostingMembers
        return retval


class MostActiveMemberList(PostingMemberList):

    def __init__(self, group, request, view, manager):
        super(MostActiveMemberList, self).__init__(group, request, view, manager)
        self.title = _('most-tab-title', 'Most active')

    @Lazy
    def topPostingMembers(self):
        retval = []
        tm = self.membersQuery.top_posting_authors(self.siteInfo.id, self.groupInfo.id, limit=6)
        for m in tm:
            pu = TopPostingUser(self.context, m['user_id'], self.groupInfo, self.siteInfo,
                                m['post_count'])
            retval.append(pu)
        return retval

    @Lazy
    def show(self):
        retval = self.viewTopics and self.topPostingMembers
        return retval
