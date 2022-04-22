import requests

# local server:
# server = "http://127.0.0.1:5000"

# deployment to VM
server = "http://vcm-25826.vm.duke.edu:5001"


def upload_patient_data_to_server(medical_id, patient_name,
                                  medIm_b64, ecg_b64, heart_rate):
    new_patient = {"mhrnumber": medical_id, "name": patient_name,
                   "medimgbytes": medIm_b64,
                   "ecgimgbytes": ecg_b64, "hr": heart_rate}
    r = requests.post(server + "/patient/dataupload", json=new_patient)
    return r.text


# r = requests.get(server+"/get_ids")
# print(r.status_code)
# print(r.text)
#
#
r = requests.get(server+"/get_patient_info/1235")
print(r.status_code)
print(r.text)

# r = requests.get(server+"/get_ecg_times/123")
# print(r.status_code)
# print(r.text)
