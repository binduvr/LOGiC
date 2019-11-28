from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import logic.config

app = Flask(__name__)
CORS(app)

# Set config from config presets
app.config.from_object('logic.config.TestingConfig')

# Set rate Limiter
limiter = Limiter(app, default_limits = ["1/second"], key_func=get_remote_address)

# Register the different blueprints
from logic.location_data.controllers import location_data
from logic.offgrid_simulator.controllers import offgrid_simulator
from logic.report_generator.controllers import report_generator

app.register_blueprint(location_data, url_prefix='/location_data')
app.register_blueprint(offgrid_simulator, url_prefix='/offgrid_simulator')
app.register_blueprint(report_generator, url_prefix='/report')
