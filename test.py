from src.ukrposhtaApi import UkrposhtaApi
import os
from dotenv import load_dotenv
load_dotenv()
from src.transliteration import transliterate

bearer = os.getenv('sandbox_bearer')
ukrposhta = UkrposhtaApi(bearer)

def writeToFile(name_file, data_list):
    with open(name_file, "w", encoding='utf-8') as file:
        for data in data_list:
            file.write(f'{data}\n')


allRegions = ["Харківська", "Полтавська", "Донецька", "Луганська", "Запорізька", "Сумська", "Чернігівська", "Дніпропетровська", "Херсонська", "Миколаївська", "Одеська", "Черкаська", "Київська", "Житомирська", "Тернопільська", "Вінницька", "Волинська", "Чернівецька", "Львівська", "Закарпатська", "Хмельницька", "Івано-Франківська", "Рівненська"]
def writeToFileAllRegions(region_list):
    data_list = list()
    for region in region_list:
        result = ukrposhta.getRegionId(region)
        data_list.append(result['Entries']['Entry'][0])
    writeToFile('regions.txt', data_list)


# result = ukrposhta.getRegionIdByRegionName('Полтавська')
# result = ukrposhta.getDistrictsByRegionName('Харківська')
# print(result)
# writeToFile('data/districts/kharkiv_districts.txt', result)
# print(transliterate('Харківська'))

