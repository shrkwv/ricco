#!/usr/bin/env python

from utils import general_utilities, search_utilities
from core.base.abstract_vector import base_vector
import utils.scraper as scraper
import shlex

class flickr_by_radius(base_vector):
    result = []
    banner = general_utilities.generate_banner("Instagram By Location")
    header = ['screen_name', 'profile_name', 'profile_url', 'media_url', 'message', 'time', 'latitude', 'longitude']

    def prepare(self, target, vector_args=None):
        self.radius = 100
        splitted_point = target.split(',')
        self.lat = splitted_point[0]
        self.lon = splitted_point[1]

        if vector_args:
            s_vector_args = ' '.join(vector_args)
            vector_args = dict(token.split('=') for token in shlex.split(s_vector_args))

            if vector_args.has_key('radius'):
                self.radius = int(vector_args['radius'])

    def execute(self):
        if self.ricco_conf.has_option('ApiKeys','InstagramClientID') and self.ricco_conf.has_option('ApiKeys','InstagramClientSecret'):
            client_id = self.ricco_conf.get('ApiKeys','InstagramClientID')
            client_secret = self.ricco_conf.get('ApiKeys','InstagramClientSecret')
            instagram = search_utilities.InstagramApi(client_id,client_secret)
            self.result = instagram.get_photos_by_circle(self.lan,self.lon, self.radius)
        else:
            self.result = ['Need client id and client secret to run.']
