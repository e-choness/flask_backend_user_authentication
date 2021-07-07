# coding:utf-8
"""

"""
from app.api.base import Service
from app.models.model import *


# --------------test table--------------------

class ArticleAPI(Service):
    """
    """
    __model__ = Article
    __methods__ = ["GET", "POST", "PUT", "DELETE"]

    service_name = 'article'
