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
from gs.database import getSession, getTable
import sqlalchemy as sa


class MembersQuery(object):
    def __init__(self):
        self.postTable = getTable('post')

    def posting_authors(self, siteId, groupId, limit=5):
        '''Get the most recently posting authors.'''
        # The query to get the five authors who most recently posted looks a
        # bit like the following.
        #   SELECT user_id, MAX(date) AS max_date
        #   FROM post
        #   WHERE group_id = 'development'
        #     AND site_id = 'groupserver'
        #     AND hidden is NULL
        #   GROUP BY user_id
        #   ORDER BY max_date DESC
        #   LIMIT 5;
        pt = self.postTable
        cols = [pt.c.user_id, sa.func.max(pt.c.date).label('max_date')]
        s = sa.select(cols, group_by=pt.c.user_id,
                        order_by=(sa.desc('max_date')), limit=limit)
        s.append_whereclause(pt.c.group_id == groupId)
        s.append_whereclause(pt.c.site_id == siteId)
        s.append_whereclause(pt.c.hidden == None)  # lint:ok

        session = getSession()
        r = session.execute(s)

        retval = []
        for x in r:
            retval.append(x['user_id'])
        assert type(retval) == list
        return retval

    def top_posting_authors(self, siteId, groupId, limit=5):
        pt = self.postTable
        cols = [pt.c.user_id, sa.func.count('*').label('post_count')]
        s = sa.select(cols, limit=limit, group_by=pt.c.user_id,
                      order_by=sa.desc('post_count'))
        s.append_whereclause(pt.c.group_id == groupId)
        s.append_whereclause(pt.c.site_id == siteId)
        s.append_whereclause(pt.c.hidden == None)  # lint:ok

        session = getSession()
        r = session.execute(s)

        retval = [{'user_id': x['user_id'], 'post_count':x['post_count']}
                    for x in r]
        return retval
