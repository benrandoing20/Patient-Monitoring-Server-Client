import logging
from flask import Flask, request, jsonify

from pymodm import connect
from pymodm import errors as pymodm_errors

from mhrpatient_info import Patient

import base64
import io
import matplotlib.image as mpimg
from matplotlib import pyplot as plt

from datetime import datetime, time, date

app = Flask(__name__)


def init_server():
    """Initializes server conditions

    This function can be used for any speific tasks that you would like to run
    upon initial server start-up. Currently, it configures the logging
    functionality and it makes a connection to a MongoDB database. Ben is on
    MacOS, which is not experiencing issues with accessing a MongoDB database,
    but I am (Windows 10), so I included two different connect() statements.
    """
    logging.basicConfig(filename="patient_monitoring_sys_server.log",
                        level=logging.DEBUG,
                        filemode='w')
    print("Connecting to database...")
    connect("mongodb+srv://LijoShua:cvK3Z53NofAz1jPl@bme547.iiecj."
            "mongodb.net/finalprojDatabase?retryWrites=true&w=majority",
            tls=True, tlsAllowInvalidCertificates=True)
    # @Ben comment out the first connect and uncomment the second connect
    # if the first connect isn't working
    # connect("mongodb+srv://bme547classwork:Percussionist20"
    #         "@bme547.1e368.mongodb.net/finalprojDatabase?retry"
    #         "Writes=true&w=majority",
    #         tls=True, tlsAllowInvalidCertificates=True)
    print("Connection attempt finished")


@app.route("/patient/dataupload", methods=["POST"])
def patient_dataupload_handler():
    """Handles requests to upload patient data to MHR database

    This handler method operates under the route /patient/dataupload and
    can receive a JSON-encoded string that looks like this:

    {"mhrnumber": int,
     "name": str,
     "medimg": b64_string,
     "ecgimg": b64_string,
     "hr": int
    }

    "mhrnumber": int - patient's medical health record ID number.
    REQUIRED PARAMETER
    "name": str - patient's name, generally in format LastName.FirstName.
    OPTIONAL PARAMETER
    "medimgbytes": b64_string - string variable containing the image bytes
    encoded as a base64 string. OPTIONAL PARAMETER
    "ecgimgbytes": b64_string - string variable containing the image bytes
    encoded as a base64 string. OPTIONAL PARAMETER
    "hr": int - the heart rate calculated from the provided ecgimg

    :returns: str summarizing what info was uploaded and int 200 if
    upload is successful, or str error message and int error code if
    upload is not successful.
    """
    in_data = request.get_json()
    answer, status_code = patient_dataupload_driver(in_data)
    return jsonify(answer), status_code


def patient_dataupload_driver(in_data):
    """Implements /patient/dataupload route for adding patient data

    The flask handler function for the /patient/dataupload route calls
    this function to implement the functionality. It receives as a
    parameter a dictionary that should contain the needed info in the
    following format:

    {"mhrnumber": int, "name": str,
     "medimgbytes": b64_string, "ecgimgbytes": b64_string,
     "hr": int}

    :param in_data: The input data received by the route. Ideally,
    it is a dictionary

    :returns: str summarizing what info was uploaded and int 200 if
    upload is successful, or str error message and int error code if
    upload is not successful.
        Status 200 = only medimgbytes, ecgimgbytes, and mhrno have
        values (bc)
        Status 201 = only medimgbytes and mhrno have values (b)
        Status 202 = only ecgimgbytes and mhrno have values (c)
        Status 203 = only mhrnumber has a value
        Status 204 = all fields have values (abc)
        Status 205 = only mhrno, name, and medimgbytes
        have values (ab)
        Status 206 = only mhrno, name, and ecgimgbytes
        have values (ac)
        Status 207 = only mhrno and name have values (a)
    """
    answer, status_code = validate_dataupload_driver(in_data)

    if status_code == 400:
        return answer, status_code
    elif status_code == 200:  # abc, ab, ac, bc, a, b, c
        answer, status_code = \
            perform_dataupload(mhrno=int(in_data["mhrnumber"]),
                               medimgbytes=in_data["medimgbytes"],
                               ecgimgbytes=in_data["ecgimgbytes"],
                               hr=int(in_data["hr"]))
        return answer, status_code
    elif status_code == 201:
        answer, status_code = \
            perform_dataupload(mhrno=int(in_data["mhrnumber"]),
                               medimgbytes=in_data["medimgbytes"])
        return answer, status_code
    elif status_code == 202:
        answer, status_code = \
            perform_dataupload(mhrno=int(in_data["mhrnumber"]),
                               ecgimgbytes=in_data["ecgimgbytes"],
                               hr=int(in_data["hr"]))
        return answer, status_code
    elif status_code == 203:
        answer, status_code = \
            perform_dataupload(mhrno=int(in_data["mhrnumber"]))
        return answer, status_code
    elif status_code == 204:
        answer, status_code = \
            perform_dataupload(mhrno=int(in_data["mhrnumber"]),
                               patname=in_data["name"],
                               medimgbytes=in_data["medimgbytes"],
                               ecgimgbytes=in_data["ecgimgbytes"],
                               hr=int(in_data["hr"]))
        return answer, status_code
    elif status_code == 205:
        answer, status_code = \
            perform_dataupload(mhrno=int(in_data["mhrnumber"]),
                               patname=in_data["name"],
                               medimgbytes=in_data["medimgbytes"])
        return answer, status_code
    elif status_code == 206:
        answer, status_code = \
            perform_dataupload(mhrno=int(in_data["mhrnumber"]),
                               patname=in_data["name"],
                               ecgimgbytes=in_data["ecgimgbytes"],
                               hr=int(in_data["hr"]))
        return answer, status_code
    elif status_code == 207:
        answer, status_code = \
            perform_dataupload(mhrno=int(in_data["mhrnumber"]),
                               patname=in_data["name"])
        return answer, status_code


