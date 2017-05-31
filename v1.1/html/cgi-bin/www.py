#!/usr/bin/env python

import CGIHTTPServer
import BaseHTTPServer
import os

if __name__ == "__main__":
    os.chdir("/var/www/html/")
    server = BaseHTTPServer.HTTPServer
    handler = CGIHTTPServer.CGIHTTPRequestHandler
    server_address = ("", 80)
    # Note that only /cgi-bin will work:
    handler.cgi_directories = ["/cgi-bin", "/cgi-bin/subdir"]
    httpd = server(server_address, handler)
    httpd.serve_forever()
