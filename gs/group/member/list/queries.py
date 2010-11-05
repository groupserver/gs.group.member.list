# coding=utf-8
import pytz
from datetime import  datetime
import sqlalchemy as sa

class MembersQuery(object):
    def __init__(self, da):
        self.postTable = da.createTable('post')
        
    def posting_authors(self, siteId, groupId, limit=5):
        # The query to get the five authors who most recently posted
        #   requires a subquery (that is a SELECT within a SELECT). The
        #   query looks a bit like the following.
        # 
        # SELECT user_id AS distinct_user, date AS distinct_date
        # FROM (
        #   SELECT DISTINCT ON (user_id) user_id, date
        #    FROM post
        #      WHERE group_id = 'development'
        #     ORDER BY user_id, date DESC) AS something
        # ORDER BY distinct_date DESC
        # LIMIT 5;
        retval = []
        pt = self.postTable
        # In SQL Alchemy we write the query from inside out. First the
        #   inner query.
        s1 = sa.select([pt.c.user_id, pt.c.date], distinct=pt.c.user_id)
        s1.append_whereclause(pt.c.group_id == groupId)
        s1.append_whereclause(pt.c.site_id == siteId)
        s1.order_by(pt.c.user_id, sa.desc(pt.c.date))
        # We alias the inner query (this is the "AS something" part).
        ss = s1.alias('ss')
        # Now we write the outer query
        s2 = sa.select([ss.c.user_id, ss.c.date])
        s2.order_by(sa.desc(ss.c.date))
        s2.limit = limit
        
        r =  s2.execute()
        for x in r:
            retval.append(x['user_id'])
        
        assert type(retval) == list
        return retval

    def top_posting_authors(self, siteId, groupId, limit=5):
        pt = self.postTable
        cols = [pt.c.user_id, sa.func.count('*').label('post_count')]
        s = sa.select(cols)
        s.append_whereclause(pt.c.group_id == groupId)
        s.append_whereclause(pt.c.site_id == siteId)
        s.group_by(pt.c.user_id)
        s.order_by(sa.desc('post_count'))
        s.limit = limit

        r = s.execute()

        retval = [{'user_id': x['user_id'], 'post_count':x['post_count']}
                    for x in r]
        return retval

