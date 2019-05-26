# -*- coding: utf8 -*-

from app.models import Post
import app
import math
import datetime


class Feed:
    CACHE_WELCOME_PAGE = 'stamps/welcome'
    CACHE_RANKING_PAGE = 'stamps/ranking'
    CACHE_CATEGORY_PAGE = 'stamps/category'

    CACHE_FEED_LIST = 'stamps/feeds.v1'
    FEED_DEFAULT_LIMIT = 100

    vote_factor = 10
    epoch = datetime.datetime(1970, 1, 1)

    @classmethod
    def epoch_seconds(cls, date):
        td = date - cls.epoch
        return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)

    @classmethod
    def base_score(cls, page_views, ups, downs):
        return page_views + (ups * cls.vote_factor) - (downs * cls.vote_factor)

    @classmethod
    def score(cls, page_views, ups, downs, date):
        s = cls.base_score(page_views, ups, downs)
        order = math.log(max(abs(s), 1), 10)
        sign = 1 if s > 0 else -1 if s < 0 else 0
        seconds = cls.epoch_seconds(date) - 1134028003
        return round((sign * order) + (seconds / 45000), 7)

    @classmethod
    def get_feed_cache(cls, name, page=1, limit=FEED_DEFAULT_LIMIT, lang='en'):
        key = u'%s.%s.%s.%s' % (name, page, limit, lang)
        return app.cache.get(key)

    @classmethod
    def set_feed_cache(cls, name, data, page=1, limit=FEED_DEFAULT_LIMIT, duration=3600, lang='en'):
        key = u'%s.%s.%s.%s' % (name, page, limit, lang)
        app.cache.set(key, data, duration)

        feed_list = app.cache.get(cls.CACHE_FEED_LIST) or []

        if key not in feed_list:
            feed_list.append(key)
            app.cache.set(cls.CACHE_FEED_LIST, feed_list, 3600 * 24)

    @classmethod
    def clear_feed_cache(cls):
        keys = app.cache.get(cls.CACHE_FEED_LIST) or []
        for key in keys:
            app.cache.set(key, None)

    @classmethod
    def posts(cls, page=1, limit=10, status=Post.POST_PUBLIC, orderby='created_at', desc=True):
        q = Post.query.filter_by(status=status)

        count = q.count()
        records = []

        if count:
            sort_by = '%s %s' % (orderby, 'DESC' if desc else 'ASC')

            records = q.order_by(app.sa.text(sort_by)) \
                .limit(limit) \
                .offset((page - 1) * limit)

        return list(records), count

    @classmethod
    def ranking(cls, page=1, limit=20):
        from app.models import Post
        query = Post.query.filter_by(status=Post.POST_PUBLIC)
        count = query.count()
        records = []
        if count:
            order = app.sa.text('score DESC')
            offset = (page - 1) * limit
            records = query.order_by(order).limit(limit).offset(offset)
        return records, count

    @classmethod
    def category(cls, category, page=1, limit=20):
        from app.models import Post
        query = Post.query.filter_by(
            category_id=category.id, status=Post.POST_PUBLIC)
        count = query.count()
        records = []
        if count:
            order = app.sa.text('created_at DESC')
            offset = (page - 1) * limit
            records = query.order_by(order).limit(limit).offset(offset)
        return records, count
