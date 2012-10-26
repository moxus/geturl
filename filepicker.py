'''
Created on 26.10.2012

@author: christian.sagmueller@gmail.com
'''

from urllib2 import Request, urlopen, build_opener
from MultipartPostHandler import MultipartPostHandler
import urllib
import json

class Filepicker:
    sfurl = 'https://www.filepicker.io/api/path/storage'
    fpapiurl = 'https://developers.filepicker.io/getKey'

    def __init__(self, email='', apikey=''):
        self.email = email
        self.apikey = apikey
        if not self.apikey:
            self.load_apikey()

    def load_apikey(self):
        assert self.email
        url = '%s?email=%s' % (self.fpapiurl, self.email)
        print url
        r = Request(url)
        res = urlopen(r)
        self.apikey = res.read()

    def upload_file(self, filename):
        assert self.apikey
        fileurl = urllib.pathname2url(filename)
        file_handle = open(filename)
        data = {'fileUpload': file_handle, 'apikey': self.apikey}
        r = Request('%s/%s' % (self.sfurl, fileurl), data)
        opener = build_opener(MultipartPostHandler)
        res = opener.open(r)
        res_data = res.read()
        print res_data
        res_json = json.loads(res_data)
        return res_json['data'][0]['url']

