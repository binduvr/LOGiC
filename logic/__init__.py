from flask import Flask
from flask_cors import CORS


from logic.location_data.controllers import location_data
from logic.offgrid_simulator.controllers import offgrid_simulator
from logic.report_generator.controllers import report_generator

import logic.config

app = Flask(__name__)
CORS(app)

# Set config from config presets
app.config.from_object('logic.config.TestingConfig')

# Register the different blueprints
app.register_blueprint(location_data, url_prefix='/location_data')
app.register_blueprint(offgrid_simulator, url_prefix='/offgrid_simulator')
app.register_blueprint(report_generator, url_prefix='/report')
