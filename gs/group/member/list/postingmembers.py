# coding=utf-8
from urllib import urlencode
from zope.component import createObject
from Products.GSSearch.queries import MessageQuery
from queries import MembersQuery

class PostingMemberList(object):
    def __init__(self, context, request, view, manager):
        # TODO: move core code to gs.group.base
        self.context = context
        self.request = request
        self.__parent__ = view
        self.siteInfo = createObject('groupserver.SiteInfo', context)
        self.groupInfo = createObject('groupserver.GroupInfo', context)
        self.recentPostingMembers = []
        self.topPostingMembers = []

    # TODO: Fix
    viewTopics = True

    def update(self):
        if self.viewTopics:
            # If you cannot see the topics you should not see who posted
            self.update_recent_posting_members()
            self.update_top_posting_members()

    def update_recent_posting_members(self):
        mq = MembersQuery(self.context.zsqlalchemy)
        ml = mq.posting_authors(self.siteInfo.id, self.groupInfo.id,
                                limit=6)
        for uid in ml:
            pu = RecentPostingUser(self.context, uid, self.groupInfo, 
                    self.siteInfo)
            self.recentPostingMembers.append(pu)

    def update_top_posting_members(self):
        mq = MembersQuery(self.context.zsqlalchemy)
        tm = mq.top_posting_authors(self.siteInfo.id, 
                                   self.groupInfo.id, limit=6)
        for m in tm:
            pu = TopPostingUser(self.context, m['user_id'], 
                    self.groupInfo, self.siteInfo, m['post_count'])
            self.topPostingMembers.append(pu)

class RecentPostingUser(object):
    def __init__(self, context, uid, groupInfo, siteInfo):
        userInfo =  createObject('groupserver.UserFromId', context, uid)
        self.userInfo = userInfo
        
        mq = MessageQuery(context, context.zsqlalchemy)
        t = createObject('groupserver.SearchTextTokens', '')
        self.latestPost = mq.post_search_keyword(t, siteInfo.id,  
                                                 [groupInfo.id], 
                                                 [userInfo.id], 1)[0]

        self.postUrl = '/r/post/%s' % self.latestPost['post_id']
        
    def __getattr__(self, name):
        return getattr(self.userInfo, name)

class TopPostingUser(object):
    def __init__(self, context, uid, groupInfo, siteInfo, nPosts):
        userInfo =  createObject('groupserver.UserFromId', context, uid)
        self.nPosts = nPosts
        d = {   'g': groupInfo.id,
                'a': userInfo.id,
                'p': '1',
                't': '0'}
        self.searchUrl = '/s?%s' % urlencode(d)
        self.userInfo = userInfo
        
    def __getattr__(self, name):
        return getattr(self.userInfo, name)
