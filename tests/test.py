import time
from datetime import datetime
import pprint as pp

import logic.offgrid_simulator.processor as processor
import logic.offgrid_simulator.controllers as controllers

# Create input dictionary
# input_dict = {
#     'project_name': 'hoevelaken',
#     'country_code': 'NL',
#     # NOTE: Make sure they are sent as floats.
#     'latitude': 51,
#     'longitude': 5,
#     'demands': {
#         'residential_demand': 35000,
#         'commercial_demand': 0,
#         'industrial_demand': 0
#     },
#     'active_components': {
#         'wind': True,
#         'solar': True,
#         'storage': True,
#         'dieselgen': False,
#         'grid_connection': False
#     },
#     'additional_parameters': {'blackout_frequency': 0}
# }

# session_id = time.strftime("%Y%m%d%H%M%S", time.gmtime())
# controllers.process_request(input_dict, session_id)

# session_id = '20191018120134'
# output_dict = controllers.get_result(session_id)

output_id = controllers.handle_request()
pp.pprint(controller.get_result(output_id))
# pp.pprint(results)