def validate_dataupload_driver(in_data):
    """Validates that input data to server contains a dictionary with the
    correct keys and data types

    To avoid server errors, this function checks that the input data is a
    dictionary, that it has at least the mhrnumber key, and that the datatypes
    stored in the posted keys are of the proper type.

    :param in_data: The input data received by the route. Ideally,
    it is a dictionary

    :returns: bool True and int status code 200/1/2/3 if data validation is
    successful, and str error message and int status code 400 if not
    successful.
    """
    expected_keys = ["mhrnumber", "name", "medimgbytes", "ecgimgbytes", "hr"]
    expected_types = [int, str, str, str, int]
    missing_keys = []
    if type(in_data) is not dict:
        return "The input was not a dictionary.", 400
    input_keys = in_data.keys()
    if expected_keys[0] not in input_keys:
        error_message = ("Attempted data upload does not contain"
                         " the mandatory"
                         " mhrnumber key")
        return error_message, 400
    for input_key in input_keys:
        if input_key not in expected_keys:
            error_message = ("The provided key {} is not an"
                             " accepted key.").format(input_key)
            return error_message, 400
        # If the input key is one of the expected keys, then we
        # evaluate whether its value is the correct datatype.
        for expected_key, expected_type in\
                zip(expected_keys, expected_types):
            if expected_key is input_key:
                if type(in_data[expected_key]) is not expected_type:
                    if expected_key == "mhrnumber" and \
                            (type(in_data[expected_key]) is str):
                        try:
                            mhrnumber_int = int(in_data[expected_key])
                        except ValueError:
                            return "mhrnumber was not an integer", 400
                    if expected_key == "hr" and \
                            (type(in_data[expected_key]) is str):
                        try:
                            hr_int = int(in_data[expected_key])
                        except ValueError:
                            return "hr was not an integer", 400
                    error_message = ("Value of key {} is not of"
                                     " type {}").format(expected_key,
                                                        expected_type)
                    return error_message, 400
                if expected_key == "medimgbytes" \
                        or expected_key == "ecgimgbytes":
                    b64_string = in_data[expected_key]
                    try:
                        image_bytes = base64.b64decode(b64_string)
                    except ValueError:
                        error_message =\
                            ("The provided image string is not in"
                             " base64 and cannot be converted to"
                             " an image file")
                        return error_message, 400
    if ("ecgimgbytes" in input_keys) and ("hr" not in input_keys):
        error_message = ("Did not provide a heart rate along with the"
                         " uploaded image data")
        return error_message, 400
    if ("hr" in input_keys) and ("ecgimgbytes" not in input_keys):
        error_message = ("Did not provide an uploaded image data file"
                         " along with the provided heart rate")
        return error_message, 400
    # After making sure only the keys that should be there are there,
    # and making sure their values are of appropriate type,
    # the following identifies the missing keys
    for expected_key in expected_keys:
        if expected_key not in input_keys:
            if expected_key != "mhrnumber":
                missing_keys.append(expected_key)
    if len(missing_keys) == 4:
        return True, 203
    if len(missing_keys) == 3:
        if "name" in missing_keys:
            return True, 201
        if "medimgbytes" in missing_keys:
            return True, 207
    if len(missing_keys) == 2:
        if "medimgbytes" in missing_keys:
            return True, 202
        if "ecgimgbytes" in missing_keys:
            return True, 205
    if len(missing_keys) == 1:
        if missing_keys[0] == "medimgbytes":
            return True, 206
        if missing_keys[0] == "name":
            return True, 200
    return True, 204


