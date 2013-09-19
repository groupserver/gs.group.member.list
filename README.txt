========================
``gs.group.member.list``
========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
List the members of a GroupServer group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2013-09-19
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.

Introduction
============

The ``gs.group.member.list`` product provides some simple lists of group
members on the `members page`_ and a query_ that can be used by other
products.

Members Page
============

The Members page (``members.html`` in the Group context) lists the members
of the group. It is a simple list: only the profile photo, name, and
membership status is listed.

The Members Directory [#directory]_ provides a more complete and complex
page, that allows members to be sorted based on different fields.

Viewlet managers
----------------

The viewlet manager ``groupserver.MembersList`` organises the viewlets_
into tabs. The manager provides the
``gs.group.member.list.interfaces.IMemberList`` interface. In addition
there is a viewlet manager for organising the JavaScript (if needed), which
provides the ``gs.group.member.list.interfaces.IMemberListJavaScript``
interface.

Viewlets
--------

There are three viewlets

Recently active: 
  The list of members who have posted recently.

Most active:
  The list of members that have posted the most frequently.

All members:
  Actually three lists: 
  
  * The administrators
  * The normal members, and
  * The invited members (which is only shown in private and secret groups).

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

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.group.member.list
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/

.. [#directory] See ``gs.group.member.directory``
                <https://source.iopen.net/groupserver/gs.group.member.directory>

..  LocalWords:  Viewlets MembersList viewlets
