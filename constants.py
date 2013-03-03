import os

BASE_DIR = '/Users/BunBe/Sites'
PHOTOBOOTH_DIRECTORY = 'photobooth'
DIRECTORY_TO_WATCH = os.path.join(BASE_DIR, PHOTOBOOTH_DIRECTORY)
RESIZE_DIRECTORY = os.path.join(DIRECTORY_TO_WATCH, 'small')

if not os.path.isdir(RESIZE_DIRECTORY):
 os.mkdir(RESIZE_DIRECTORY)

HOSTNAME = 'macair.local'
USERNAME = 'BunBe'
PHOTOBOOTH_URL = 'http://%s/~%s/%s' % (HOSTNAME, USERNAME, PHOTOBOOTH_DIRECTORY)

WS_PATH = '/new_photo'
WS_URL = 'ws://%s:8888/%s' % (HOSTNAME, WS_PATH)
