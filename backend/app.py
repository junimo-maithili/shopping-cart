from flask import Flask
from flask_cors import CORS
from routes import api

app = Flask(__name__)


CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)

app.register_blueprint(api)

if __name__ == "__main__":
    app.run(debug=True)