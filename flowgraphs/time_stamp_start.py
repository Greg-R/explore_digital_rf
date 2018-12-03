# this module will be imported in the into your flowgraph

import datetime

iso_time = datetime.datetime.now().replace(microsecond=0).isoformat() +'Z'