def perform_dataupload(mhrno, patname="", medimgbytes="",
                       ecgimgbytes="", hr=""):
    """Updates the patient database with the provided info

    perform_dataupload will create a new patient entry for a new
    mhrnumber and add any images that were attached to the post
    request. This method will also just add attached images to
    an existing patient if the mhrnumber is already in the
    database.

    :param mhrnumber: int - patient's medical health record ID number.
    REQUIRED PARAMETER
    :param patname: str - patient's name, generally in format
    LastName.FirstName. OPTIONAL PARAMETER
    :param medimgbytes: b64_string - string variable containing the image bytes
    encoded as a base64 string. OPTIONAL PARAMETER with default empty string
    :param ecgimgbytes: b64_string - string variable containing the image bytes
    encoded as a base64 string. OPTIONAL PARAMETER with default empty string

    :returns: str summary of data input and status code 200
    """
    # abc,ab,ac,bc,a,b,c
    try:
        patient = Patient.objects.raw({"_id": mhrno}).first()
    except Exception:
        # If the patient doesn't exist in the db, create a new patient
        # and add any data that was provided along with the patient.
        if (
            patname == "" and
            medimgbytes == "" and  # abc
            ecgimgbytes == ""
                ):
            new_patient = Patient(mhrnumber=mhrno,
                                  name="No name given",
                                  medimgs={"e": "e"},
                                  ecgimgs={"e": "e"},
                                  hrlist=["e"],
                                  ecgimgtstamps=["e"],
                                  medimgtstamps=["e"])
            new_patient.save()
            message = ("Created new patient for mhrnumber {}."
                       " No new data added to this patient").\
                format(mhrno)
            return message, 200
        elif patname == "" and medimgbytes == "":  # ab
            timestamp = current_time()
            new_patient = Patient(mhrnumber=mhrno,
                                  name="No name given",
                                  medimgs={"e": "e"},
                                  ecgimgs={"e": "e",
                                           "ekgimg1": ecgimgbytes},
                                  hrlist=["e", hr],
                                  ecgimgtstamps=["e", timestamp],
                                  medimgtstamps=["e"])
            new_patient.save()
            message = ("Created new patient for mhrnumber {}."
                       " Added provided ecgimg, hr, and current"
                       " time and date. Stored image as ekgimg1").\
                format(mhrno)
            return message, 200
        elif patname == "" and ecgimgbytes == "":  # ac
            timestamp = current_time()
            new_patient = Patient(mhrnumber=mhrno,
                                  name="No name given",
                                  medimgs={"e": "e",
                                           "medimg1": medimgbytes},
                                  ecgimgs={"e": "e"},
                                  hrlist=["e"],
                                  ecgimgtstamps=["e"],
                                  medimgtstamps=["e", timestamp])
            new_patient.save()
            message = ("Created new patient for mhrnumber {}."
                       " Added provided medimg and stored as"
                       " medimg1.").format(mhrno)
            return message, 200
        elif medimgbytes == "" and ecgimgbytes == "":  # bc
            new_patient = Patient(mhrnumber=mhrno,
                                  name=patname,
                                  medimgs={"e": "e"},
                                  ecgimgs={"e": "e"},
                                  hrlist=["e"],
                                  ecgimgtstamps=["e"],
                                  medimgtstamps=["e"])
            new_patient.save()
            message = ("Created new patient for mhrnumber {}."
                       " Added name {} to record.").\
                format(mhrno, patname)
            return message, 200
        elif patname == "":  # a
            timestamp = current_time()
            new_patient = Patient(mhrnumber=mhrno,
                                  name="No name given",
                                  medimgs={"e": "e",
                                           "medimg1": medimgbytes},
                                  ecgimgs={"e": "e",
                                           "ekgimg1": ecgimgbytes},
                                  hrlist=["e", hr],
                                  ecgimgtstamps=["e", timestamp],
                                  medimgtstamps=["e", timestamp])
            new_patient.save()
            message = ("Created new patient for mhrnumber {}."
                       " Added provided ecgimg, hr, and current"
                       " time and date. Stored ecgimage as ekgimg1"
                       " Added provided medimg stored as medimg1").\
                format(mhrno)
            return message, 200
        elif medimgbytes == "":  # b
            timestamp = current_time()
            new_patient = Patient(mhrnumber=mhrno,
                                  name=patname,
                                  medimgs={"e": "e"},
                                  ecgimgs={"e": "e",
                                           "ekgimg1": ecgimgbytes},
                                  hrlist=["e", hr],
                                  ecgimgtstamps=["e", timestamp],
                                  medimgtstamps=["e"])
            new_patient.save()
            message = ("Created new patient for mhrnumber {}."
                       " Added name {} to record."
                       " Added provided ecgimg, hr, and current"
                       " time and date. Stored image as ekgimg1").\
                format(mhrno, patname)
            return message, 200
        elif ecgimgbytes == "":  # c
            timestamp = current_time()
            new_patient = Patient(mhrnumber=mhrno,
                                  name=patname,
                                  medimgs={"e": "e",
                                           "medimg1": medimgbytes},
                                  ecgimgs={"e": "e"},
                                  hrlist=["e"],
                                  ecgimgtstamps=["e"],
                                  medimgtstamps=["e", timestamp])
            new_patient.save()
            message = ("Created new patient for mhrnumber {}."
                       " Added name {} to record."
                       " Added provided medimg and stored as"
                       " medimg1.").format(mhrno, patname)
            return message, 200
        else:
            timestamp = current_time()
            new_patient = Patient(mhrnumber=mhrno,
                                  name=patname,
                                  medimgs={"e": "e",
                                           "medimg1": medimgbytes},
                                  ecgimgs={"e": "e",
                                           "ekgimg1": ecgimgbytes},
                                  hrlist=["e", hr],
                                  ecgimgtstamps=["e", timestamp],
                                  medimgtstamps=["e", timestamp])
            new_patient.save()
            message = ("Created new patient for mhrnumber {}."
                       " Added name {} to record."
                       " Added provided ecgimg, hr, and current"
                       " time and date. Stored ecgimage as ekgimg1"
                       " Added provided medimg stored as medimg1").\
                format(mhrno, patname)
            return message, 200
    # If patient already exists in the database, add provided info to
    # the patient's existing records
    if (
        patname == "" and
        medimgbytes == "" and  # abc
        ecgimgbytes == ""
            ):
        message = "No new data added to patient {}".format(mhrno)
        return message, 200
    elif patname == "" and medimgbytes == "":  # ab
        timestamp = current_time()
        num_img = len(patient.ecgimgs)-1
        next_img = num_img+1
        filename = "ekgimg{}".format(next_img)
        patient.ecgimgs[filename] = ecgimgbytes
        patient.hrlist.append(hr)
        patient.ecgimgtstamps.append(timestamp)
        patient.save()
        message = ("Added provided ecgimg, hr, and current"
                   " time and date for patient {}. Stored"
                   " image as {}").\
            format(mhrno, filename)
        return message, 200
    elif patname == "" and ecgimgbytes == "":  # ac
        num_img = len(patient.medimgs)-1
        next_img = num_img+1
        filename = "medimg{}".format(next_img)
        patient.medimgs[filename] = medimgbytes
        timestamp = current_time()
        patient.medimgtstamps.append(timestamp)
        patient.save()
        message = ("Added provided medimg for patient {}. Stored"
                   " image as {}").format(mhrno, filename)
        return message, 200
    elif medimgbytes == "" and ecgimgbytes == "":  # bc
        patient.name = patname
        patient.save()
        message = ("Added name {} for patient {}.").\
            format(patname, mhrno)
        return message, 200
    elif patname == "":  # a
        timestamp = current_time()
        ecg_num_img = len(patient.ecgimgs)-1
        ecg_next_img = ecg_num_img+1
        ecg_filename = "ekgimg{}".format(ecg_next_img)
        patient.ecgimgs[ecg_filename] = ecgimgbytes
        patient.hrlist.append(hr)
        med_num_img = len(patient.medimgs)-1
        med_next_img = med_num_img+1
        med_filename = "medimg{}".format(med_next_img)
        patient.medimgs[med_filename] = medimgbytes
        patient.ecgimgtstamps.append(timestamp)
        patient.medimgtstamps.append(timestamp)
        patient.save()
        message = ("Added provided ecgimg, hr, and current"
                   " time and date for patient {}. Stored"
                   " ecgimage as {}. Stored medimage as {}").\
            format(mhrno, ecg_filename, med_filename)
        return message, 200
    elif medimgbytes == "":  # b
        timestamp = current_time()
        num_img = len(patient.ecgimgs)-1
        next_img = num_img+1
        filename = "ekgimg{}".format(next_img)
        patient.ecgimgs[filename] = ecgimgbytes
        patient.hrlist.append(hr)
        patient.ecgimgtstamps.append(timestamp)
        patient.name = patname
        patient.save()
        message = ("Added name {} for patient {}."
                   " Added provided ecgimg, hr, and current"
                   " time and date. Stored image as {}").\
            format(patname, mhrno, filename)
        return message, 200
    elif ecgimgbytes == "":  # c
        num_img = len(patient.medimgs)-1
        next_img = num_img+1
        filename = "medimg{}".format(next_img)
        patient.medimgs[filename] = medimgbytes
        patient.name = patname
        timestamp = current_time()
        patient.medimgtstamps.append(timestamp)
        patient.save()
        message = ("Added name {} for patient {}."
                   "Added provided medimg. Stored"
                   " image as {}").\
            format(patname, mhrno, filename)
        return message, 200
    else:
        timestamp = current_time()
        ecg_num_img = len(patient.ecgimgs)-1
        ecg_next_img = ecg_num_img+1
        ecg_filename = "ekgimg{}".format(ecg_next_img)
        patient.ecgimgs[ecg_filename] = ecgimgbytes
        patient.hrlist.append(hr)
        med_num_img = len(patient.medimgs)-1
        med_next_img = med_num_img+1
        med_filename = "medimg{}".format(med_next_img)
        patient.medimgs[med_filename] = medimgbytes
        patient.name = patname
        patient.ecgimgtstamps.append(timestamp)
        patient.medimgtstamps.append(timestamp)
        patient.save()
        message = ("Added name {} for patient {}."
                   " Added provided ecgimg, hr, and current"
                   " time and date. Stored"
                   " ecgimage as {}. Stored medimage as {}").\
            format(patname, mhrno, ecg_filename, med_filename)
        return message, 200


