# coding=utf-8
from zope.cachedescriptors.property import Lazy
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from gs.group.member.viewlet import MemberViewlet


class SimpleMemberList(MemberViewlet):
    def __init__(self, context, request, view, manager):
        MemberViewlet.__init__(self, context, request, view, manager)

    @Lazy
    def show(self):
        return self.isMember

    def update(self):
        members = GSGroupMembersInfo(self.context)
        l = lambda u: u.name

        # Create a handy function to curry createObject
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
        self.invitedMembers.sort(key=l)
