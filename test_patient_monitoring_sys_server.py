import pytest
from mhrpatient_info import Patient
from pymodm import connect
from pymongo import MongoClient

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

pytest_vars = "mhrno, patname, medimgbytes, ecgimgbytes, hr, expected"


@pytest.mark.parametrize(pytest_vars, [
    [937891, "", "", "", "",
        (("Created new patient for mhrnumber 937891."
          " No new data added to this patient"), 200)],
    [937892, "", "", "blah", 56,
        (("Created new patient for mhrnumber 937892."
          " Added provided ecgimg, hr, and current"
          " time and date. Stored image as ekgimg1"), 200)],
    [937893, "", "blah", "", "",
        (("Created new patient for mhrnumber 937893."
          " Added provided medimg and stored as"
          " medimg1."), 200)],
    [937894, "Farmer.Paul", "", "", "",
        (("Created new patient for mhrnumber 937894."
          " Added name Farmer.Paul to record."), 200)],
    [937895, "", "blah", "blah", 56,
        (("Created new patient for mhrnumber 937895."
          " Added provided ecgimg, hr, and current"
          " time and date. Stored ecgimage as ekgimg1"
          " Added provided medimg stored as medimg1"), 200)],
    [937896, "Farmer.Paul", "", "blah", 56,
        (("Created new patient for mhrnumber 937896."
          " Added name Farmer.Paul to record."
          " Added provided ecgimg, hr, and current"
          " time and date. Stored image as ekgimg1"), 200)],
    [937897, "Farmer.Paul", "blah", "", "",
        (("Created new patient for mhrnumber 937897."
          " Added name Farmer.Paul to record."
          " Added provided medimg and stored as"
          " medimg1."), 200)],
    [937898, "Farmer.Paul", "blah", "blah", 56,
        (("Created new patient for mhrnumber 937898."
          " Added name Farmer.Paul to record."
          " Added provided ecgimg, hr, and current"
          " time and date. Stored ecgimage as ekgimg1"
          " Added provided medimg stored as medimg1"), 200)],
    [846137, "", "", "", "",
        (("No new data added to patient 846137"), 200)],
    [846137, "", "", "blah", 56,
        (("Added provided ecgimg, hr, and current"
          " time and date for patient 846137. Stored"
          " image as ekgimg1"), 200)],
    [846137, "", "blah", "", "",
        (("Added provided medimg for patient 846137. Stored"
          " image as medimg2"), 200)],
    [846137, "Farmer.Paul", "", "", "",
        (("Added name Farmer.Paul for patient 846137."), 200)],
    [846137, "", "blah", "blah", 56,
        (("Added provided ecgimg, hr, and current"
          " time and date for patient 846137. Stored"
          " ecgimage as ekgimg1."
          " Stored medimage as medimg2"), 200)],
    [846137, "Farmer.Paul", "", "blah", 56,
        (("Added name Farmer.Paul for patient 846137."
          " Added provided ecgimg, hr, and current"
          " time and date. Stored image as ekgimg1"), 200)],
    [846137, "Farmer.Paul", "blah", "", "",
        (("Added name Farmer.Paul for patient 846137."
          "Added provided medimg. Stored"
          " image as medimg2"), 200)],
    [846137, "Farmer.Paul", "blah", "blah", 56,
        (("Added name Farmer.Paul for patient 846137."
          " Added provided ecgimg, hr, and current"
          " time and date. Stored"
          " ecgimage as ekgimg1. Stored"
          " medimage as medimg2"), 200)]
    ])
def test_perform_dataupload(mhrno, patname, medimgbytes,
                            ecgimgbytes, hr, expected):
    from patient_monitoring_sys_server import perform_dataupload
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": "somethinghex"},
                           ecgimgs={"e": "e"},
                           hrlist=["e"],
                           ecgimgtstamps=["2022-4-10 2:04:33"])
    saved_patient = test_patient.save()
    answer = perform_dataupload(mhrno, patname, medimgbytes,
                                ecgimgbytes, hr)
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


