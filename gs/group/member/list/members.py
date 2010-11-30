# coding=utf-8
from zope.component import createObject
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from gs.group.home.simpletab import MemberOnlyTab

class SimpleMemberList(MemberOnlyTab):
    def __init__(self, context, request, view, manager):
        MemberOnlyTab.__init__(self, context, request, view, manager)

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

