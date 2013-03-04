import os

BASE_DIR = '/Users/BunBe/Sites/'
HOME_FOLDER = 'photobooth'
WATCH_FOLDER = 'CANON'
DIRECTORY_TO_WATCH = os.path.join(BASE_DIR, HOME_FOLDER, WATCH_FOLDER)
RESIZE_DIRECTORY = os.path.join(BASE_DIR, HOME_FOLDER, 'small')

if not os.path.isdir(RESIZE_DIRECTORY):
 os.mkdir(RESIZE_DIRECTORY)

if not os.path.isdir(DIRECTORY_TO_WATCH):
 os.mkdir(DIRECTORY_TO_WATCH)

HOSTNAME = 'macair.local'
USERNAME = 'BunBe'
IMAGE_PATH = '%s/%s/%s' % (HOME_FOLDER, WATCH_FOLDER, 'small')
PHOTOBOOTH_URL = 'http://%s/~%s/%s' % (HOSTNAME, USERNAME, IMAGE_PATH)

WS_PATH = '/new_photo'
WS_URL = 'ws://%s:8888/%s' % (HOSTNAME, WS_PATH)
