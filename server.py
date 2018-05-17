import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path

from handlers import GameSocketHandler
from tornado.web import StaticFileHandler

root = os.path.dirname(__file__)


from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/game", GameSocketHandler),
            (r"/(.*)", StaticFileHandler, {
                'path': root,
                'default_filename': 'index.html',
            }),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
        )
        super(Application, self).__init__(handlers, **settings)


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()