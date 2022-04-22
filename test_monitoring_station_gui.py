import pytest
from mhrpatient_info import Patient
from pymodm import connect
from pymongo import MongoClient
import requests
import json

server = "http://127.0.0.1:5000"

connect("mongodb+srv://LijoShua:cvK3Z53NofAz1jPl@bme547.iiecj."
        "mongodb.net/finalprojDatabase?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True)
# @Ben comment out the first connect and uncomment the second connect
# if the first connect isn't working
# connect("mongodb+srv://bme547classwork:Percussionist20"
#         "@bme547.1e368.mongodb.net/finalprojDatabase?"
#         "retry"
#         "Writes=true&w=majority",
#         tls=True, tlsAllowInvalidCertificates=True)

mongo_client = MongoClient("mongodb+srv://LijoShua:cvK3Z53NofAz1jPl"
                           "@bme547.iiecj.mongodb.net/finalproj"
                           "Database?retryWrites=true&w=majority",
                           tls=True, tlsAllowInvalidCertificates=True)

# mongo_client = MongoClient("mongodb+srv://bme547classwork:Percussionist20"
#                            "@bme547.1e368.mongodb.net/finalprojDatabase?"
#                            "retry"
#                            "Writes=true&w=majority",
#                            tls=True, tlsAllowInvalidCertificates=True)


b64string_test = ("/9j/4AAQSkZJRgABAQEAlgCWAAD/2wBDAAMCAgM"
                  "CAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCw"
                  "sNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUF"
                  "RT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQU"
                  "FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQ"
                  "UFBQUFBQUFBQUFBT/wAARCAAuACsDASIAAhEBAx"
                  "EB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFB"
                  "gcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQID"
                  "AAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fA"
                  "kM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRk"
                  "dISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDh"
                  "IWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2"
                  "t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5uf"
                  "o6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQ"
                  "AAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDB"
                  "AcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEI"
                  "FEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJyg"
                  "pKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2"
                  "hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmao"
                  "qOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU"
                  "1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAM"
                  "BAAIRAxEAPwDj6KKK/oM/LwooooAKKKKACiiigA"
                  "ooooAKKKKACiiigAooooAKKKKAP//Z")


def test_process_mhrnumbers_good():
    from monitoring_station_gui import process_mhrnumbers
    json_list = '[846138,846137]\n'
    answer = process_mhrnumbers(json_list)
    expected = [846137, 846138]
    assert all(item in answer for item in expected)


def test_process_mhrnumbers_bad():
    from monitoring_station_gui import process_mhrnumbers
    json_list = '[]'
    answer = process_mhrnumbers(json_list)
    expected = ["No patients in DB yet!"]
    assert answer == expected


def test_jsonified_dict_parser():
    from monitoring_station_gui import jsonified_dict_parser
    jsonified_dict = ('{"name":"Li.Joshua",'
                      '"last_hr":89,'
                      '"latest_ecg":"hello",'
                      '"latest_ecg_tstamp":"2022-4-10 2:04:33"}\n')
    answer = jsonified_dict_parser(jsonified_dict)
    expected = {"name": "Li.Joshua",
                "last_hr": 89,
                "latest_ecg": "hello",
                "latest_ecg_tstamp": "2022-4-10 2:04:33"}
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_b64_string_to_file():
    from monitoring_station_gui import convert_b64_to_image
    from patient_side_gui import convert_file_to_b64_string
    import filecmp
    import os
    b64str = convert_file_to_b64_string("test_image1.jpg")
    convert_b64_to_image(b64str, "temp.jpg")
    answer = filecmp.cmp("test_image1.jpg",
                         "temp.jpg")
    os.remove("temp.jpg")
    assert answer is True


def test_process_tstmp():
    from monitoring_station_gui import process_tstmp
    json_list = ('["2022-4-10 2:04:33","2022-4-10 2:04:33",'
                 '"2022-4-10 2:04:33","2022-4-10 2:04:33"]\n')
    answer = process_tstmp(json_list)
    expected = ['2022-4-10 2:04:33', '2022-4-10 2:04:33',
                '2022-4-10 2:04:33', '2022-4-10 2:04:33']
    assert answer == expected
