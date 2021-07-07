import atexit
import logging
import logging.config
import platform
import yaml
import os
from flask import Flask, Blueprint
from app.celery import celery_app

from app.utils.core import JSONEncoder, db, scheduler
from app.api.router import router


def create_app(config_name, config_path=None):
    app = Flask(__name__)
    # read config file
    if not config_path:
        pwd = os.getcwd()
        config_path = os.path.join(pwd, 'config/config.yaml')
    if not config_name:
        config_name = 'PRODUCTION'

    # read config file
    conf = read_yaml(config_name, config_path)
    app.config.update(conf)

    # update Celery info
    celery_conf = "redis://{}:{}/{}".format(app.config['REDIS_HOST'], app.config['REDIS_PORT'], app.config['REDIS_DB'])
    celery_app.conf.update({"broker_url": celery_conf, "result_backend": celery_conf})

    # register api
    register_api(app=app, routers=router)

    # return Json encoder
    app.json_encoder = JSONEncoder

    # db connection
    db.app = app
    db.init_app(app)

    if app.config.get("SCHEDULER_OPEN"):
        scheduler_init(app)

    if not os.path.exists(app.config['LOGGING_PATH']):
        os.mkdir(app.config['LOGGING_PATH'])

    if not os.path.exists(app.config['REPORT_PATH']):
        os.mkdir(app.config['REPORT_PATH'])

    with open(app.config['LOGGING_CONFIG_PATH'], 'r', encoding='utf-8') as f:
        dict_conf = yaml.safe_load(f.read())
    logging.config.dictConfig(dict_conf)

    with open(app.config['RESPONSE_MESSAGE'], 'r', encoding='utf-8') as f:
        msg = yaml.safe_load(f.read())
        app.config.update(msg)

    return app


def read_yaml(config_name, config_path):
    """
    config_name:
    config_path:
    """
    if config_name and config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            conf = yaml.safe_load(f.read())
        if config_name in conf.keys():
            return conf[config_name.upper()]
        else:
            raise KeyError('not found')
    else:
        raise ValueError('please input right name')


def register_api(app, routers):
    for router_api in routers:
        if isinstance(router_api, Blueprint):
            app.register_blueprint(router_api)
        else:
            try:
                endpoint = router_api.__name__
                view_func = router_api.as_view(endpoint)
                url = '/{}/'.format(router_api.__name__.lower())
                if 'GET' in router_api.__methods__:
                    app.add_url_rule(url, defaults={'key': None}, view_func=view_func, methods=['GET', ])
                    app.add_url_rule('{}<string:key>'.format(url), view_func=view_func, methods=['GET', ])
                if 'POST' in router_api.__methods__:
                    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
                if 'PUT' in router_api.__methods__:
                    app.add_url_rule('{}<string:key>'.format(url), view_func=view_func, methods=['PUT', ])
                if 'DELETE' in router_api.__methods__:
                    app.add_url_rule('{}<string:key>'.format(url), view_func=view_func, methods=['DELETE', ])
            except Exception as e:
                raise ValueError(e)


def scheduler_init(app):
    """
    :param app:
    :return:
    """
    if platform.system() != 'Windows':
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            scheduler.init_app(app)
            scheduler.start()
            app.logger.debug('Scheduler Started,---------------')
        except:
            pass

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

        atexit.register(unlock)
    else:
        msvcrt = __import__('msvcrt')
        f = open('scheduler.lock', 'wb')
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            scheduler.init_app(app)
            scheduler.start()
            app.logger.debug('Scheduler Started,----------------')
        except:
            pass

        def _unlock_file():
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except:
                pass

        atexit.register(_unlock_file)
