import logging
from flask import Flask

from toolbox.conf_loader import RootConfiguration
from toolbox.logger import get_logger
from toolbox.database import db

conf = RootConfiguration()
log = get_logger(__name__)

log.info("Starting root app...")
app = Flask(__name__)

log.info("Connect to database")
app.config['SQLALCHEMY_DATABASE_URI'] = conf.get('databaseURI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = conf.get('databaseTrackModifications')

from modules.datacenter.api import app as datacenter_app
app.register_blueprint(datacenter_app, url_prefix = '/datacenters')

from modules.node.api import app as node_app
app.register_blueprint(node_app, url_prefix = '/nodes')

from modules.user.api import app as user_app
app.register_blueprint(user_app, url_prefix = '/users')

from modules.project.api import app as project_app
app.register_blueprint(project_app, url_prefix = '/projects')

# init app and db
db.init_app(app)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(
        host = conf.get('devServerHost'),
        port = conf.get('devServerPort'),
        debug = True,
        threaded = True
    )