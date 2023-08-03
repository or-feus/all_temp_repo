from collections import Counter
from functools import partial
from http import HTTPStatus

from flask import Flask, request, Response
from flask_injector import FlaskInjector
from redis import Redis
from redis_module import RedisModule
from view_storage_backend import ViewsStorageBackend
from redis_backend import RedisBackend
app = Flask(__name__)
storage = Counter()

PIXEL = (
    b'GIF89a\x01\x00\x01\x00\x00\x00\x00\x00'
    b'\x00\x00\xff\xff\xff!\xf9\x04\x01\x00'
    b'\x00\x00\xff\xff\xff!\xf9\x04\x01\x00'
    b'\x00\x00\xff\xff\xff!\xf9\x04\x01\x00;'
)


@app.route('/track')
def track(storage: ViewsStorageBackend):
    try:
        referer = request.headers["Referer"]
    except KeyError:
        return Response(status=HTTPStatus.BAD_REQUEST)

    storage.increment(referer)

    return Response(
        PIXEL, headers={
            "Content-Type": "image/gif",
            "Expires": "Mon, 01 Jan 1990 00:00:00 GMT",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
        }
    )


@app.route('/stats')
def stats(storage: ViewsStorageBackend):
    return storage.most_common(10)


@app.route('/test')
def test():
    return """
    <html>
    <head></head>
    <body><img src="/track"></body>
    </html>
    """


if __name__ == '__main__':

    # FlaskInjector(app=app, modules=[RedisModule()])
    app.run(host="localhost", port=8000)
