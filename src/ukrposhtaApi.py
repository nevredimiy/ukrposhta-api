import requests
from requests import RequestException
from datetime import datetime
import json

class UkrposhtaAddressClassifier:
    host = 'https://www.ukrposhta.ua/address-classifier-ws'
    url = None
    bearer = None

    headers = {
        'Authorization': f'Bearer {bearer}',
        'Accept': 'application/json'
    }

    def __init__(self, bearer):
        self.bearer = bearer


    def request_data(self, end_point, param=''):
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
            resp = requests.get(self.url, headers=headers)
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

    def getCitiesByRegion(self, region_name):
        regionId = self.getRegionIdByRegionName(region_name)
        endPoint = 'get_city_by_region_id_and_district_id_and_city_ua'
        param = f'region_id={regionId}'
        result = self.request_data(endPoint, param)
        res = result["Entries"]["Entry"]
        cities = []
        for city in res:
            cities.append({
                'name': city['CITY_UA'],
                'name_id': city['CITY_ID'],
                'district': city['DISTRICT_UA'],
                'district_id': city['DISTRICT_ID'],
                'region': city['REGION_UA'],
                'region_id': city['REGION_ID'],
                'city_type': city['CITYTYPE_UA'],
                })
        return cities

    def getStreetsByCity(self, city_name):
        endPointCN = 'get_city_by_region_id_and_district_id_and_city_ua'
        paramCN = f'city_ua={city_name}'
        resultCN = self.request_data(endPointCN, paramCN)
        cityId = resultCN["Entries"]["Entry"][0]["CITY_ID"]
        endPoint = 'get_street_by_region_id_and_district_id_and_city_id_and_street_ua'
        param = f'city_id={cityId}'
        result = self.request_data(endPoint, param)
        streets = result["Entries"]["Entry"]
        streetNames = []
        for street in streets:
            streetNames.append(street["STREET_UA"])
        return streetNames

    def getAddressByIndex(self, postindex):
        if not isinstance(postindex, str):
            postindex = str(postindex)
        endPoint = 'get_postoffices_by_postindex'
        param = f'pi={postindex}'
        result = self.request_data(endPoint, param)
        res = result["Entries"]["Entry"][0]
        print(f'{res['PDCITYTYPE_UA']} {res['PO_SHORT']} - {res['ADDRESS']}: {res['PHONE']}')

        return res

    def getPostofficeOpenHoursByIndex(self, postcode):
        endPoint = 'get_postoffices_openhours_by_postindex'
        if not isinstance(postcode, str):
            postcode = str(postcode)
        param = f'pc={postcode}'
        result = self.request_data(endPoint, param)
        cleanRes = result["Entries"]["Entry"]
        openHours = []
        day = datetime.now().weekday()
        dayOfWeek = day - 1
        for day in cleanRes:
            openHours.append(f'{day['DAYOFWEEK_UA']} з {day['TFROM']} до {day['TTO']}')
        return openHours[dayOfWeek]

class UkrposhtaCreateShipment:
    uri = 'https://www.ukrposhta.ua/ecom/0.0.1/'
    url = None
    bearer = None

    def __init__(self, bearer):
        self.bearer = bearer

    def prepare(self, data):
        """
        Prepare the data for the request
        :return json
        """
        return json.dumps(data, ensure_ascii=False)

    def request_data(self, end_point: str, data='', method='post'):
        """
        Send request
        :return json
        """
        if not isinstance(end_point, str):
            end_point = str(end_point)

        self.url = self.uri + end_point
        print(self.url)
        headers = {
            "Content-Type": "application/json",
            "authorization": "Bearer " + self.bearer
        }
        resp = None
        try:
            if method == 'post':
                resp = requests.post(self.url, headers=headers, data=self.prepare(data))
                print(resp.status_code)
            elif method == 'get':
                resp = requests.get(self.url, headers=headers)
                print(resp.status_code)
            elif type == 'put':
                resp = requests.put(self.uri, data=self.prepare(data), headers=headers)
        except RequestException as msg:
            return msg
        return resp.json()

    #Створення адреси
    def createAddressId(self, data):
        resp = self.request_data(end_point='addresses', data=data)
        return resp["id"]

    #Перевірка доступності маршруту доставки між індексами
    def availabilityChecking(self, senderPostcode, recipientPostcode ):
        if not isinstance(senderPostcode, str):
            senderPostcode = str(senderPostcode)
        if not isinstance(recipientPostcode, str):
            recipientPostcode = str(recipientPostcode)

        resp = self.request_data(end_point=f'addresses/availability-checking/from/{senderPostcode}/to/{recipientPostcode}', method='get')
        return resp

    def createClient(self, token: str, dataClient: dict):
        data = {
                "type":"INDIVIDUAL",
                "name": dataClient['name'],
                "firstName": dataClient['firstName'],
                "lastName": dataClient['lastName'],
                "middleName": dataClient['middleName'],
                "addressId":dataClient["addressId"],
                "phoneNumber": dataClient["phoneNumber"]
            }
        resp = self.request_data(end_point=f'clients?token={token}', data=data)
        return resp

    def getClient(self, token: str, phNumber:str):
        resp = self.request_data(end_point=f'clients/phone?token={token}&countryISO3166=UA&phoneNumber={phNumber}', method='get')
        print(resp)
        return resp

    #Перевірка коректності введення номеру телефону
    def phoneProhibited(self, token, phone: str):
        resp = self.request_data(end_point=f'phones/UA/prohibited/{phone}?token={token}', method='get')
        return resp

    #створення відправлення
    def shipments(self, token, data):
        resp = self.request_data(end_point=f'shipments?token={token}', data=data)
        print(resp)
        return resp
