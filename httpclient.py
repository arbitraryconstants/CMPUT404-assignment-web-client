#!/usr/bin/env python
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
import urllib
import json

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPResponse(object):
    
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

        
class HTTPClient(object):

    
    def parse_url(self, url):
        # By okigan (https://stackoverflow.com/users/142207/okigan) on stackoverflow:
        # https://stackoverflow.com/questions/27745/getting-parts-of-a-url-regex
        pattern = (r'^'
               r'((?P<schema>.+?)://)?'
               r'((?P<user>.+?)(:(?P<password>.*?))?@)?'
               r'(?P<host>.*?)'
               r'(:(?P<port>\d+?))?'
               r'(?P<path>/.*?)?'
               r'(?P<query>[?].*?)?'
               r'$'
               )
        regex = re.compile(pattern)
        m = regex.match(url)
        self.url_dictionary = m.groupdict() if m is not None else None

        if not self.url_dictionary["path"]:
            self.url_dictionary["path"] = "/"
            
    
    def get_host_port(self, url):
        host = self.url_dictionary["host"]
        port = self.url_dictionary["port"]
       
        if not port:
            port = 80
        port = int(port)
        
        return host, port
   

    def connect(self, host, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        return client_socket

    
    def get_code(self, response):
        code = int(response.split()[1])
        return code
       
        
    def get_headers(self, method, path, user_agent, host, content=None, content_type="application/x-www-form-urlencoded"):
        
        if method == "GET":
            headers = "User-Agent: " +  user_agent + "\r\n" + \
                      "Host: " + host + "\r\n" + \
                      "Accept: */* \r\n" + \
                      "\r\n"
            
        if method == "POST":
            if content:
                content_length = len(content)
                headers = "User-Agent: " +  user_agent + "\r\n" + \
                          "Host: " + host + "\r\n" + \
                          "Accept: */* \r\n" + \
                          "Content-Length: " + str(content_length) + "\r\n" + \
                          "Content-Type: " + content_type + "\r\n" + \
                          "\r\n"
            else:
                headers = "User-Agent: " +  user_agent + "\r\n" + \
                          "Host: " + host + "\r\n" + \
                          "Accept: */* \r\n" + \
                          "Content-Length: " + '0' + "\r\n" + \
                          "Content-Type: " + content_type + "\r\n" + \
                          "\r\n"
            
        return headers

    
    def get_body(self, response):
        try:
            body = response.split("\r\n\r\n")[1]
            return body
        except:
            return ""
       

    def get_content(self, args):
        if not args:
            return None
        content = urllib.urlencode(args)
        return content

    
    # Read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    
    def GET(self, url, args=None):
        self.parse_url(url)
        method = "GET"
        host, port = self.get_host_port(url)
        path = self.url_dictionary["path"]
        user_agent = "curl/7.43.0"
        client_socket = self.connect(host, port)
        
        query = self.url_dictionary["query"]
        if query:
            status_line = "GET" + " " + path + query + " HTTP/1.1\r\n"
        else:
            status_line = "GET" + " " + path + " HTTP/1.1\r\n"
            
        headers = self.get_headers(method, path, user_agent, host)
        request = status_line + headers
        print ""
        print "----------GET REQUEST-----------"
        print request
        client_socket.sendall(request)

        response = self.recvall(client_socket)
        print ""
        print "----------HTTP RESPONSE----------"
        print response
        code = self.get_code(response)
        body = self.get_body(response)

        return HTTPResponse(code, body)


    def POST(self, url, args=None):
        self.parse_url(url)
        method = "POST"
        host, port = self.get_host_port(url)
        path = self.url_dictionary["path"]
        user_agent = "curl/7.43.0"
        
        client_socket = self.connect(host, port)
        query = self.url_dictionary["query"]
        if query:
            status_line = "GET" + " " + path + query + " HTTP/1.1\r\n"
        else:
            status_line = "GET" + " " + path + " HTTP/1.1\r\n"

        status_line = "POST" + " " + path + " HTTP/1.1\r\n"
        content = self.get_content(args)
        headers = self.get_headers(method, path, user_agent, host, content)
        
        if content:
            request = status_line + headers + content
        else:
            request = status_line + headers

        print ""
        print "----------POST REQUEST-----------"
        print request
        client_socket.sendall(request)

        response = self.recvall(client_socket)
        print ""
        print "----------HTTP RESPONSE----------"
        print response
        code = self.get_code(response)
        body = self.get_body(response)
        
        return HTTPResponse(code, body)    

   
    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )


if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
    
    else:
        print client.command( sys.argv[1] )   
