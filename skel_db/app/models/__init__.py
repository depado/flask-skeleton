# -*- coding: utf-8 -*-

try:
    from .user import User, Permission
except ImportError:
    from user import User, Permission