def current_time():
    """Implements identifying the current time of the heart rate entry

   This function implements the obtaining of the current date and time to
   match with a heart rate entry for a particular patient

   :returns: str formatted_now with the current date and time
   """
    now = datetime.now()
    formatted_now = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
    return formatted_now


@app.route("/get_ids", methods=["GET"])
def get_patient_ids_handler():
    """Obtains patient ids from the MongoDB database

    get_patient_ids_handler operates under the route
    /ids,
    which does not receive any inputs as the get request is general and
    desires a list of all patient_ids available in the database.

    :returns: patient medical record number and status code
    200 if
    successful
    """
    answer, status_code = get_patient_ids_driver()
    return jsonify(answer), status_code


def get_patient_ids_driver():
    """Runs the function to acquire all patient ids

    get_patient_ids_driver does not need to first validates the quality of the
    input data as there are no inputs. Subsequently, a list of patient ids
    are obtained from the health database.

    :returns: patient medical record number list and status code 200 if
    successful
    """
    answer, status_code = get_patient_ids()
    return answer, status_code


def get_patient_ids():
    """Obtains the medical record numbers currently in the database

    get_patient_ids looks for all the instances of the Patient class in
    the database and then appends the mhrnumber ids into a list to output.

    :return: patient medical record number list and status code 200 if
    successful
    """
    patients = Patient.objects.raw({})
    ids = []
    for item in patients:
        ids.append(item.mhrnumber)
    return ids, 200