@pytest.mark.parametrize("in_data, expected", [
    ["hello", ("The input was not a dictionary.", 400)],
    [{"name": "Li.Joshua"}, (("Attempted data upload does not contain"
                              " the mandatory"
                              " mhrnumber key"), 400)],
    [{"mhrnumber": 846137, "bloodpressure": "120/80"},
     ("The provided key bloodpressure is not an accepted key.", 400)],
    [{"mhrnumber": "935.2"}, ("mhrnumber was not an integer", 400)],
    [{"mhrnumber": 846137, "ecgimgbytes": b64string_test, "hr": "87.2"},
     ("hr was not an integer", 400)],
    [{"mhrnumber": 846137, "ecgimgbytes": "hallo", "hr": 87},
     (("The provided image string is not in"
       " base64 and cannot be converted to"
       " an image file"), 400)],
    [{"mhrnumber": 846137, "ecgimgbytes": b64string_test},
     (("Did not provide a heart rate along with the"
       " uploaded image data"), 400)],
    [{"mhrnumber": 846137, "hr": 90},
     (("Did not provide an uploaded image data file"
       " along with the provided heart rate"), 400)],
    [{"mhrnumber": 846137}, (True, 203)],
    [{"mhrnumber": 846137, "medimgbytes": b64string_test},
     (True, 201)],
    [{"mhrnumber": 846137, "name": "Li.Joshua"},
     (True, 207)],
    [{"mhrnumber": 846137, "ecgimgbytes": b64string_test, "hr": 87},
     (True, 202)],
    [{"mhrnumber": 846137, "name": "Li.Joshua",
      "medimgbytes": b64string_test}, (True, 205)],
    [{"mhrnumber": 846137, "name": "Li.Joshua",
      "ecgimgbytes": b64string_test, "hr": 87}, (True, 206)],
    [{"mhrnumber": 846137, "medimgbytes": b64string_test,
      "ecgimgbytes": b64string_test, "hr": 87}, (True, 200)],
    [{"mhrnumber": 846137, "name": "Li.Joshua",
      "medimgbytes": b64string_test, "ecgimgbytes": b64string_test,
      "name": "Li.Joshua", "hr": 78}, (True, 204)]
    ])
def test_validate_dataupload_driver(in_data, expected):
    from patient_monitoring_sys_server import validate_dataupload_driver
    answer = validate_dataupload_driver(in_data)
    assert answer == expected


