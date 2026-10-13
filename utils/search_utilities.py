#!/usr/bin/env python3
from datetime import datetime
import json
import urllib.parse

from utils import general_utilities


class Google(object):
    def __init__(self, pages=1, hl='en', api_key=None):
        # query = None
        self.pages = pages
        self.hl = hl
        self.rsz = 8
        self.filter = 1
        self.base_url = 'http://ajax.googleapis.com/ajax/services/search/web?'
        self.api_key = None
        self.geocoding = None
        if api_key:
            self.base_url += 'key=%s&' % (api_key)
            self.api_key = api_key
        self.results = None

    def search(self, query):
        results = []
        for page in range(0, self.pages):
            args = {'q': query,
                    'v': '1.0',
                    'start': page * self.rsz,
                    'rsz': self.rsz,
                    'filter': self.filter,
                    'hl': self.hl}

            data, err = general_utilities.get_page(self.base_url, params=args)
            data = json.loads(data)
            if 'responseStatus' not in data:
                continue
            if data.get('responseStatus') != 200:
                continue
            results.append(data)
        self.results = results

    def get_results(self):
        return self.results

    def get_links_result(self):
        """
        parse urls from result
        :return: list of urls
        """
        search_results = self.results
        results = []
        for data in search_results:
            if data and 'responseData' in data and data['responseData']['results']:
                for result in data['responseData']['results']:
                    if result:
                        results.append(urllib.parse.unquote(result['unescapedUrl']))
        return results

    def fetch_geocoding(self, query):
        """
        return all geocoding data on address or cordinate
        :return:
        """
        result = {}
        list_result = []
        if self.api_key:
            base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
            args = {'address': query,
                    'key': self.api_key}
        else:
            base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
            args = {'address': query}

        data, err = general_utilities.get_page(base_url, params=args)
        jsonobj = json.loads(data)

        status = jsonobj["status"]
        json_results = jsonobj["results"]

        if status == "OK":
            for res in json_results:
                cur_result = {}

                cur_result["formatted_address"] = res["formatted_address"]
                cur_result["lat"] = res["geometry"]["location"]["lat"]
                cur_result["lng"] = res["geometry"]["location"]["lng"]
                list_result.append(cur_result)

        result["results"] = list_result

        result["status"] = status
        self.geocoding = result

    def get_geocoding(self):
        """
        return all fetch_geocoding result
        :return:
        """
        return self.geocoding

    def get_coordinates(self):
        """
        return first coordinates from fetched geocoding
        :return:
        """
        first_result = self.geocoding["results"][0]
        return (first_result["lat"], first_result["lng"])

class FlickrApi(object):
    def __init__(self, api_key, per_page=200):
        self.method = 'flickr.photos.search'
        self.format = 'json'
        self.api_key = api_key
        self.min_date = '2000-01-01 00:00:00'
        self.max_date = ''
        self.radius_units = 'km'
        self.per_page = per_page
        self.has_geo = 1
        self.extras = 'date_upload,date_taken,owner_name,geo,url_t,url_m'
        self.error = None

        self.base_url = 'https://api.flickr.com/services/rest/?'

    def get_photos_by_point(self, point, radius_in_meters):
        rad = radius_in_meters / 1000.0
        lat = point.split(',')[0]
        lon = point.split(',')[1]
        params = {'method': self.method,
                  'format': self.format,
                  'api_key': self.api_key,
                  'lat': lat,
                  'lon': lon,
                  'has_geo': self.has_geo,
                  'min_taken_date': self.min_date,
                  'extras': self.extras,
                  'radius': rad,
                  'radius_units': self.radius_units,
                  'per_page': self.per_page}

        data, self.error = general_utilities.get_page(self.base_url, params=params)
        jsonobj = json.loads(data[14:-1])
        photo_results = []

        if jsonobj['stat'] == 'fail':
            self.error(jsonobj['message'])
        else:

            for photo in jsonobj['photos']['photo']:
                latitude = photo['latitude']
                longitude = photo['longitude']
                if not all((latitude, longitude)): continue
                screen_name = photo['owner']
                profile_name = photo['ownername']
                profile_url = 'http://flickr.com/photos/%s' % screen_name
                try:
                    media_url = photo['url_m']
                except KeyError:
                    media_url = photo['url_t'].replace('_t.', '.')
                message = photo['title']
                try:
                    time = str(datetime.strptime(photo['datetaken'], '%Y-%m-%d %H:%M:%S'))
                except ValueError:
                    time = str(datetime(1970, 1, 1))
                photo_results.append(
                    [screen_name, profile_name, profile_url, media_url, message, latitude, longitude,
                     time])

        return photo_results

    def get_photos_by_user(self, user):
        params = {'method': self.method,
                  'format': self.format,
                  'api_key': self.api_key,
                  'user_id': user,
                  'min_taken_date': self.min_date,
                  'extras': self.extras,
                  'radius_units': self.radius_units,
                  'per_page': self.per_page}
        data, self.error = general_utilities.get_page(self.base_url, params=params)

        jsonobj = json.loads(data[14:-1])
        photo_results = []

        if jsonobj['stat'] == 'fail':
            self.error(jsonobj['message'])
        else:

            for photo in jsonobj['photos']['photo']:
                source = 'Flickr'
                screen_name = photo['owner']
                profile_name = photo['ownername']
                profile_url = 'http://flickr.com/photos/%s' % screen_name
                try:
                    media_url = photo['url_m']
                except KeyError:
                    media_url = photo['url_t'].replace('_t.', '.')
                thumb_url = photo['url_t']
                message = photo['title']
                try:
                    time = str(datetime.strptime(photo['datetaken'], '%Y-%m-%d %H:%M:%S'))
                except ValueError:
                    time = str(datetime(1970, 1, 1))
                photo_results.append([screen_name, profile_name, profile_url, media_url, thumb_url, message, time])

        return photo_results
