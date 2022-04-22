import pytest
from mhrpatient_info import Patient
from pymodm import connect
from pymongo import MongoClient
from pymodm import errors as pymodm_errors
from patient_monitoring_sys_server import patient_dataupload_driver
from monitoring_station_gui import jsonified_dict_parser
from flask import Flask, request, jsonify

import requests
import json

server = "http://127.0.0.1:5000"

connect("mongodb+srv://LijoShua:cvK3Z53NofAz1jPl@bme547.iiecj."
        "mongodb.net/finalprojDatabase?retryWrites=true&w=majority",
        tls=True, tlsAllowInvalidCertificates=True)

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

test_patient = Patient(mhrnumber=846137,
                       name="Li.Joshua",
                       medimgs={"e": "e"},
                       ecgimgs={"e": "e"},
                       hrlist=["e"],
                       ecgimgtstamps=["e"],
                       medimgtstamps=["e"])
saved_patient = test_patient.save()

in_data = {"mhrnumber": 846137, "name": "Farmer.Paul",
           "medimgbytes": b64string_test}

answer = patient_dataupload_driver(in_data)

in_data = {"mhrnumber": 846138, "name": "Farmer.Paul",
           "ecgimgbytes": b64string_test, "hr": 89}

answer = patient_dataupload_driver(in_data)

in_data = {"mhrnumber": 846140, "name": "Ward.David",
           "ecgimgbytes": b64string_test, "hr": 89}
answer = patient_dataupload_driver(in_data)

in_data = {"mhrnumber": 846139, "medimgbytes": b64string_test}
answer = patient_dataupload_driver(in_data)

# r = requests.get(server + "/get_ids")
# list_json = r.text
# print(list_json)
# list_json_nobracks = list_json[1:-2]
# list_separated = list_json_nobracks.split(",")
# print(list_separated)
# print(list_separated[0])
# list_int = [int(i) for i in list_separated]
# print(list_int)
# print(type(list_int))

patient_id = 846137
# r = requests.get(server + "/get_patient_info/{}".format(patient_id))
# output = r.text
# print(output)

# try:
#     patient = Patient.objects.raw({"_id": patient_id}).first()
# except pymodm_errors.DoesNotExist:
#     print("Patient_id {} was not found".format(patient_id)), 400
# ecgimg_keys = list(patient.ecgimgs.keys())
# print(ecgimg_keys)
# latest_file = "e"
# for i in range(1, len(ecgimg_keys)):
#     print(ecgimg_keys[i])
#     if ecgimg_keys[i] > latest_file:
#         latest_file = ecgimg_keys[i]
# print(latest_file)
# info_json = {"name": patient.name, "last_hr": patient.hrlist[-1],
#              "latest_ecg": patient.ecgimgs[latest_file],
#              "latest_ecg_tstamp": patient.ecgimgtstamps[-1]}
# print(info_json)

output = ('{"name":"Li.Joshua",'
          '"last_hr":89,'
          '"latest_ecg":"e",'
          '"latest_ecg_tstamp":"2022-4-10 2:04:33"}\n')
print(type(output))
output_nobrackets = output[1:-2]
output_parsed = output_nobrackets.split(",")
print(output_parsed)
dict_fixed = {}
list_dict = output_parsed
for entry in list_dict:
    print(entry)
    entry_split = entry.split(":", 1)

    key = (entry_split[0])[1:-1]
    print(key)
    try:
        value = int(entry_split[1])
    except Exception:
        value = (entry_split[1])[1:-1]
    print(value)
    dict_fixed[key] = value
print(dict_fixed)
dict_done = jsonified_dict_parser(output)
print(dict_done)

# try:
#     patient = Patient.objects.raw({"_id": 846138}).first()
# except pymodm_errors.DoesNotExist:
#     print("Patient_id {} was not found".format(patient_id))
# ecgimg_keys = list(patient.ecgimgs.keys())
# latest_file = ""
# for i in range(0, len(ecgimg_keys)-1):
#     if ecgimg_keys[i] < ecgimg_keys[i+1]:
#         latest_file = ecgimg_keys[i+1]
# print(latest_file)
# print(patient.ecgimgs[latest_file])

patient_id = 846138
r = requests.get(server + "/get_ecg_times/{}".format(patient_id))
json_list = r.text
print(json_list)
tstmp_json_nobrackets = json_list[1:-2]
tstmp_separated = tstmp_json_nobrackets.split(",")
if len(tstmp_separated) == 1:
    print("No images uploaded yet!")
tstmp_list = [i[1:-1] for i in tstmp_separated]
print(tstmp_list[1:len(tstmp_separated)])

patient_id = 846138
tstmpindex = 2
r = requests.get(server + "/get_ecg_"
                          "img/{}/{}".format(patient_id,
                                             tstmpindex))
bytes = r.text
print(bytes)
bytestrim = bytes[1:-2]
print(bytestrim)