@pytest.mark.parametrize("in_data, expected", [
    ["hello", ("The input was not a dictionary.", 400)],
    [{"name": "Li.Joshua"}, (("Attempted data upload does not contain"
                              " the mandatory"
                              " mhrnumber key"), 400)],
    [{"mhrnumber": 846137, "bloodpressure": "120/80"},
     ("The provided key bloodpressure is not an accepted key.", 400)],
    [{"mhrnumber": "935.2"}, ("mhrnumber was not an integer", 400)],
    [{"mhrnumber": 846137, "ecgimgbytes": b64string_test, "hr": "87.2"},
     ("hr was not an integer", 400)],
    [{"mhrnumber": 846137, "ecgimgbytes": "hallo", "hr": 87},
     (("The provided image string is not in"
       " base64 and cannot be converted to"
       " an image file"), 400)],
    [{"mhrnumber": 846137, "ecgimgbytes": b64string_test},
     (("Did not provide a heart rate along with the"
       " uploaded image data"), 400)],
    [{"mhrnumber": 846137, "hr": 90},
     (("Did not provide an uploaded image data file"
       " along with the provided heart rate"), 400)],
    [{"mhrnumber": 937891},
        (("Created new patient for mhrnumber 937891."
          " No new data added to this patient"), 200)],
    [{"mhrnumber": 937892, "ecgimgbytes": b64string_test, "hr": 89},
        (("Created new patient for mhrnumber 937892."
          " Added provided ecgimg, hr, and current"
          " time and date. Stored image as ekgimg1"), 200)],
    [{"mhrnumber": 937893, "medimgbytes": b64string_test},
        (("Created new patient for mhrnumber 937893."
          " Added provided medimg and stored as"
          " medimg1."), 200)],
    [{"mhrnumber": 937894, "name": "Farmer.Paul"},
        (("Created new patient for mhrnumber 937894."
          " Added name Farmer.Paul to record."), 200)],
    [{"mhrnumber": 937895, "medimgbytes": b64string_test,
      "ecgimgbytes": b64string_test, "hr": 89},
        (("Created new patient for mhrnumber 937895."
          " Added provided ecgimg, hr, and current"
          " time and date. Stored ecgimage as ekgimg1"
          " Added provided medimg stored as medimg1"), 200)],
    [{"mhrnumber": 937896, "name": "Farmer.Paul",
      "ecgimgbytes": b64string_test, "hr": 89},
        (("Created new patient for mhrnumber 937896."
          " Added name Farmer.Paul to record."
          " Added provided ecgimg, hr, and current"
          " time and date. Stored image as ekgimg1"), 200)],
    [{"mhrnumber": 937897, "name": "Farmer.Paul",
      "medimgbytes": b64string_test},
        (("Created new patient for mhrnumber 937897."
          " Added name Farmer.Paul to record."
          " Added provided medimg and stored as"
          " medimg1."), 200)],
    [{"mhrnumber": 937898, "name": "Farmer.Paul",
      "medimgbytes": b64string_test, "ecgimgbytes": b64string_test,
      "hr": 89},
        (("Created new patient for mhrnumber 937898."
          " Added name Farmer.Paul to record."
          " Added provided ecgimg, hr, and current"
          " time and date. Stored ecgimage as ekgimg1"
          " Added provided medimg stored as medimg1"), 200)],
    [{"mhrnumber": 846137},
        (("No new data added to patient 846137"), 200)],
    [{"mhrnumber": 846137, "ecgimgbytes": b64string_test, "hr": 89},
        (("Added provided ecgimg, hr, and current"
          " time and date for patient 846137. Stored"
          " image as ekgimg1"), 200)],
    [{"mhrnumber": 846137, "medimgbytes": b64string_test},
        (("Added provided medimg for patient 846137. Stored"
          " image as medimg2"), 200)],
    [{"mhrnumber": 846137, "name": "Farmer.Paul"},
        (("Added name Farmer.Paul for patient 846137."), 200)],
    [{"mhrnumber": 846137, "medimgbytes": b64string_test,
      "ecgimgbytes": b64string_test, "hr": 89},
        (("Added provided ecgimg, hr, and current"
          " time and date for patient 846137. Stored"
          " ecgimage as ekgimg1."
          " Stored medimage as medimg2"), 200)],
    [{"mhrnumber": 846137, "name": "Farmer.Paul",
      "ecgimgbytes": b64string_test, "hr": 89},
        (("Added name Farmer.Paul for patient 846137."
          " Added provided ecgimg, hr, and current"
          " time and date. Stored image as ekgimg1"), 200)],
    [{"mhrnumber": 846137, "name": "Farmer.Paul",
      "medimgbytes": b64string_test},
        (("Added name Farmer.Paul for patient 846137."
          "Added provided medimg. Stored"
          " image as medimg2"), 200)],
    [{"mhrnumber": 846137, "name": "Farmer.Paul",
      "medimgbytes": b64string_test, "ecgimgbytes": b64string_test,
      "hr": 89},
        (("Added name Farmer.Paul for patient 846137."
          " Added provided ecgimg, hr, and current"
          " time and date. Stored"
          " ecgimage as ekgimg1. Stored"
          " medimage as medimg2"), 200)]
    ])
