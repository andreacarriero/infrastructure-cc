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

from modules.datacenter.admin_api import app as datacenter_admin_app
app.register_blueprint(datacenter_admin_app, url_prefix = '/admin/datacenters')

from modules.node.api import app as node_app
app.register_blueprint(node_app, url_prefix = '/nodes')

from modules.node.admin_api import app as node_admin_app
app.register_blueprint(node_admin_app, url_prefix = '/admin/nodes')

from modules.user.admin_api import app as user_admin_app
app.register_blueprint(user_admin_app, url_prefix = '/admin/users')

from modules.project.admin_api import app as project_admin_app
app.register_blueprint(project_admin_app, url_prefix = '/admin/projects')

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