@app.route("/get_patient_info/<patient_id>", methods=["GET"])
def get_patient_info_handler(patient_id):
    """Obtains patient info for a specific patient in MongoDB

    get_patient_info_handler operates under the route
    /get_patient_info/<patient_id>,
    which receives a JSON-encoded string with the following format:

    :param: string of an integer patient medical record number

    :returns: string patient name, b64 string ecg image, heart rate int,
    and associated timestamp string with status code 200 if successful.
    A string error message and status code of 400 are returned if the
    patient_id is not an int or not found within the MongoDB database
    """
    answer, status_code = get_patient_info_driver(patient_id)
    return jsonify(answer), status_code


def get_patient_info_driver(patient_id):
    """Runs the appropriate validation and acquisition module
    to get patient info

    get_patient_info_driver first validates the quality of the
    input data to ensure the patient_id provided is an int. Subsequently,
    patient information is obtained from the health database. This
    information is the patient name, most recent b64 string for the ecg
    imagee, and most recent heart rate. This module takes in the JSON

    :param: string of an integer patient medical record number

    :returns: string patient name, b64 string ecg image, and heart rate int
    with status code 200 if successful. A string erro rmessage and status
    code of 400 are returned if the patient_id is not an int or not found
    within the MongoDB database
    """
    answer, status_code = validate_patient_id(patient_id)
    if status_code != 200:
        return answer, status_code
    answer, status_code = get_patient_info(answer)
    return answer, status_code