def test_patient_dataupload_driver(in_data, expected):
    from patient_monitoring_sys_server import patient_dataupload_driver
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": "somethinghex"},
                           ecgimgs={"e": "e"},
                           hrlist=["e"],
                           ecgimgtstamps=["2022-4-10 2:04:33"])
    saved_patient = test_patient.save()
    answer = patient_dataupload_driver(in_data)
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_ids():
    from patient_monitoring_sys_server import get_patient_ids
    from patient_monitoring_sys_server import perform_dataupload
    patient_id_1 = 24
    patient_id_2 = 546
    perform_dataupload(patient_id_1)
    perform_dataupload(patient_id_2)
    answer = get_patient_ids()
    expected = [24, 546], 200
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_ids_driver():
    from patient_monitoring_sys_server import get_patient_ids_driver
    from patient_monitoring_sys_server import perform_dataupload
    patient_id_1 = 24
    patient_id_2 = 546
    perform_dataupload(patient_id_1)
    perform_dataupload(patient_id_2)
    answer = get_patient_ids_driver()
    expected = [24, 546], 200
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_info_good():
    from patient_monitoring_sys_server import get_patient_info
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": b64string_test},
                           ecgimgs={"e": "e",
                                    "ekgimg1": b64string_test,
                                    "ekgimg2": "hello"},
                           hrlist=["e", 50],
                           ecgimgtstamps=["e", "2022-4-10 2:04:33",
                                          "2022-4-18 10:08:15"])
    saved_patient = test_patient.save()
    answer = get_patient_info(846137)
    expected = {"last_hr": 50,
                "latest_ecg": "hello", "name": "Li.Joshua",
                "latest_ecg_tstamp": "2022-4-18 10:08:15"}, 200
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_info_bad():
    from patient_monitoring_sys_server import get_patient_info
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": b64string_test},
                           ecgimgs={"e": "e",
                                    "ekgimg1": b64string_test,
                                    "ekgimg2": "hello"},
                           hrlist=["e", 50],
                           ecgimgtstamps=["e", "2022-4-10 2:04:33",
                                          "2022-4-18 10:08:15"])
    saved_patient = test_patient.save()
    answer = get_patient_info(222)
    expected = "Patient_id 222 was not found", 400
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_info_driver_good():
    from patient_monitoring_sys_server import get_patient_info_driver
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": b64string_test},
                           ecgimgs={"e": "e",
                                    "ekgimg1": b64string_test,
                                    "ekgimg2": "hello"},
                           hrlist=["e", 50],
                           ecgimgtstamps=["e", "2022-4-10 2:04:33",
                                          "2022-4-18 10:08:15"])
    saved_patient = test_patient.save()
    answer = get_patient_info_driver(846137)
    expected = {"last_hr": 50,
                "latest_ecg": "hello", "name": "Li.Joshua",
                "latest_ecg_tstamp": "2022-4-18 10:08:15"}, 200
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_info_driver_bad():
    from patient_monitoring_sys_server import get_patient_info_driver
    from patient_monitoring_sys_server import perform_dataupload
    patient_id = 345
    name = "Ben Randoing"
    perform_dataupload(patient_id, patname=name, medimgbytes="",
                       ecgimgbytes=b64string_test, hr=50)
    answer = get_patient_info_driver(222)
    expected = "Patient_id 222 was not found", 400
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


@pytest.mark.parametrize("patient_id, expected", [
    ["Ben", ("Patient_id was not an integer", 400)],
    [25, (25, 200)],
])
def test_validate_patient_id(patient_id, expected):
    from patient_monitoring_sys_server import validate_patient_id
    answer = validate_patient_id(patient_id)
    assert answer == expected


def test_get_patient_ecg_times_good():
    from patient_monitoring_sys_server import get_patient_ecg_times
    from patient_monitoring_sys_server import perform_dataupload
    patient_id = 846137
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": "somethinghex"},
                           ecgimgs={"e": "e"},
                           hrlist=["e"],
                           ecgimgtstamps=["2022-4-10 2:04:33"])
    test_patient.save()
    answer = get_patient_ecg_times(846137)
    expected = test_patient.ecgimgtstamps, 200
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_ecg_times_bad():
    from patient_monitoring_sys_server import get_patient_ecg_times
    from patient_monitoring_sys_server import perform_dataupload
    patient_id = 345
    name = "Ben Randoing"
    perform_dataupload(patient_id, patname=name, medimgbytes="",
                       ecgimgbytes=b64string_test, hr=50)
    answer = get_patient_ecg_times(222)
    expected = "Patient_id 222 was not found", 400
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_ecg_times_driver_good():
    from patient_monitoring_sys_server import get_patient_ecg_times_driver
    from patient_monitoring_sys_server import perform_dataupload
    patient_id = 846137
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": "somethinghex"},
                           ecgimgs={"e": "e"},
                           hrlist=["e"],
                           ecgimgtstamps=["2022-4-10 2:04:33"])
    test_patient.save()
    answer = get_patient_ecg_times_driver(846137)
    expected = test_patient.ecgimgtstamps, 200
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_ecg_times_driver_bad():
    from patient_monitoring_sys_server import get_patient_ecg_times_driver
    from patient_monitoring_sys_server import perform_dataupload
    patient_id = 345
    name = "Ben Randoing"
    perform_dataupload(patient_id, patname=name, medimgbytes="",
                       ecgimgbytes=b64string_test, hr=50)
    answer = get_patient_ecg_times_driver(222)
    expected = "Patient_id 222 was not found", 400
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


