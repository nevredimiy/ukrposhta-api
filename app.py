import requests
import os
from dotenv import load_dotenv
import gspread
import pandas as pd
load_dotenv()


bearer = os.getenv('sandbox_bearer')
host = 'https://www.ukrposhta.ua/address-classifier-ws'
headers = {
        'Authorization': f'Bearer {bearer}',
        'Accept': 'application/json'
    }
#region_name - писать на украинском языке, например 'Харківська'
def writeToFile(name_file, data_list):
    with open(name_file, "w", encoding='utf-8') as file:
        for data in data_list:
            file.write(f'{data}\n')

def getRegionId(region_name):
    url = f'{host}/get_regions_by_region_ua?region_name={region_name}'
    res = requests.get(url, headers=headers)
    # print(res.json())
    #RESPONSE
    #{'Entries': {'Entry': [{'REGION_ID': '280', 'REGION_UA': 'Харківська', 'REGION_EN': 'Kharkivska', 'REGION_KATOTTG': '63000000000041885', 'REGION_KOATUU': '6300000000', 'REGION_RU': None}]}}
    r = res.json()
    region = r["Entries"]["Entry"][0] #словарь(dict) - возвращается лист, но он всегда один.
    return region['REGION_ID']

def get_districts(region_name):
    id = getRegionId(region_name)
    url = f'{host}/get_districts_by_region_id_and_district_ua?region_id={id}'
    res = requests.get(url, headers=headers)
    r = res.json()
    data = r["Entries"]["Entry"]
    writeToFile('districts.txt', data)
    # print(data)
    districtIdList = []
    for d in data:
        districtIdList.append({
            "name":d["DISTRICT_UA"],
            "district_id":d["DISTRICT_ID"]
            })

    return districtIdList

def get_city(districtId):
    url = f'{host}/get_city_by_region_id_and_district_id_and_city_ua?district_id={districtId}'
    res = requests.get(url, headers=headers)
    r = res.json()
    data = r["Entries"]["Entry"]
    writeToFile('cities_KH_districts.txt', data)
    cities = []
    for d in data:
        cities.append({
                'name':d['CITY_UA'],
                'city_id': d['CITY_ID'],
                'district': d['DISTRICT_UA'],
                'region': d['REGION_UA'],
                'cityType': d['CITYTYPE_UA']
            })
    return cities

def get_street_by_city_id(cityId):
    url = f'{host}/get_street_by_region_id_and_district_id_and_city_id_and_street_ua?city_id={cityId}'
    res = requests.get(url, headers=headers)
    r = res.json()
    data = r["Entries"]["Entry"]
    streets = []
    for street in data:
        streets.append({
                'id': street['STREET_ID'],
                'streetType': street['STREETTYPE_UA'],
                'name': street['STREET_UA'],
            })
    return streets

def get_addr_house_by_street_id(streetId):
    url = f'{host}/get_addr_house_by_street_id?street_id={streetId}'
    res = requests.get(url, headers=headers)
    r = res.json()
    data = r["Entries"]["Entry"]
    return data

def get_courierarea_by_postindex(postindex):
    url = f'{host}/get_courierarea_by_postindex?postindex={postindex}'
    res = requests.get(url, headers=headers)
    r = res.json()
    data = r["Entries"]["Entry"][0]
    if data['IS_COURIERAREA'] == '0':
        message = 'Курьерской доставки нет'
    else:
        message = 'Возможна курьерская доставка'
    return message

def get_postoffices_by_postindex(postindex):
    url = f'{host}/get_postoffices_by_postindex?pi={postindex}'
    res = requests.get(url, headers=headers)
    r = res.json()
    data = r["Entries"]["Entry"]
    return data

def get_postoffices_openhours_by_postindex(postcode):
    url = f'{host}/get_postoffices_openhours_by_postindex?pc={postcode}'
    res = requests.get(url, headers=headers)
    r = res.json()
    data = r["Entries"]["Entry"]
    mode = []
    for d in data:
        mode.append({
                'day': d["DAYOFWEEK_UA"],
                'hour': f'{d["TFROM"]} - {d["TTO"]}'
            })
    d = pd.DataFrame(mode)
    print(d)

def get_postoffices_by_geolocation(latitude, longitude, maxDistance):
    url = f'{host}/get_postoffices_by_geolocation?lat={latitude}&long={longitude}&maxdistance={maxDistance}'
    res = requests.get(url, headers=headers)
    print(res.status_code)
    r = res.json()
    data = r["Entries"]["Entry"]
    for d in data:
        print(d['ADDRESS'], d['POSTINDEX'], d['DISTANCE'])

    print(len(data))

def get_postoffices_by_city_id(region_id):
    url = f'{host}/get_postoffices_by_city_id?region_id={region_id}'
    res = requests.get(url, headers=headers)
    print(res.status_code)
    r = res.json()
    data = r["Entries"]["Entry"]
    return data

def main(region_name):
    districtId = ''
    districts = get_districts(region_name)

    for district in districts:
        if(district['name']=='Миргородський'):
            districtId = district['district_id']

    if districtId != '':
        cities = get_city(districtId)
        for city in cities:
            if city['name'] == 'Миргород':
                street = get_street_by_city_id(city['city_id'])
                print(street)
    else:
        print('Nothin print')

allRegions = ["Харківська", "Полтавська", "Донецька", "Луганська", "Запорізька", "Сумська", "Чернігівська", "Дніпропетровська", "Херсонська", "Миколаївська", "Одеська", "Черкаська", "Київська", "Житомирська", "Тернопільська", "Вінницька", "Волинська", "Чернівецька", "Львівська", "Закарпатська"]
region_name = 'Харківська'

if __name__ == '__main__':
    print(getRegionId(region_name))
    # res = get_street_by_city_id('18550')
    # r = pd.DataFrame(res)
    # print(r)
    # get_postoffices_openhours_by_postindex('61091')
    # get_postoffices_by_geolocation('49.958343', '36.332375', '1')
    # region_id = getRegion(region_name)
    # res = get_postoffices_by_city_id(region_id)
    # print(res[0])
    # print(len(res))
    # get_districts(region_name)
    # get_city('390')

