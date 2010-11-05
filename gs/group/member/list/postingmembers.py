# coding=utf-8
from urllib import urlencode
from zope.component import createObject
from queries import MembersQuery

class PostingMemberList(object):
    def __init__(self, context, request, view, manager):
        # TODO: move core code to gs.group.base
        self.context = context
        self.request = request
        self.__parent__ = view
        self.siteInfo = createObject('groupserver.SiteInfo', context)
        self.groupInfo = createObject('groupserver.GroupInfo', context)

    # TODO: Fix
    viewTopics = True

    def update(self):
        self.recentPostingMembers = []
        self.topPostingMembers = []
        if self.viewTopics:
            # If you cannot see the topics you should not see who posted
            mq = MembersQuery(self.context.zsqlalchemy)
            
            ml = mq.posting_authors(self.siteInfo.id, self.groupInfo.id,
                                    limit=6)
            self.recentPostingMembers = [self.kulfi(uid) for uid in ml]
            
            tm = mq.top_posting_authors(self.siteInfo.id, 
                                       self.groupInfo.id, limit=6)
            for m in tm:
                userInfo =  createObject('groupserver.UserFromId', 
                                self.context, m['user_id'])
                pu = PostingUser(self.context, userInfo, self.groupInfo,
                        self.siteInfo, m['post_count'])
                self.topPostingMembers.append(pu)
            
    def kulfi(self, uid):
        return createObject('groupserver.UserFromId', self.context, uid)

class PostingUser(object):
    def __init__(self, context, userInfo, groupInfo, siteInfo, nPosts):
        self.nPosts = nPosts
        d = {   'g': groupInfo.id,
                'a': userInfo.id,
                'p': '1',
                't': '0'}
        self.searchUrl = '/s?%s' % urlencode(d)
        self.userInfo = userInfo
        
    def __getattr__(self, name):
        return getattr(self.userInfo, name)