@pytest.mark.parametrize("mhrno, index, expected", [
    [846137, 1, ({"image": b64string_test,
                  "hr": 50}, 200)],
    [846138, 1, ("Patient_id 846138 was not found", 400)],
    [846137, 3, ("ECG image not found", 400)],
    [846136, 2, ("ECG image list is empty!", 400)]
    ])
def test_locate_ecg_img(mhrno, index, expected):
    from patient_monitoring_sys_server import locate_ecg_img
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": b64string_test},
                           ecgimgs={"e": "e",
                                    "ekgimg1": b64string_test,
                                    "ekgimg2": "hello"},
                           hrlist=["e", 50, 89],
                           ecgimgtstamps=["e", "2022-4-10 2:04:33",
                                          "2022-4-18 10:08:15"])
    saved_patient = test_patient.save()
    test_patient1 = Patient(mhrnumber=846136,
                            name="Li.Joshua",
                            medimgs={"e": "e",
                                     "medimg1": "somethinghex"},
                            ecgimgs={"e": "e"},
                            hrlist=["e"],
                            ecgimgtstamps=["2022-4-10 2:04:33"])
    test_patient1.save()
    answer = locate_ecg_img(mhrno, index)
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


@pytest.mark.parametrize("patient_id, ecg_img_index, expected", [
    ["9.9", "1", ("Patient_id is not an integer", 400)],
    ["9", "1.1", ("ECG_img_index is not an integer", 400)],
    ["8", "1", (True, 200)]
    ])
def test_validate_get_ecg_img(patient_id, ecg_img_index, expected):
    from patient_monitoring_sys_server import validate_get_ecg_img
    answer = validate_get_ecg_img(patient_id, ecg_img_index)
    assert answer == expected


@pytest.mark.parametrize("patient_id, ecg_img_index, expected", [
    [846137, 1, ({"image": b64string_test,
                  "hr": 50}, 200)],
    [846138, 1, ("Patient_id 846138 was not found", 400)],
    [846137, 3, ("ECG image not found", 400)],
    [846136, 2, ("ECG image list is empty!", 400)],
    ["9.9", "1", ("Patient_id is not an integer", 400)],
    ["9", "1.1", ("ECG_img_index is not an integer", 400)],
    ["8", "1", ("Patient_id 8 was not found", 400)]
    ])
def test_get_ecg_img_driver(patient_id, ecg_img_index, expected):
    from patient_monitoring_sys_server import get_ecg_img_driver
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": b64string_test},
                           ecgimgs={"e": "e",
                                    "ekgimg1": b64string_test,
                                    "ekgimg2": "hello"},
                           hrlist=["e", 50, 89],
                           ecgimgtstamps=["e", "2022-4-10 2:04:33",
                                          "2022-4-18 10:08:15"])
    saved_patient = test_patient.save()
    test_patient1 = Patient(mhrnumber=846136,
                            name="Li.Joshua",
                            medimgs={"e": "e",
                                     "medimg1": "somethinghex"},
                            ecgimgs={"e": "e"},
                            hrlist=["e"],
                            ecgimgtstamps=["2022-4-10 2:04:33"])
    test_patient1.save()
    answer = get_ecg_img_driver(patient_id, ecg_img_index)
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_med_times_good():
    from patient_monitoring_sys_server import get_patient_med_times
    from patient_monitoring_sys_server import perform_dataupload
    patient_id = 846137
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": "somethinghex"},
                           ecgimgs={"e": "e"},
                           hrlist=["e"],
                           ecgimgtstamps=["2022-4-10 2:04:33"],
                           medimgtstamps=["2022-4-10 2:04:33"])
    test_patient.save()
    answer = get_patient_med_times(846137)
    expected = test_patient.medimgtstamps, 200
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_med_times_bad():
    from patient_monitoring_sys_server import get_patient_med_times
    from patient_monitoring_sys_server import perform_dataupload
    patient_id = 345
    name = "Ben Randoing"
    perform_dataupload(patient_id, patname=name, medimgbytes=b64string_test)
    answer = get_patient_med_times(222)
    expected = "Patient_id 222 was not found", 400
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_med_times_driver_good():
    from patient_monitoring_sys_server import get_patient_med_times_driver
    from patient_monitoring_sys_server import perform_dataupload
    patient_id = 846137
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": "somethinghex"},
                           ecgimgs={"e": "e"},
                           hrlist=["e"],
                           ecgimgtstamps=["2022-4-10 2:04:33"],
                           medimgtstamps=["2022-4-10 2:04:33"])
    test_patient.save()
    answer = get_patient_med_times_driver(846137)
    expected = test_patient.medimgtstamps, 200
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


