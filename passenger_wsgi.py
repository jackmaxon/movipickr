import sys
import os

sys.path.insert(0, '/home/s6jilwoagjb6/public_html/movipickr')
os.environ['FLASK_APP'] = 'app.py'

from app import app as application