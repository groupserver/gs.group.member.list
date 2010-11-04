# coding=utf-8
from zope.component import createObject
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo

class SimpleMemberList(object):
    def __init__(self, context, request, view, manager):
        self.context = context
        self.request = request
        self.__parent__ = view
        self.siteInfo = createObject('groupserver.SiteInfo', context)
        self.groupInfo = createObject('groupserver.GroupInfo', context)

    def update(self):
        members = GSGroupMembersInfo(self.context)
        l = lambda u: u.name

        # Create a handy function to curry createObject
        self.managers = members.managers
        
        self.ptnCoach = members.ptnCoach
        
        self.admins = [a for a in self.managers + [self.ptnCoach] if a]
        print self.admins
        self.admins.sort(key=l)

        # TODO: do this in GSGroupMembersInfo
        skip = [m.id for m in self.admins]
        self.normalMembers = [m for m in members.fullMembers
                            if m.id not in skip]
        self.normalMembers.sort(key=l)
        
        self.invitedMembers = members.invitedMembers
        self.invitedMembers.sort(key=l)

