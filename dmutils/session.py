import flask_session
import redis

import dmutils.cloudfoundry as cf

def init_app(app):
    vcap_services = cf.get_vcap_services(app)

    redis_service_name = app.config["DM_REDIS_SERVICE_NAME"]
    redis_service = cf.get_service_by_name_from_vcap_services(vcap_services, redis_service_name)

    app.config["SESSION_REDIS"] = redis.from_url(redis_service["credentials"]["url"])
    flask_session.Session(app)