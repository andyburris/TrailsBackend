#!/usr/bin/python3.6
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"<path/to/project/directory>")

from trailsbackend.trails_backend import app as application
application.secret_key = 'joshgordon'