def validate_patient_id(patient_id):
    """Convert the patient id is an integer if possible

    The patient_id, received as a string, is checked to see if it contains an
    integer.  If it does, the string is converted to an integer and is returned
    with a status code of 200.  If the string does not an integer, an error
    message is returned with a status code of 400.

    :param: patient_id (str): the patient id string taken from the variable URL

    :returns: int or string, int: the patient id as an integer or an error
    message string; status code
    """
    try:
        patient_id_int = int(patient_id)
    except ValueError:
        return "Patient_id was not an integer", 400
    return patient_id_int, 200


def get_patient_info(patient_id):
    """Obtains the name, most recent heart_rate and ecg image

    get_patient_info finds a specific patient based on a medical record
    number input. The output of the name, and most recent ecg image with
    heart_rate is provided.

    :param: patient_id (str): the patient id string taken from the variable URL

    :return: string patient name, b64 string ecg image, and heart rate int
    with status code 200 if successful. A string erro rmessage and status
    code of 400 are returned if the patient_id is not an int or not found
    within the MongoDB database
    """
    try:
        patient = Patient.objects.raw({"_id": patient_id}).first()
    except pymodm_errors.DoesNotExist:
        return "Patient_id {} was not found".format(patient_id), 400
    ecgimg_keys = list(patient.ecgimgs.keys())
    latest_file = "e"
    for i in range(1, len(ecgimg_keys)):
        if ecgimg_keys[i] > latest_file:
            latest_file = ecgimg_keys[i]
    info_json = {"name": patient.name, "last_hr": patient.hrlist[-1],
                 "latest_ecg": patient.ecgimgs[latest_file],
                 "latest_ecg_tstamp": patient.ecgimgtstamps[-1]}
    return info_json, 200


@app.route("/get_ecg_times/<patient_id>", methods=["GET"])
def get_patient_ecg_times_handler(patient_id):
    """Obtains ecg timestamps for a specific patient in MongoDB

    get_patient_ecg_times_handler operates under the route
    /get_ecg_times/<patient_id>,
    which receives a JSON-encoded string with the following format:

    :param: patient_id (str): the patient id string taken from the variable URL

    :returns: list ecg timestamps with status code 200 if successful. A
    string error message and status code of 400 are returned if the
    patient_id is not an int or not found within the MongoDB database
    """
    answer, status_code = get_patient_ecg_times_driver(patient_id)
    return jsonify(answer), status_code


def get_patient_ecg_times_driver(patient_id):
    """Runs the appropriate validation and acquisition module
    to get patient ecg times

    get_patient_ecg_time_driver first validates the quality of the
    input data to ensure the patient_id provided is an int. Subsequently,
    patient information is obtained from the health database. This
    information is the list of time stamps associated with the ecg data
    files. This module takes in the JSON

    :param: patient_id (str): the patient id string taken from the variable URL

    :returns: list ecg timestamps with status code 200 if successful. A
    string error message and status code of 400 are returned if the
    patient_id is not an int or not found within the MongoDB database
    """
    answer, status_code = validate_patient_id(patient_id)
    if status_code != 200:
        return answer, status_code
    answer, status_code = get_patient_ecg_times(answer)
    return answer, status_code


