#!/bin/bash
#
# Script wsstop.sh
# Stop nginx web server.

sudo /usr/local/nginx/sbin/nginx -s quit
ps aux | grep nginx
