#!/usr/bin/env python2.7
#  coding: utf-8 
import SocketServer
import mimetypes

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Copyright 2016 Sarah Van Belleghem
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

class MyWebServer(SocketServer.BaseRequestHandler):
    
	def handle(self):
	        self.data = self.request.recv(1024).strip()
	        print ("Got a request of: %s\n" % self.data)	

		#parse the given data into headers, method, body and path
		self.parse_request(self.data)
	
		#check that the root website is either the IP or the localhost
		if (self.host == "localhost:8080" or self.host == "127.0.0.1:8080"):
			self.file_requested = "www/" + self.path
			split_path = self.path.split("/")
			#check that the user is only looking in www or deep.
			if(len(split_path) == 1 or split_path[0] == "deep"):
				#check the path to make sure they are only looking for index.html or base.css,
				#and determine the mime type
				#http://stackoverflow.com/questions/21397565/mixing-mime-types-with-httpserver-in-python 01/14/2016
				#self.path = self.path.rstrip("/")
				file_name = split_path[-1]
				if (self.path == "" or self.path == "deep"):
					self.file_requested += "/index.html"
					self.mimetype, _ = mimetypes.guess_type("index.html") 
					self.show_page()
				elif (file_name == "index.html" or file_name == "base.css" or file_name == "deep.css"):
					self.mimetype, _ = mimetypes.guess_type(self.path) 
					self.show_page()
				else:
					self.error_404()
			#if they try to see something that isnt the www or deep page
			else:
				self.error_404()
		#if the host name is not correct
		else:
			self.error_404()

	#display the error page not found message
	#http://blog.wachowicz.eu/?p=256 01/13/2016
	def error_404(self):
		print("WARNING: File Not Found")
		response_content = "HTTP/1.1 404 NOT FOUND\r\n\r\n<html><body><h1>Error 404: File not found</h1>"
		self.request.sendall(response_content)		
	
	#display the page
	#http://stackoverflow.com/questions/21397565/mixing-mime-types-with-httpserver-in-python 01/14/2016
	def show_page(self):
		f = open(self.file_requested, "r")
		file_content = f.read()
		f.close()
		self.request.sendall("HTTP/1.1 200 OK\r\n")
		self.request.sendall("Content-Type: "+self.mimetype+"\r\n")
		self.request.sendall("Content-Length: "+ str(len(file_content))+"\r\n\r\n")
		self.request.sendall(file_content)


#http://stackoverflow.com/questions/18563664/socketserver-python 01/13/2016
#parses the data received in the self.data
   	def parse_request(self, req):
        	headers = {}
        	lines = req.splitlines()
        	inbody = False
        	body = ''
        	for line in lines[1:]:
        	    if line.strip() == "":
        	        inbody = True
        	    if inbody:
        	        body += line
        	    else:
        	        k, v = line.split(":", 1)
        	        headers[k.strip()] = v.strip()
        	method, path, _ = lines[0].split()
        	self.path = path.strip("/")
        	self.method = method
        	self.headers = headers
        	self.body = body	
		self.host = self.headers["Host"]

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()




















