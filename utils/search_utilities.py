#!/usr/bin/env python
from datetime import datetime
import json
import re
import socket
import urllib
import urllib2
import webbrowser
import time

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
        for page in xrange(0, self.pages):
            args = {'q': query,
                    'v': '1.0',
                    'start': page * self.rsz,
                    'rsz': self.rsz,
                    'filter': self.filter,
                    'hl': self.hl}

            # params = urllib.urlencode(args)
            # search_results = urllib2.urlopen(self.base_url + params)
            # data = json.loads(search_results.read())
            data, err = general_utilities.get_page(self.base_url, params=args)
            data = json.loads(data)
            if not data.has_key('responseStatus'):
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
            if data and data.has_key('responseData') and data['responseData']['results']:
                for result in data['responseData']['results']:
                    if result:
                        results.append(urllib2.unquote(result['unescapedUrl']))
        return results

    def fetch_geocoding(self, query):
        """
        return all geocoding data on address or cordinate
        :return:
        """
        result = {}
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
            list_result = []

            for res in json_results:
                cur_result = {}

                cur_result["formatted_address"] = res["formatted_address"]
                cur_result["lat"] = res["geometry"]["location"]["lat"]
                cur_result["lng"] = res["geometry"]["location"]["lng"]
                list_result.append(cur_result)

        elif status == "ZERO_RESULTS":
            pass
        elif status == "OVER_QUERY_LIMIT":
            pass
        elif status == "REQUEST_DENIED":
            pass
        elif status == "INVALID_REQUEST":
            pass
        elif status == "UNKNOWN_ERROR":
            pass
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

class Youtube(object):
    def __init__(self, api_key=None):
        self.base_url = 'http://gdata.youtube.com/feeds/api/videos?'
        self.alt = 'json'
        if api_key:
            self.base_url += 'key=%s&' % (api_key)
            self.api_key = api_key
        self.error = None

    ###### DEPRECATED API
    def get_videos_by_point(self, point, radius_in_meters):
        videos_result = []
        # radius = radius_in_meters / 1000.0
        radius = radius_in_meters
        params = {'alt': self.alt, 'location': '%s' % (point,), 'location-radius': '%dkm' % (radius,)}
        data, self.error = general_utilities.get_page(self.base_url, params=params)
        jsonobj = json.loads(data)

        if not jsonobj:
            self.error(data.get('text'))
        else:
            if not 'entry' in jsonobj['feed']:
                pass
            else:
                for video in jsonobj['feed']['entry']:
                    if 'georss$where' not in video:
                        continue
                    source = 'YouTube'
                    screen_name = video['author'][0]['name']['$t']
                    profile_name = video['author'][0]['name']['$t']
                    profile_url = 'http://www.youtube.com/user/%s' % video['author'][0]['uri']['$t'].split('/')[-1]
                    media_url = video['link'][0]['href']
                    thumb_url = video['media$group']['media$thumbnail'][0]['url']
                    message = video['title']['$t']
                    latitude = video['georss$where']['gml$Point']['gml$pos']['$t'].split()[0]
                    longitude = video['georss$where']['gml$Point']['gml$pos']['$t'].split()[1]
                    time = datetime.strptime(video['published']['$t'], '%Y-%m-%dT%H:%M:%S.%fZ')
                    videos_result.append(
                        [source, screen_name, profile_name, profile_url, media_url, thumb_url, message, latitude,
                         longitude, time])
        return videos_result


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


