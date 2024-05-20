import os, time
from src.ukrposhtaApi import *

bearer = os.getenv('sandbox_bearer')
token = os.getenv('SAND_COUNTERPARTY_TOKEN')
ukrposhta = UkrposhtaCreateShipment(bearer)
ukrposhtaAddress = UkrposhtaAddressClassifier(bearer)

def createShipment():
    postcodeSender = input("Введіть індекс відправника:")
    postcodeRecipient = input("Введіть індекс отримувача:")
    resp = ukrposhta.availabilityChecking(senderPostcode=postcodeSender, recipientPostcode=postcodeRecipient)
    if resp['code'] == 'SUCCESS':
        print(resp['description'])
        time.sleep(2)
    else:
        print(resp['description'])
        time.sleep(2)
        return
    print('--- Дані відправника ---')
    firstNameSender = input("Введіть ім\'я відправника:")
    lastNameSender = input("Введіть прізвище відправника:")
    middleNameSender = input("Введіть ім\'я по-батькові:")
    phoneNumberSender = input("Введіть номер телефона відправника у форматі +380111111111:")
    print('--- Дані отримувача ---')
    firstNameRecipient = input("Введіть ім\'я відправника:")
    lastNameRecipient = input("Введіть прізвище відправника:")
    middleNameRecipient = input("Введіть ім\'я по-батькові:")
    phoneNumberRecipient = input("Введіть номер телефона відправника у форматі +380111111111:")
    postcodeSender = { "postcode": postcodeSender }
    postcodeRecipient = { "postcode": postcodeRecipient }
    addressIdSender = ukrposhta.createAddressId(postcodeSender)
    addressIdRecipient = ukrposhta.createAddressId(postcodeRecipient)
    sender = {
            "name": firstNameSender + middleNameSender + lastNameSender,
            "firstName": firstNameSender,
            "lastName": lastNameSender,
            "middleName": middleNameSender,
            "addressId": addressIdSender,
            "phoneNumber": phoneNumberSender
        }
    recipient = {
            "name": firstNameRecipient + middleNameRecipient + lastNameRecipient,
            "firstName": firstNameRecipient,
            "lastName": lastNameRecipient,
            "middleName": middleNameRecipient,
            "addressId": addressIdRecipient,
            "phoneNumber": phoneNumberRecipient
        }
    send = ukrposhta.createClient(token=token, dataClient=sender)
    reciv = ukrposhta.createClient(token=token, dataClient=recipient)
    print(send["uuid"])
    print(reciv["uuid"])
    dataShipments = {
        "sender":{
            "uuid":send["uuid"]
        },
        "recipient":{
            "uuid":reciv["uuid"]
        },
        "deliveryType":"W2W",
        "paidByRecipient": True,
        "parcels":[
            {
            "weight":30,
            "length":20
            }
        ]
    }
    ukrposhta.shipments(token=token, data=dataShipments)

def lastVerdionDoc():
    data = {
        "postcode":"61091",
    }
    # resp = ukrposhta.request_data(end_point='addresses', data=data, method='post')
    resp = ukrposhta.createAddressId(data)
    print(resp)

def getPostOfficeByPostindex():
    postindex = input('Введіть номер індекса:')
    ukrposhtaAddress.getAddressByIndex(postindex)

def main():
    inp = input("Знайти відділення(ЗВ) чи створити відправлення(СВ): ")
    if inp == 'ЗВ':
        getPostOfficeByPostindex()
    elif inp == 'СВ':
        createShipment()
    else:
        print('Ви повинні ввести \'ЗВ\' або \'СВ\': ')
        main()
if __name__ == '__main__':
    main()