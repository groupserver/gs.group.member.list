# coding=utf-8
"""Interfaces for the members page."""
from zope.viewlet.interfaces import IViewletManager
from zope.schema import Text, ASCIILine

class IMemberList(IViewletManager):
    '''A viewlet manager for the list of group members.'''

