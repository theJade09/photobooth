import constants
import os.path
from PIL import Image
import shutil

import tornado.web
import tornado.websocket
import tornado.options
import tornado.ioloop


from tornado.options import define,options

define("port", default=8888, help="run on the given port", type=int)

static_path = 'static'

class WebSocketServer(tornado.web.Application):
    """ Webserver for serving the web application. """

    def __init__(self):
        handlers = [
          (constants.WS_PATH, PhotoSocketHandler),
          (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
          (r'/(.*)', tornado.web.StaticFileHandler, {'path': static_path}),
          (r'/templates/(.*)', FrontEndClient, {'path': 'templates'}),
        ]
        settings = {
#            'template_path':os.path.join(os.path.dirname(__file__), "templates")
        }
        tornado.web.Application.__init__(self, handlers, **settings)


class FrontEndClient(tornado.web.RequestHandler):
    def get():
        self.render('index2.html', ws_url=constants.WS_URL)



class PhotoSocketHandler(tornado.websocket.WebSocketHandler):
    SOCKET_COUNTER = 0
    DESIRED_FILE_TYPES = 'jpg'

    @staticmethod
    def get_dir():
        """ Returns a list of only JPG files """
        x = set([i for i in os.listdir(constants.DIRECTORY_TO_WATCH)
                 if os.path.isfile(os.path.join(constants.DIRECTORY_TO_WATCH, i)) and 
                    i.lower().split('.')[-1] == 'jpg'])
        return x

    def open(self):
        # Keep track of which sockets are open/closed.
        self.socket_id = PhotoSocketHandler.SOCKET_COUNTER
        print 'Socket has been open (%d)' % self.socket_id
        PhotoSocketHandler.SOCKET_COUNTER+=1

        # Initialize Directory Listing
        self.current_dir = PhotoSocketHandler.get_dir()
        try:
          self.write_message('%s/%s' % (constants.PHOTOBOOTH_URL,
                             sorted(self.current_dir)[-1]))
        except:
          self.write_message('directory is empty')

        # Start the polling loop for the directory.
        self.loop = tornado.ioloop.PeriodicCallback(self.check_directory, 500)
        self.loop.start()

    def resize_image(self, image_name):
        """ Resizes the image and returns the new full path to image """
        original_path = os.path.join(constants.DIRECTORY_TO_WATCH, image_name)
        resize_path = os.path.join(constants.RESIZE_DIRECTORY, image_name)

        # Resize only if greater than 1k
        if os.path.getsize(original_path) > 1024000:
            img = Image.open(original_path)
            new_img = img.resize([i/4 for i in img.size], Image.LINEAR)
            new_img.save(resize_path, 'jpeg')
        else:
            shutil.copyfile(original_path, resize_path)

        return image_name 

    def check_directory(self):
        """ Checks directory for any changes and sends them over the ws """
        new_dir = PhotoSocketHandler.get_dir()

        # Only send over new files.
        if len(new_dir) > len(self.current_dir):
            new_elements = sorted(list(new_dir - self.current_dir))
            for i in new_elements:
                self.resize_image(i)
                i_fullpath = '%s/%s' % (constants.PHOTOBOOTH_URL, i)
                self.write_message(i_fullpath)
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
