from src.ukrposhtaApi import *
import os
from dotenv import load_dotenv
load_dotenv()
from src.transliteration import transliterate
import json

bearer = os.getenv('PRODUCTION_BEARER_eCom')
token = os.getenv('PROD_COUNTERPARTY_TOKEN')
# bearerStatusTracking = os.getenv('PRODUCTION_BEARER_StatusTracking')
# bearer = os.getenv('sandbox_bearer')
# token = os.getenv('SAND_COUNTERPARTY_TOKEN')
# bearer = os.getenv('SANDBOX_BEARER_StatusTracking')
# bearer = os.getenv('COUNTERPARTY_UUID')

# Для работы с адресами
ukrposhtaCreateAddress = UkrposhtaAddressClassifier(bearer)
# Для работы с созданием отправления
ukrposhtaCreatShipment = UkrposhtaCreateShipment(bearer)

def writeToFile(name_file, data_list):
    with open(name_file, "w", encoding='utf-8') as file:
        for data in data_list:
            file.write(f'{data}\n')

allRegions = ["Харківська", "Полтавська", "Донецька", "Луганська", "Запорізька", "Сумська", "Чернігівська", "Дніпропетровська", "Херсонська", "Миколаївська", "Одеська", "Черкаська", "Київська", "Житомирська", "Тернопільська", "Вінницька", "Волинська", "Чернівецька", "Львівська", "Закарпатська", "Хмельницька", "Івано-Франківська", "Рівненська"]


# data = {"postcode":"90000"}
# res = ukrposhtaCreatShipment.createAddressId(data=data)

# res = ukrposhtaCreatShipment.availabilityChecking(61091, 37602)
# res = ukrposhtaCreatShipment.getClient(token=token, phNumber='+380964536073')
# print(res)

res = ukrposhtaCreatShipment.phoneProhibited(token=token, phone='380636360299')
print(res)