def get_patient_ecg_times(patient_id):
    """Obtains the ecg times for a specific patient currently in the
    database

    get_patient_ecg_times looks for all the instances of the Patient class in
    the database and then appends the ecg timestamps into a list to output.

    :param: patient_id (str): the patient id string taken from the variable URL

    :return: list ecg timestamps with status code 200 if successful. A
    string error message and status code of 400 are returned if the
    patient_id is not an int or not found within the MongoDB database
    """
    try:
        patient = Patient.objects.raw({"_id": patient_id}).first()
    except pymodm_errors.DoesNotExist:
        return "Patient_id {} was not found".format(patient_id), 400
    ecg_times = patient.ecgimgtstamps
    return ecg_times, 200


@app.route("/get_ecg_img/<patient_id>/<ecg_img_index>", methods=["GET"])
def get_ecg_img_handler(patient_id, ecg_img_index):
    """Obtains the ecg_img of selected patient at selected index

    This handler operates under the route
    /get_ecg_imgs/<patient_id>/<ecg_img_index> and downloads all
    ecg imgs for the given patient_id. It then searches for and
    returns the ecg img located at the specified index. This index
    matches the index of the selected timestamp.

    :param patient_id: str (int) patient id
    :param ecg_img_index: str (int) ecg img index

    :returns: status code 200 and jsonified dictionary containing
    b64 string image and hr if successful, error message
    and status code 400 if not successful.
    """
    answer, status_code = get_ecg_img_driver(patient_id,
                                             ecg_img_index)
    return jsonify(answer), status_code


def get_ecg_img_driver(patient_id, ecg_img_index):
    """Obtains desired ecg img

    This function oversees the obtaining of the desired
    ecg img. It first performs input validation to ensure
    both patient id and index are integers. It then runs
    the image search function.

    :param patient_id: str (int) patient id
    :param ecg_img_index: str (int) ecg img index

    :returns: status code 200 and dictionary containing
    b64 string image and hr if successful, error message
    and status code 400 if not successful.
    """
    answer, status_code = validate_get_ecg_img(patient_id,
                                               ecg_img_index)
    if status_code == 400:
        return answer, status_code
    mhrno = int(patient_id)
    index = int(ecg_img_index)
    package, status_code = locate_ecg_img(mhrno, index)
    return package, status_code


def validate_get_ecg_img(patient_id, ecg_img_index):
    """Performs input validation for get_ecg_img

    This function checks whether the two inputs are
    integers or strings that are convertible to
    integers.

    :param patient_id: str (int) patient id
    :param ecg_img_index: str (int) ecg img index

    :returns: bool True and status code 200 if data inputs
    are valid; error message and status code 400 if data
    are invalid.
    """
    try:
        int(patient_id)
    except ValueError:
        error_message = "Patient_id is not an integer"
        return error_message, 400
    try:
        int(ecg_img_index)
    except ValueError:
        error_message = "ECG_img_index is not an integer"
        return error_message, 400
    return True, 200


def locate_ecg_img(mhrno, index):
    """Locates the image file

    This function iterates through the ecg img dictionary
    keys to locate the desired key. It then returns the
    b64 image string value stored in that dictionary key.

    :param mhrno: int medical health record number
    :param index: int of index in the ecg timestamp list
    at which the selected timestamp is located

    :returns: status code 200 and dictionary containing
    b64 string image and hr if successful, error message
    and status code 400 if not successful.
    """
    try:
        patient = Patient.objects.raw({"_id": mhrno}).first()
    except pymodm_errors.DoesNotExist:
        return "Patient_id {} was not found".format(mhrno), 400
    ecgimg_keys = list(patient.ecgimgs.keys())
    foundkey = "empty"
    if len(ecgimg_keys) == 1:
        return "ECG image list is empty!", 400
    for key in ecgimg_keys[1:len(ecgimg_keys)]:
        imgnumber = (key.split("ekgimg"))[1]
        if index == int(imgnumber):
            foundkey = key
            ecgimgbytes = patient.ecgimgs[key]
            hr = patient.hrlist[index]
            info_dict = {"image": ecgimgbytes,
                         "hr": hr}
            return info_dict, 200
    error_message = "ECG image not found"
    return error_message, 400


@app.route("/get_med_times/<patient_id>", methods=["GET"])
def get_patient_med_times_handler(patient_id):
    """Obtains patient info for a specific patient in MongoDB

    get_patient_med_times operates under the route
    /get_med_times/<patient_id>,
    which receives a JSON-encoded string with the following format:

    :param patient_id: str (int) patient id

    :returns: jsonified list of timestamps with status code 200 if
    successful. A string error message and status code of 400 are
    returned if unsuccessful
    """
    answer, status_code = get_patient_med_times_driver(patient_id)
    return jsonify(answer), status_code