class Panoramio(object):
    def __init__(self, number_of_results=100):
        self.base_url = 'http://www.panoramio.com/map/get_panoramas?'
        self.num_results = number_of_results

    def get_photos_by_box(self, lat, lon, half_dist_meters=100):
        box = general_utilities.get_bounding_box(float(lat), float(lon), half_dist_meters)

        params = {'set': 'public',
                  'order': 'popularity',
                  'size': 'original',
                  'from': 0,
                  'to': self.num_results,
                  'miny': box['lat_min'],
                  'minx': box['lon_min'],
                  'maxy': box['lat_max'],
                  'maxx': box['lon_max'],
                  'mapfilter': 'true'
                  }
        data, self.error = general_utilities.get_page(self.base_url, params=params)
        jsonobj = json.loads(data)
        photos = jsonobj['photos']
        photo_results = []
        for photo in photos:
            owner_name = photo['owner_name']
            owner_id = photo['owner_id']
            owner_url = photo['owner_url']
            media_url = photo['photo_file_url']
            photo_url = photo['photo_url']
            title = photo['photo_title']
            # time = datetime.strptime(photo['datetaken'], '%Y-%m-%d %H:%M:%S')
            time = photo['upload_date']
            latitude = photo['latitude']
            longitude = photo['longitude']
            photo_results.append(
                [owner_id, owner_name, owner_url, media_url, photo_url, title, latitude, longitude, time])

        return photo_results


class InstagramApi(object):
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()

        self.port = 12345

    def get_access_token(self, ):
        resource = 'instagram'
        scope = 'basic'
        authorize_url = 'https://instagram.com/oauth/authorize/'
        access_url = 'https://api.instagram.com/oauth/access_token'
        client_id = self.client_id
        client_secret = self.client_secret

        redirect_uri = 'http://localhost:%d' % (self.port)
        params = {'response_type': 'code', 'client_id': client_id, 'scope': scope,
                  'state': general_utilities.get_random_str(40), 'redirect_uri': redirect_uri}
        encoded_params = urllib.urlencode(params)
        authorize_url = '%s?%s' % (authorize_url, encoded_params)
        w = webbrowser.get()
        w.open(authorize_url)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', self.port))
        sock.listen(1)
        conn, addr = sock.accept()
        data = conn.recv(1024)
        conn.sendall(
            'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><head><title>Recon-ng</title></head><body>Response received. Return to Recon-ng.</body></html>')
        conn.close()

        # process the received data
        if 'error_description' in data:
            self.error(urllib.unquote_plus(re.search('error_description=([^\s&]*)', data).group(1)))
            return None
        authorization_code = re.search('code=([^\s&]*)', data).group(1)
        params = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': redirect_uri,
                  'client_id': client_id, 'client_secret': client_secret}
        resp = general_utilities.get_page(access_url, params)
        if 'error' in resp.json:
            return None
        access_token = resp.json['access_token']
        return access_token

    def get_photos_by_circle(self, lat, lon, radius_in_meters, min_time=1281139200, max_time=time.time()):

        base_url = 'https://api.instagram.com/v1/media/search'
        params = {'lat': lat, 'lng': lon, 'distance': radius_in_meters, 'min_timestamp': min_time,
                  'max_timestamp': max_time,
                  'access_token': self.access_token}

        data = general_utilities.get_page(base_url, params)
        jsonobj = json.loads(data)
        photos = jsonobj['data']
        media_results = []
        for media in photos:
            latitude = media['location']['latitude']
            longitude = media['location']['longitude']
            if not latitude or not longitude:
                continue
            screen_name = media['user']['username']
            profile_name = media['user']['full_name']
            profile_url = 'http://instagram.com/%s' % screen_name
            media_url = media['images']['standard_resolution']['url']
            try:
                message = media['caption']['text']
            except:
                message = ''
            try:
                time = datetime.fromtimestamp(float(media['created_time']))
            except ValueError:
                time = datetime(1970, 1, 1)
            media_results.append(
                [screen_name, profile_name, profile_url, media_url, message, time, latitude, longitude])

        return media_results


class TwitterApi(object):
    def __init__(self, api_key):
        self.api_key = api_key


class FacebookApi(object):
    def __init__(self, api_key):
        self.api_key = api_key


class Picasa(object):
    def __init__(self, api_key):
        self.api_key = api_key


class ShodanApi(object):
    def __init__(self, api_key):
        self.api_key = api_key