def test_get_patient_med_times_driver_bad():
    from patient_monitoring_sys_server import get_patient_med_times_driver
    from patient_monitoring_sys_server import perform_dataupload
    patient_id = 345
    name = "Ben Randoing"
    perform_dataupload(patient_id, patname=name, medimgbytes=b64string_test)
    answer = get_patient_med_times_driver(222)
    expected = "Patient_id 222 was not found", 400
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


@pytest.mark.parametrize("mhrno, index, expected", [
    [846137, 1, (b64string_test, 200)],
    [846138, 1, ("Patient_id 846138 was not found", 400)],
    [846137, 3, ("med image not found", 400)],
    [846136, 2, ("med image list is empty!", 400)]
    ])
def test_locate_med_img(mhrno, index, expected):
    from patient_monitoring_sys_server import locate_med_img
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": b64string_test},
                           ecgimgs={"e": "e",
                                    "ekgimg1": b64string_test,
                                    "ekgimg2": "hello"},
                           hrlist=["e", 50, 89],
                           ecgimgtstamps=["e", "2022-4-10 2:04:33",
                                          "2022-4-18 10:08:15"],
                           medimgtstamps=["e", "2022-4-10 2:04:33"])
    saved_patient = test_patient.save()
    test_patient1 = Patient(mhrnumber=846136,
                            name="Li.Joshua",
                            medimgs={"e": "e"},
                            ecgimgs={"e": "e"},
                            hrlist=["e"],
                            ecgimgtstamps=["e"],
                            medimgtstamps=["e"])
    test_patient1.save()
    answer = locate_med_img(mhrno, index)
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected


@pytest.mark.parametrize("patient_id, med_img_index, expected", [
    ["9.9", "1", ("Patient_id is not an integer", 400)],
    ["9", "1.1", ("med_img_index is not an integer", 400)],
    ["8", "1", (True, 200)]
    ])
def test_validate_get_med_img(patient_id, med_img_index, expected):
    from patient_monitoring_sys_server import validate_get_med_img
    answer = validate_get_med_img(patient_id, med_img_index)
    assert answer == expected


@pytest.mark.parametrize("patient_id, med_img_index, expected", [
    [846137, 1, (b64string_test, 200)],
    [846138, 1, ("Patient_id 846138 was not found", 400)],
    [846137, 3, ("med image not found", 400)],
    [846136, 2, ("med image list is empty!", 400)],
    ["9.9", "1", ("Patient_id is not an integer", 400)],
    ["9", "1.1", ("med_img_index is not an integer", 400)],
    ["8", "1", ("Patient_id 8 was not found", 400)]
    ])
def test_get_med_img_driver(patient_id, med_img_index, expected):
    from patient_monitoring_sys_server import get_med_img_driver
    test_patient = Patient(mhrnumber=846137,
                           name="Li.Joshua",
                           medimgs={"e": "e",
                                    "medimg1": b64string_test},
                           ecgimgs={"e": "e",
                                    "ekgimg1": b64string_test,
                                    "ekgimg2": "hello"},
                           hrlist=["e", 50, 89],
                           ecgimgtstamps=["e", "2022-4-10 2:04:33",
                                          "2022-4-18 10:08:15"],
                           medimgtstamps=["e", "2022-4-10 2:04:33"])
    saved_patient = test_patient.save()
    test_patient1 = Patient(mhrnumber=846136,
                            name="Li.Joshua",
                            medimgs={"e": "e"},
                            ecgimgs={"e": "e"},
                            hrlist=["e"],
                            ecgimgtstamps=["e"],
                            medimgtstamps=["e"])
    test_patient1.save()
    answer = get_med_img_driver(patient_id, med_img_index)
    db = mongo_client['finalprojDatabase']
    col = db['patient']
    col.drop()
    assert answer == expected
