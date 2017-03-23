# -*- coding: utf-8 -*-
import os
from gevent.wsgi import WSGIServer
from komafly import app

# if __name__ == '__main__':
#     http_server = WSGIServer(('',5000),app)
#     http_server.serve_forever()

app.run(debug=True)