#!/usr/bin/env python
import re

from utils import general_utilities, search_utilities
from core.base.abstract_vector import base_vector
import shlex
from utils.search_utilities import Panoramio


class panoramio_by_box(base_vector):
    result = []
    banner = general_utilities.generate_banner("Panoramio By Location")
    # header = ['owner_id','owner_name', 'owner_url', 'media_url', 'photo_url', 'title', 'latitude', 'longtitude', 'upload_date']
    header = ['media_url', 'photo_url', 'title', 'latitude', 'longtitude', 'upload_date']

    def prepare(self, target, vector_args=None):
        if re.match(r"[\d\.]\,[\d\.]",target):
            point = target
            splitted_point = point.split(',')
            self.lat = splitted_point[0]
            self.lon = splitted_point[1]
        else:
            serch_cord = search_utilities.Google()
            serch_cord.fetch_geocoding(target)
            self.lat, self.lon = serch_cord.get_coordinates()

        self.half_side = 100

        if vector_args:
            s_vector_args = ' '.join(vector_args)
            vector_args = dict(token.split('=') for token in shlex.split(s_vector_args))


            if vector_args.has_key('radius'):
                self.half_side = int(vector_args['radius'])

    def execute(self):
        panoramio = Panoramio()
        result = panoramio.get_photos_by_box(self.lat, self.lon, self.half_side)
        self.result = [item[3:] for item in result ]