def get_patient_med_times_driver(patient_id):
    """Runs the appropriate validation and acquisition module
    to get patient info

    get_patient_med_times_driver first validates the quality of the
    input data to ensure the patient_id provided is an int. Subsequently,
    patient information is obtained from the health database.

    :param patient_id: str (int) patient id

    :returns: med timestamp list and status code 200 if
    successful; error message and status code 400 if not.
    """
    answer, status_code = validate_patient_id(patient_id)
    if status_code != 200:
        return answer, status_code
    answer, status_code = get_patient_med_times(answer)
    return answer, status_code


def get_patient_med_times(patient_id):
    """Obtains the med timestamps

    get_patient_med_times looks for all the instances of the Patient class in
    the database and then appends the med timestamps into a list to output.

    :param patient_id: int patient id

    :return: medtime list and status code 200 if successful; error message and
    status code 400 if not.
    """
    try:
        patient = Patient.objects.raw({"_id": patient_id}).first()
    except pymodm_errors.DoesNotExist:
        return "Patient_id {} was not found".format(patient_id), 400
    med_times = patient.medimgtstamps
    return med_times, 200


@app.route("/get_med_img/<patient_id>/<med_img_index>", methods=["GET"])
def get_med_img_handler(patient_id, med_img_index):
    """Obtains the med_img of selected patient at selected index

    This handler operates under the route
    /get_med_imgs/<patient_id>/<med_img_index> and downloads all
    med imgs for the given patient_id. It then searches for and
    returns the med img located at the specified index. This index
    matches the index of the selected timestamp.

    :param patient_id: str (int) patient id
    :param med_img_index: str (int) med img index

    :returns: status code 200 and jsonified
    b64 string image if successful, error message
    and status code 400 if not successful.
    """
    answer, status_code = get_med_img_driver(patient_id,
                                             med_img_index)
    return jsonify(answer), status_code


def get_med_img_driver(patient_id, med_img_index):
    """Obtains desired med img

    This function oversees the obtaining of the desired
    med img. It first performs input validation to ensure
    both patient id and index are integers. It then runs
    the image search function.

    :param patient_id: str (int) patient id
    :param med_img_index: str (int) med img index

    :returns: status code 200 and
    b64 string image if successful, error message
    and status code 400 if not successful.
    """
    answer, status_code = validate_get_med_img(patient_id,
                                               med_img_index)
    if status_code == 400:
        return answer, status_code
    mhrno = int(patient_id)
    index = int(med_img_index)
    package, status_code = locate_med_img(mhrno, index)
    return package, status_code


def validate_get_med_img(patient_id, med_img_index):
    """Performs input validation for get_med_img

    This function checks whether the two inputs are
    integers or strings that are convertible to
    integers.

    :param patient_id: str (int) patient id
    :param med_img_index: str (int) med img index

    :returns: bool True and status code 200 if data inputs
    are valid; error message and status code 400 if data
    are invalid.
    """
    try:
        int(patient_id)
    except ValueError:
        error_message = "Patient_id is not an integer"
        return error_message, 400
    try:
        int(med_img_index)
    except ValueError:
        error_message = "med_img_index is not an integer"
        return error_message, 400
    return True, 200


def locate_med_img(mhrno, index):
    """Locates the image file

    This function iterates through the med img dictionary
    keys to locate the desired key. It then returns the
    b64 image string value stored in that dictionary key.

    :param mhrno: int medical health record number
    :param index: int of index in the med timestamp list
    at which the selected timestamp is located

    :returns: status code 200 and
    b64 string image if successful, error message
    and status code 400 if not successful.
    """
    try:
        patient = Patient.objects.raw({"_id": mhrno}).first()
    except pymodm_errors.DoesNotExist:
        return "Patient_id {} was not found".format(mhrno), 400
    medimg_keys = list(patient.medimgs.keys())
    foundkey = "empty"
    if len(medimg_keys) == 1:
        return "med image list is empty!", 400
    for key in medimg_keys[1:len(medimg_keys)]:
        imgnumber = (key.split("medimg"))[1]
        if index == int(imgnumber):
            foundkey = key
            medimgbytes = patient.medimgs[key]
            return medimgbytes, 200
    error_message = "med image not found"
    return error_message, 400


if __name__ == '__main__':
    init_server()
    app.run(host="0.0.0.0", port=5001)
