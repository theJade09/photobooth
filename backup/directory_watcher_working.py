# File does not have image resizing.  HTML file should read from ~/BunBe/photobooth.

import tornado.web
import tornado.websocket
import tornado.options
import tornado.ioloop
import os.path

import constants
from tornado.options import define,options

define("port", default=8888, help="run on the given port", type=int)

class WebSocketServer(tornado.web.Application):
    """ Webserver for serving the web application. """

    def __init__(self):
        handlers = [
          (constants.WS_PATH, PhotoSocketHandler)
        ]
        settings = {}
        tornado.web.Application.__init__(self, handlers, **settings)


class PhotoSocketHandler(tornado.websocket.WebSocketHandler):
    SOCKET_COUNTER = 0
    DESIRED_FILE_TYPES = 'jpg'

    @staticmethod
    def get_dir():
        return set(os.listdir(constants.DIRECTORY_TO_WATCH))

    def open(self):
        # Keep track of which sockets are open/closed.
        self.socket_id = PhotoSocketHandler.SOCKET_COUNTER
        print 'Socket has been open (%d)' % self.socket_id
        PhotoSocketHandler.SOCKET_COUNTER+=1

        # Initialize Directory Listing
        self.current_dir = PhotoSocketHandler.get_dir()
        try:
          self.write_message(sorted(self.current_dir)[-1])
        except:
          self.write_message('directory is empty')

        # Start the polling loop for the directory.
        self.loop = tornado.ioloop.PeriodicCallback(self.check_directory, 500)
        self.loop.start()

    def check_directory(self):
        """ Checks directory for any changes and sends them over the ws """
        new_dir = PhotoSocketHandler.get_dir()

        # Only send over new files.
        if len(new_dir) > len(self.current_dir):
            new_elements = sorted(list(new_dir - self.current_dir))
            for i in new_elements:
                self.write_message(str(i))
            self.current_dir = new_dir
        else:
            # If the directory somehow changed (removed file),
            # the current dir is now smaller, but we don't send
            # over a message to indicate this.
            if len(new_dir) != len(self.current_dir):
                self.current_dir = new_dir

    def write_message(self, msg, *args, **kwargs):
        try:
          print "(%d) Sending message %s" % (self.socket_id, msg)
          super(PhotoSocketHandler, self).write_message(msg, binary=False)
        except Exception, e:
          print "(%d) Ran into exception %s" % (self.socket_id, str(e))
          self.close()

    def close(self):
        print "socket is now closed (%d)" % self.socket_id
        self.loop.stop()

def main():
    tornado.options.parse_command_line()
    app = WebSocketServer()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
