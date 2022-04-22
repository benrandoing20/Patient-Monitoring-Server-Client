import requests

# local server:
# server = "http://127.0.0.1:5000"

# deployment to VM
server = "http://vcm-25826.vm.duke.edu:5001"


def download_mhrnumbers():
    """Downloads jsonified string of all mhr numbers in db

    This function calls the flask route /get_ids, which
    downloads all of the mhr numbers stored in the MongoDB
    patient database.

    :returns: string containing the list of all stored
    mhr numbers
    """
    r = requests.get(server + "/get_ids")
    mhrno_json = r.text
    return mhrno_json


def download_patient_info(mhrno):
    """Downloads patient info for given mhr number

    This function performs a get request that retrieves
    a jsonified dictionary of patient information for a
    specific mhr number. Retrieves patient name, latest
    heart rate, latest ecg image, latest ecg timestamp.

    :param mhrno: int medical health record number

    :returns: jsonified dict containing necessary information
    """
    r = requests.get(server + "/get_patient_info/{}".format(mhrno))
    patinfo_json = r.text
    return patinfo_json


def download_patient_ecg_times(mhrno):
    """Downloads timestamps when ecg imgs were uploaded

    This function performs a get request that retrieves
    a jsonified list of timestamps at which ecg imgs were
    uploaded for a specific mhr number.

    :param mhrno: int medical health record number

    :returns: jsonified list of strings containing timestamps
    """
    r = requests.get(server + "/get_ecg_times/{}".format(mhrno))
    ecgtimes_json = r.text
    return ecgtimes_json


def download_selected_ecg_img(mhrno, tstmpindex):
    """Downloads selected ecg img

    This function performs a get request that retrieves
    the ecg img specified by the selected timestamp for a
    specific mhr number.

    :param mhrno: int medical health record number
    :param ecgimgindex: int index of selected timestamp, which
    corresponds to the index of a stored ecg img file on the
    mongoDB database

    :returns: jsonified b64string image file
    """
    r = requests.get(server + "/get_ecg_"
                              "img/{}/{}".format(mhrno,
                                                 tstmpindex))
    ecgimgbytes = r.text
    return ecgimgbytes


def download_patient_med_times(mhrno):
    """Downloads timestamps when med imgs were uploaded

    This function performs a get request that retrieves
    a jsonified list of timestamps at which med imgs were
    uploaded for a specific mhr number.

    :param mhrno: int medical health record number

    :returns: jsonified list of strings containing timestamps
    """
    r = requests.get(server + "/get_med_times/{}".format(mhrno))
    medtimes_json = r.text
    return medtimes_json


def download_selected_med_img(mhrno, tstmpindex):
    """Downloads selected med img

    This function performs a get request that retrieves
    the med img specified by the selected timestamp for a
    specific mhr number.

    :param mhrno: int medical health record number
    :param medimgindex: int index of selected timestamp, which
    corresponds to the index of a stored med img file on the
    mongoDB database

    :returns: jsonified b64string image file
    """
    r = requests.get(server + "/get_med_"
                              "img/{}/{}".format(mhrno,
                                                 tstmpindex))
    medimgbytes = r.text
    return medimgbytes
