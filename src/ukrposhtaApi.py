import requests
from requests import RequestException

class UkrposhtaApi:
    host = 'https://www.ukrposhta.ua/address-classifier-ws'
    url = None
    bearer = None

    headers = {
        'Authorization': f'Bearer {bearer}',
        'Accept': 'application/json'
    }

    def __init__(self, bearer):
        self.bearer = bearer


    def request_data(self, end_point, param='', data='', method='get'):
        """
        Send request
        :return json
        """
        if not isinstance(param, str):
            param = str(param)

        self.url = f'{self.host}/{end_point}?{param}'
        headers = {
                'authorization': 'Bearer ' + self.bearer,
                'Accept': 'application/json'
            }
        resp = None

        try:
            if method == 'post':
                resp = requests.post(self.url, self.prepare(data), headers=headers)
            elif method == 'get':
                resp = requests.get(self.url, headers=headers)
            elif type == 'put':
                resp = requests.put(self.url, data=self.prepare(data), headers=headers)
        except RequestException as msg:
            return msg
        return resp.json()

    def getRegionIdByRegionName(self,region_name):
        endPoint = 'get_regions_by_region_ua'
        param = f'region_name={region_name}'
        result = self.request_data(endPoint, param)
        return result['Entries']['Entry'][0]['REGION_ID']

    def getDistrictsByRegionName(self, region_name):
        id = self.getRegionIdByRegionName(region_name)
        endPoint = 'get_districts_by_region_id_and_district_ua'
        param = f'region_id={id}'
        result = self.request_data(endPoint, param)
        data = result["Entries"]["Entry"]
        districtsList = []
        for d in data:
            districtsList.append({
                "name":d["DISTRICT_UA"],
                "district_id":d["DISTRICT_ID"]
                })

        return districtsList
