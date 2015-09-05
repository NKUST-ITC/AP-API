import json
from flask import current_app


def jsonify(*args, **kwargs):
    """Creates a :class:`~flask.Response` with the JSON representation of
    the given arguments with an :mimetype:`application/json` mimetype.  The
    arguments to this function are the same as to the :class:`dict`
    constructor.

    Example usage::

        from flask import jsonify

        @app.route('/_get_current_user')
        def get_current_user():
            return jsonify(username=g.user.username,
                           email=g.user.email,
                           id=g.user.id)

    This will send a JSON response like this to the browser::

        {
            "username": "admin",
            "email": "admin@localhost",
            "id": 42
        }

    For security reasons only objects are supported toplevel.  For more
    information about this, have a look at :ref:`json-security`.

    This function's response will be pretty printed if it was not requested
    with ``X-Requested-With: XMLHttpRequest`` to simplify debugging unless
    the ``JSONIFY_PRETTYPRINT_REGULAR`` config parameter is set to false.
    Compressed (not pretty) formatting currently means no indents and no
    spaces after separators.

    .. versionadded:: 0.2
    """

    indent = 2
    separators = (',', ':')

    # Note that we add '\n' to end of response
    # (see https://github.com/mitsuhiko/flask/pull/1262)
    rv = current_app.response_class(
        (json.dumps(
            dict(*args, **kwargs),
            indent=indent,
            separators=separators,
            ensure_ascii=False
        ), '\n'),
        mimetype='application/json')
    return rv
