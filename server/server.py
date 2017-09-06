import json

import tornado.ioloop
from tornado.web import RequestHandler

import data


class PostArticleHandler(RequestHandler):
    def post(self):
        s = self.request.body.decode('gb18030')
        d = json.loads(s)

        data.add_article(d['title'], d['text'], d['cate'])
        self.write('ok')


class GetListHandler(RequestHandler):
    def get(self):
        lst = data.get_list()
        s = json.dumps(lst)

        self.write(s.encode('gb18030'))


class GetArticleHandler(RequestHandler):
    def get(self):
        aid = self.get_argument('aid')

        b = data.get_article(aid)

        if b is not None:
            self.write(b)


class DeleteArticleHandler(RequestHandler):
    def post(self):
        s = self.request.body.decode('gb18030')
        del_lst = json.loads(s)

        data.del_article(del_lst)


class Error404_Handler(RequestHandler):
    def post(self):
        self.write('HTTP ERROR 404: 无此页面')

    def get(self):
        self.write('HTTP ERROR 404: 无此页面')


def make_app():
    return tornado.web.Application([
        (r'/post_article', PostArticleHandler),
        (r'/get_article', GetArticleHandler),
        (r'/get_list', GetListHandler),
        (r'/del_article', DeleteArticleHandler),
        (r'^.*$', Error404_Handler)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(17828)

    tornado.ioloop.IOLoop.current().start()
