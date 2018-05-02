#!/usr/bin/env python

from utils import general_utilities, search_utilities
from core.base.abstract_vector import base_vector
import utils.scraper as scraper
import shlex

class flickr_by_radius(base_vector):
    result = []
    banner = general_utilities.generate_banner("Flickr By Location")
    header = ['screen_name', 'profile_name', 'profile_url', 'media_url', 'message', 'latitude', 'longitude', 'date_taken']

    def prepare(self, target, vector_args=None):
        self.radius = 100
        self.point = target
        if vector_args:
            s_vector_args = ' '.join(vector_args)
            vector_args = dict(token.split('=') for token in shlex.split(s_vector_args))

            if vector_args.has_key('radius'):
                self.radius = int(vector_args['radius'])

    def execute(self):
        if self.ricco_conf.has_option('ApiKeys', 'Flickr'):
            api_key = self.ricco_conf.get('ApiKeys', 'Flickr')
        else:
            api_key = None
        flickr = search_utilities.FlickrApi(api_key)
        self.result = flickr.get_photos_by_point(self.point, self.radius)
        # self.result = flickr.get_photos_by_user('27862259@N02')