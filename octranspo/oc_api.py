import os
import dotenv
import requests
# http://www.octranspo.com/developers/documentation#method-GTFS
# https://developers.google.com/transit/gtfs/reference/#tripstxt

# Adjustment Age
# AdjustmentAge indicates the last time (in minutes and adjusted in whole and fractional minutes) when the GPS data available for the bus was used to determine the AdjustedScheduleTime. The higher the number the less reliable the AdjustedScheduleTime is.

# If the AdjustmentAge is a negative value, it indicates that the AdjustedScheduleTime contains the planned scheduled time.
assert dotenv.load(__file__.replace('octranspo/oc_api.py', '.env'))


def route_summary_for_stop(stop_no: int) -> dict:
    if not(dotenv.get('APP_ID') or dotenv.get('API_KEY')):
        raise NameError('MissingAPIandAPPID')
    return requests.post(
        'https://api.octranspo1.com/v1.2/GetRouteSummaryForStop',
        data={
            "appID": dotenv.get('APP_ID'),
            "apiKey": dotenv.get('API_KEY'),
            "stopNo": stop_no,
            "format": "json"
        }
    ).json()


def next_trips_all_routes(stop_no: int) -> dict:
    if not(dotenv.get('APP_ID') or dotenv.get('API_KEY')):
        raise NameError('MissingAPIandAPPID')
    return requests.post(
        'https://api.octranspo1.com/v1.2/GetNextTripsForStopAllRoutes',
        data={
            "appID": dotenv.get('APP_ID'),
            "apiKey": dotenv.get('API_KEY'),
            "stopNo": stop_no,
            "format": "json"
        }
    ).json()


def next_trips_for_stop(stop_no: int, route_no: int) -> dict:
    if not(dotenv.get('APP_ID') or dotenv.get('API_KEY')):
        raise NameError('MissingAPIandAPPID')
    return requests.post(
        'https://api.octranspo1.com/v1.2/GetNextTripsForStop',
        data={
            "appID": dotenv.get('APP_ID'),
            "apiKey": dotenv.get('API_KEY'),
            "stopNo": stop_no,
            "routeNo": route_no,
            "format": "json"
        }
    ).json()


def gtfs(table: str, id_=None, column=None, value=None, limit=None) -> dict:
    if not(dotenv.get('APP_ID') or dotenv.get('API_KEY')):
        raise NameError('MissingAPIandAPPID')
    data = {"appID": dotenv.get('APP_ID'),
            "apiKey": dotenv.get('API_KEY'),
            "table": table,
            "format": "json"}
    data.update({k: v
                 for k, v
                 in {'id': id_,
                     'column': column,
                     'value': value,
                     'limit': limit}.items()
                 if v})
    return requests.post(
        'https://api.octranspo1.com/v1.2/Gtfs',
        data=data
    ).json()

# In [22]: oc.gtfs('stops', column='stop_code', value='4808')
# Out[22]:
# {'Gtfs': [{'id': '2559',
#    'location_type': '0\r',
#    'parent_station': '',
#    'stop_code': '4808',
#    'stop_desc': '',
#    'stop_id': 'NF200',
#    'stop_lat': '45.3804',
#    'stop_lon': '-75.7283',
#    'stop_name': 'HOLLINGTON / SHILLINGTON',
#    'stop_url': '',
#    'zone_id': ''}],
#  'Query': {'column': 'stop_code',
#   'direction': 'ASC',
#   'format': 'json',
#   'table': 'stops',
#   'value': '4808'}}

# In [20]: oc.gtfs('routes', column='route_short_name', value='14')
# Out[20]:
# {'Gtfs': [{'id': '8',
#    'route_desc': '',
#    'route_id': '14-277',
#    'route_long_name': '',
#    'route_short_name': '14',
#    'route_type': '3'}],
#  'Query': {'column': 'route_short_name',
#   'direction': 'ASC',
#   'format': 'json',
#   'table': 'routes',
#   'value': '14'}}

# oc.gtfs('trips', column='route_id', value='14-277')

# oc.gtfs('stop_times', column='stop_id', value='NF200')

# GTFS
# Retrieves specific records from all sections of the GTFS file.
