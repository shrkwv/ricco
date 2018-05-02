#!/usr/bin/env python
# System modules
from Queue import Queue
from threading import Thread
import time
import urllib2

import utils.scraper as scraper


class SetQueue(Queue):
    def _init(self, maxsize):
        Queue._init(self, maxsize)
        self.all_items = set()

    def _put(self, item):
        if item not in self.all_items:
            Queue._put(self, item)
            self.all_items.add(item)

    def _get(self):
        return self.queue.pop()


class Download(object):
    # Set up some global variable
    def __init__(self, start_url, num_fetch_threads=4, RECURSIVE=False):
        self.num_fetch_threads = num_fetch_threads
        self.start_url = start_url
        self.RECURSIVE = RECURSIVE
        self.download_queue = SetQueue()
        self.downloaded_links = []
        self.to_download_links = SetQueue()
        self.pages = {}
        self.to_download_links.put(start_url)
        self.DONE = False
        self.page_links = []

    def getSecondaryUrl(self, url):
        """
        returns the www / not www url for the entered url
        """
        if "://www." in url:
            second_url = url.split("://www.")
            second_url = second_url[0] + "://" + second_url[1]
        else:
            # TODO better one!
            second_url = url.split("://")
            second_url = second_url[0] + "://" + "www." + second_url[1]
        return second_url

    def getInsiteUrls(self, start_html, url_site):
        """
        gets all the links that contains the strat urls as list
        """
        # move to scraper!!!!
        second_url = self.getSecondaryUrl(url_site)
        urls = scraper.get_urls(start_html)  # remove all /
        links = scraper.get_a_hrefs(start_html, url_site)  # remove all /
        links = links.values()
        all_links = list(set(urls + links))
        site_links = []
        for link in all_links:
            if url_site in link:
                if link.endswith("/"):
                    link = link[:-1]
                site_links.append(link)
        return site_links

    def downloadPages(self, i, q):
        """This is the worker thread function.
        It processes items in the queue one after
        another.  These daemon threads go into an
        infinite loop, and only exit when
        the main thread ends.
        """

        while True:
            # print '%s: Looking for the next link to download' % i
            url = q.get()
            # print '%s: Downloading:' % i, url
            request = urllib2.Request(url)
            # proxy = urllib2.ProxyHandler()
            # opener = urllib2.build_opener(proxy)
            # urllib2.install_opener(opener)
            try:
                response = urllib2.urlopen(request, timeout=5)
                self.pages[url] = response.read()
                self.downloaded_links.append(url)
                    # print "################### RECURSIVE ########################"
                self.page_links = self.getInsiteUrls(self.pages[url], self.start_url)
                    # print self.page_links
                self.page_links = list(set(self.page_links) - set(self.downloaded_links))
                    # print self.page_links
                if self.page_links:
                    for link in self.page_links:
                        self.to_download_links.put(link)
                q.task_done()
            except urllib2.URLError, e:
                # print e
                q.task_done()
            except urllib2.HTTPError, e:
                # print e
                q.task_done()
            except Exception, e:
                # print e
                q.task_done()

    def getPages(self):
        """
        get all pages downloaded
        """
        # Set up some threads to fetch the enclosures
        if not self.RECURSIVE:
            self.pages[self.start_url] = urllib2.urlopen(self.start_url).read()
        else:
            for i in range(self.num_fetch_threads):
                worker = Thread(target=self.downloadPages, args=(i, self.download_queue))
                worker.setDaemon(True)
                worker.start()

            while not self.DONE:
                if not self.to_download_links.empty():
                    # print "link add to queue"
                    link = self.to_download_links.get()
                    # print link
                    self.download_queue.put(link)
                else:
                    if self.download_queue.empty() and self.download_queue.unfinished_tasks == 0:
                        self.DONE = True
                    else:
                        time.sleep(1)




            # start = time.time()
            # print '*** Main thread waiting'
            self.download_queue.join()
            # print '*** Done %s' % (time.time()-start)

        return self.pages
