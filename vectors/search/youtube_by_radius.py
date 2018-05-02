#!/usr/bin/env python

from utils import general_utilities, search_utilities
from core.base.abstract_vector import base_vector
import shlex

### DEPRECATED
class youtube_by_radius(base_vector):
    result = []
    banner = general_utilities.generate_banner("Youtube By Location")
    header = ['source', 'screen_name', 'profile_name', 'profile_url', 'media_url', 'thumb_url', 'message', 'latitude',
                         'longitude', 'time']

    def prepare(self, target, vector_args):
        self.radius = 1
        if vector_args:
            s_vector_args = ' '.join(vector_args)
            vector_args = dict(token.split('=') for token in shlex.split(s_vector_args))
            if vector_args.has_key('point'):
                self.point = vector_args['point']
            else:
                exit(1)

            if vector_args.has_key('radius'):
                self.radius = int(vector_args['radius'])

        self.target = target

    def execute(self):
        youtube = search_utilities.Youtube()
        self.result = youtube.get_videos_by_point(self.point, self.radius)
        # self.result = flickr.get_photos_by_user('27862259@N02')__author__ = 'ramen'
