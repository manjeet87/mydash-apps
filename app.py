from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
import dash

# from app1 import app as app1
# from app2 import app as app2
from flask_app import flask_app

from gst_dash.gst_ds_leaflet import app as app1
from ewb_dash.ewb_dash import app as app2

application = DispatcherMiddleware(flask_app, {
    '/gst_dash': app1.server,
    '/ewb_dash': app2.server,
})

if __name__ == '__main__':
    run_simple('localhost', 8051, application)