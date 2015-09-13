import kuas_api.modules.error as error
from flask_apiblueprint import APIBlueprint
from kuas_api.modules.json import jsonify


# Create v2 blueprint
api_v2 = APIBlueprint(
    'api_v2', __name__,
    subdomain='',
    url_prefix='/v2')


def get_git_revision_short_hash():
    import subprocess
    return subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD']).decode("utf-8").strip("\n")


@api_v2.route('/')
def version_2():
    """Return API version
    """
    return jsonify(
        name="kuas-api version 2.",
        version="2",
        server_revision=get_git_revision_short_hash(),
        endpoints="https://kuas.grd.idv.tw:14769/v2/"
    )


@api_v2.errorhandler(401)
def unauthorized_error(err):
    return error.error_handle(status=401,
                              developer_message="token expired",
                              user_message="token expired",
                              error_code=401
                              )


# Add v2 routes
from kuas_api.views.v2.utils import routes as utils_routes
from kuas_api.views.v2.ap import routes as ap_routes
from kuas_api.views.v2.bus import routes as bus_routes
from kuas_api.views.v2.leave import routes as leave_routes
from kuas_api.views.v2.notifications import routes as notifications_routes

# Dirty from #593
routes = (
    utils_routes +
    ap_routes +
    bus_routes +
    leave_routes +
    notifications_routes
)

for r in routes:
    endpoint = r["options"].pop("endpoint", None)
    api_v2.add_url_rule(
        r["rule"],
        endpoint,
        r["view_func"],
        **r["options"]
    )
