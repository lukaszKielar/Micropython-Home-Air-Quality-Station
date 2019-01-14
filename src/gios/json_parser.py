import os
import requests
import json

ALL_STATIONS = "http://api.gios.gov.pl/pjp-api/rest/station/findAll"
STATION_SENSORS = "http://api.gios.gov.pl/pjp-api/rest/station/sensors/{station_id}"
SENSOR_ID = "http://api.gios.gov.pl/pjp-api/rest/data/getData/{sensor_id}"
STATION_API = "http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{station_id}"


class GiosAPI:

    def stations(self):
        try:
            response = requests.get(ALL_STATIONS)
            if response.status_code != 200:
                raise NotImplementedError("Cannot get stations from API. Status code {}".format(response.status_code))
            else:
                return json.loads(response.text)
        except Exception as e:
            print(e)
            print("No Internet connection")

    def save_json(self, output_path):
        try:
            with open(output_path, 'w') as output_file:
                json.dump(self.stations(), output_file, ensure_ascii=False)
            print("File had been saved")
        except FileNotFoundError:
            print("Wrong path")

    @property
    def _stations_ids(self):
        return [station['id'] for station in self.stations()]

    def get_station_details(self, station_id):
        if station_id not in self._stations_ids:
            raise NotImplementedError("Station doesn't exist")
        else:
            station_dict = next((station for station in self.stations() if station['id'] == station_id), None)
            return json.dumps(station_dict)


class Station(GiosAPI):

    def __init__(self, station_id):
        self.__dict__ = json.loads(self.get_station_details(station_id=station_id))

    @property
    def sensors(self):
        try:
            response = requests.get(STATION_SENSORS.format(station_id=self.id))
            if response.status_code != 200:
                raise NotImplementedError("Cannot get station sensors from API. Status code {}".format(response.status_code))
            else:
                return json.loads(response.text)
        except Exception as e:
            print(e)
            print("No Internet connection")