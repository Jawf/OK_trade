#!/usr/bin/env python
# -*- coding: utf-8 -*-


import hashlib
import urllib
import urllib.parse
import urllib.request

import requests

try:
    from app.settings import *
except Exception as e:
    from settings import *


class OK_Utils:

    def __init__(self,params):
        self.params = params

    def create_sign(self,params):
        sign = {}
        if isinstance(params, dict):
            for key in sorted(params.keys()):
                sign[key] = str(params[key])

            data = sign
            data['secret_key'] = self.params['SECRET_KEY']
            data = urllib.parse.urlencode(sign, doseq=False, safe='', encoding=None, errors=None)

            #print(data)
        else:
            raise TypeError('{0} should has attributes of "items"'.format(params))

        return hashlib.md5(data.encode('utf8')).hexdigest().upper()

    def http_get_request(self,url, params, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        }

        if add_to_headers:
            headers.update(add_to_headers)
        #postdata = self.create_sign(params)
        postdata = urllib.parse.urlencode(params, doseq=False, safe='', encoding=None, errors=None)
        try:
            response = requests.get(url, postdata, headers=headers, timeout=20)

            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print("httpGet failed, detail is:%s" % e)
            return None

    def http_post_request(self,url, params, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        }

        if add_to_headers:
            headers.update(add_to_headers)
        params['sign'] = self.create_sign(params)

        #print(params)
        #print(url)
        try:
            response = requests.post(url, params, headers=headers, timeout=20)  #
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except BaseException as e:
            print("httpPost failed, detail is:%s" % e)
            return None

    def api_key_get(self,params, request_path):
        method = 'get'
        host_url = self.params['URL']

        url = host_url + '{0}.do?'.format(request_path)
        #print(url)
        #print(params)
        return self.http_get_request(url,params)

    def api_key_post(self,params, request_path):
        method = 'post'
        host_url = OK_PARAMS['URL']
        params.update({'api_key': self.params['api_key']})
        #print(params)
        url = host_url + '{0}.do'.format(request_path)
        return self.http_post_request(url,params)



if __name__ == '__main__':
    ok = OK_Utils(OK_PARAMS)


    path = OK_API['DEPTH']

    params={'symbol':'eth_usdt',
      }
    result = ok.api_key_get(params,path[0])
    print(result['asks'][-5:-1])