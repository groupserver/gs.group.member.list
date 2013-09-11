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
from zope.cachedescriptors.property import Lazy
from gs.group.member.viewlet import MemberViewlet
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from .postingmembers import RecentPostingUser, TopPostingUser
from .queries import MembersQuery


class PostingMemberList(MemberViewlet):
    def __init__(self, group, request, view, manager):
        super(PostingMemberList, self).__init__(group, request, view, manager)

    @Lazy
    def membersQuery(self):
        retval = MembersQuery()
        return retval


class SimpleMemberList(PostingMemberList):
    def __init__(self, group, request, view, manager):
        super(SimpleMemberList, self).__init__(group, request, view, manager)

    @Lazy
    def show(self):
        return self.isMember

    def update(self):
        members = GSGroupMembersInfo(self.context)
        l = lambda u: u.name
        self.managers = members.managers
        self.ptnCoach = members.ptnCoach
        self.admins = [a for a in self.managers + [self.ptnCoach] if a]
        self.admins.sort(key=l)
        # TODO: do this in GSGroupMembersInfo
        skip = [m.id for m in self.admins]
        self.normalMembers = [m for m in members.fullMembers
                                if m.id not in skip]
        self.normalMembers.sort(key=l)
        self.invitedMembers = members.invitedMembers


class ActiveMemberList(PostingMemberList):

    def __init__(self, group, request, view, manager):
        super(ActiveMemberList, self).__init__(group, request, view, manager)

    @Lazy
    def recentPostingMembers(self):
        retval = []
        ml = self.membersQuery.posting_authors(self.siteInfo.id,
                                                self.groupInfo.id, limit=6)
        for uid in ml:
            pu = RecentPostingUser(self.context, uid, self.groupInfo,
                                    self.siteInfo)
            retval.append(pu)
        return retval

    @Lazy
    def show(self):
        retval = self.viewTopics and self.recentPostingMembers
        return retval


class MostActiveMemberList(PostingMemberList):

    def __init__(self, group, request, view, manager):
        super(MostActiveMemberList,
              self).__init__(group, request, view, manager)

    @Lazy
    def topPostingMembers(self):
        retval = []
        tm = self.membersQuery.top_posting_authors(self.siteInfo.id,
                                                   self.groupInfo.id, limit=6)
        for m in tm:
            pu = TopPostingUser(self.context, m['user_id'], self.groupInfo,
                                self.siteInfo, m['post_count'])
            retval.append(pu)
        return retval

    @Lazy
    def show(self):
        retval = self.viewTopics and self.topPostingMembers
        return retval
