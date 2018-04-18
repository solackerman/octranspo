import datetime as dt
from octranspo import bigquery as bq
from octranspo import oc_api


class NextTrips(bq.Table):
    dataset_id = 'octranspo'
    table_id = 'next_trips'
    schema = {'AdjustedScheduleTime':  ['TIME', {'mode': 'REQUIRED',
                                                 'description': 'Time until bus arrives',
                                                 'fields': ()}],
              'AdjustmentAge':         ['TIME', {'mode': 'REQUIRED',
                                                 'description': 'Time since last GPS reading'}],
              'BusType':               ['STRING', {}],
              'Direction':             ['STRING', {}],
              'GPSSpeed':              ['FLOAT64', {}],
              'LastTripOfSchedule':    ['BOOL', {}],
              'Latitude':              ['FLOAT64', {}],
              'Longitude':             ['FLOAT64', {}],
              'RequestProcessingTime': ['DATETIME', {'mode': 'REQUIRED'}],
              'RouteLabel':            ['STRING', {'mode': 'REQUIRED'}],
              'RouteNo':               ['STRING', {'mode': 'REQUIRED'}],
              'StopLabel':             ['STRING', {'mode': 'REQUIRED'}],
              'StopNo':                ['STRING', {'mode': 'REQUIRED'}],
              'TripDestination':       ['STRING', {'mode': 'REQUIRED'}],
              'TripStartTime':         ['TIME', {'mode': 'REQUIRED'}]}

    @staticmethod
    def to_time(t):
        t_tup = list(map(int, t.split(':')))
        t_tup[0] %= 24
        return dt.time(*t_tup)


    @staticmethod
    def gen_row(stop_no, route_no):
        response = oc_api.next_trips_for_stop(stop_no, route_no)
        next_trips = response['GetNextTripsForStopResult']
        route = next_trips['Route']['RouteDirection']


        trips = route['Trips']
        if not trips:
            return

        trip = trips['Trip']
        if isinstance(trip, list):
            trip = trip[0]

        adjustment_age = dt.timedelta(seconds=int(float(trip['AdjustmentAge']) * 60))
        if adjustment_age < dt.timedelta(0):
            return

        return (
            (dt.datetime.min + dt.timedelta(minutes=float(trip['AdjustedScheduleTime']))).time(),
            (dt.datetime.min + adjustment_age).time(),
            trip['BusType'],
            route['Direction'],
            float(trip['GPSSpeed']),
            trip['LastTripOfSchedule'],
            float(trip['Latitude']),
            float(trip['Longitude']),
            dt.datetime.strptime(route['RequestProcessingTime'], '%Y%m%d%H%M%S'),
            route['RouteLabel'],
            str(route['RouteNo']),
            next_trips['StopLabel'],
            next_trips['StopNo'],
            trip['TripDestination'],
            NextTrips.to_time(trip['TripStartTime'])
        )

    def run(self, stops):
        rows = []
        for stop_no, route_no in stops:
            row = self.gen_row(stop_no, route_no)
            if row:
                rows.append(row)
        self.insert_rows(rows)
