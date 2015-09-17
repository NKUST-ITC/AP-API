from kuas_api import app
from flask.ext.compress import Compress

if __name__ == "__main__":
    Compress(app)
    app.run(host="0.0.0.0", port=14769, debug=True)
