The ``gs.group.member.list`` product provides some simple lists of group
members on the `members page`_ and a `query`_ that can be used by other
products.

Members Page
============

Linked to from the group homepage, the Members page lists the members
of the group. It is a simple list: only the profile photo, name, and
membership status is listed.

The Members Directory (found in ``gs.group.member.directory``) provides
a more complete and complex page, that allows members to be sorted based
on different fields.

Query
=====

The ``gs.group.member.list.MembersQuery`` class provides two methods.

``posting_authors(siteId, groupId, limit=5)``:
  Returns a list of distinct user-identifiers that represents the people
  that most recently posted to the group. Someone listed by this method may
  not be a group member, as people can leave the group.

``top_posting_authors(siteId, groupId, limit=5)``:
   Returns a list of distinct user-identifiers that represents the people
   in the group that post the *most*.
