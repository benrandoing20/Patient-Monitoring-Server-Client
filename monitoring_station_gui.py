import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PIL import Image, ImageTk

from mhrpatient_info import Patient
from pymodm import connect
from pymongo import MongoClient

import base64

from monitoring_station_client import (download_mhrnumbers,
                                       download_patient_info,
                                       download_patient_ecg_times,
                                       download_selected_ecg_img,
                                       download_patient_med_times,
                                       download_selected_med_img)

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


def process_mhrnumbers(json_list):
    """Downloads all medical health record numbers stored

    This function parses and processes the json-encoded string
    to create a list of integer medical health record numbers.

    :param json_list: jsonified list of medical health record
    numbers

    :returns: List of int medical health record numbers
    """
    mhrno_json_nobrackets = json_list[1:-2]
    mhrno_separated = mhrno_json_nobrackets.split(",")
    if mhrno_separated[0] == "":
        return ["No patients in DB yet!"]
    mhrno_list = [int(i) for i in mhrno_separated]
    return mhrno_list


def jsonified_dict_parser(jsonified_dict):
    """Converts a jsonified dictionary into a python dict

    This function takes a jsonified dictionary (a python
    dictionary that has been converted into one big string)
    and converts it back into a workable python dictionary.

    :param jsonified_dict: Dictionary turned into one
    large string

    :returns: dict containing all expected keys and their
    respective values
    """
    jsonified_dict_nobrackets = jsonified_dict[1:-2]
    nobrackets_split = jsonified_dict_nobrackets.split(",")
    dict_fixed = {}
    for entry in nobrackets_split:
        entry_split = entry.split(":", 1)
        key = (entry_split[0])[1:-1]
        try:
            value = int(entry_split[1])
        except Exception:
            value = (entry_split[1])[1:-1]
        dict_fixed[key] = value
    return dict_fixed


def process_tstmp(json_list):
    """Downloads all timestamps stored

    This function parses and processes the json-encoded string
    to create a list of string timestamps.

    :param json_list: jsonified list of timestamps

    :returns: List of string timestamps, but will need to
    remove the placeholder "e" entry.
    """
    tstmp_json_nobrackets = json_list[1:-2]
    tstmp_separated = tstmp_json_nobrackets.split(",")
    if len(tstmp_separated) == 1:
        return ["No images uploaded yet!"]
    tstmp_liste = [i[1:-1] for i in tstmp_separated]
    return tstmp_liste


def convert_b64_to_image(b64string, filename):
    """Converts a b64 string into an image file

    This function receives a b64 encoded string and converts
    it into a .jpg file. It saves the file as "temp.jpg".

    :returns: Does not return anything
    """
    image_bytes = base64.b64decode(b64string)
    with open(filename, "wb") as out_file:
        out_file.write(image_bytes)
    return


def main_window():
    """Creates and runs a GUI for the monitoring station

    This function creates a window that allows a user to display
    information for a specific patient medical health record
    number. Entries on the GUI include:
        - Dropdowns to select medical record number,
          ecg images, and medical images
        - Display windows for selected images
        - Buttons to save images
        - Display windows for patient ID, patient name,
          and heart rate

    :returns: Does not return anything
    """

    def confirm_cmd():
        """Obtains the selected MHR number and displays its summary

        This function runs when the user clicks on the "Confirm"
        button next to the MHR number drop down box. It gets the
        entered data from the drop down, retrieves the patient name,
        latest ECG image, latest measured heart rate, and timestamp
        of these two, and displays them on the GUI.
        """
        selected_mhrno = mhrnumber.get()
        if selected_mhrno == "No patients in DB yet!":
            status_label.configure(text="No patients in database yet!")
            return
        if selected_mhrno == "":
            status_label.configure(text="Please select a medical health"
                                        " record number!")
            return
        patinfo_json = download_patient_info(selected_mhrno)
        patient_dict = jsonified_dict_parser(patinfo_json)
        patient_name = patient_dict["name"]
        last_hr = patient_dict["last_hr"]
        latest_ecg = patient_dict["latest_ecg"]
        latest_ecg_tstamp = patient_dict["latest_ecg_tstamp"]
        ecg_tstamp_dropdown.set("")
        med_tstamp_dropdown.set("")
        latestecg_filename_entry.set('Desired Filename ("filename.jpg")')
        reset_ecg_select()
        reset_med_select()
        display_ecgimg()
        display_medimg()
        patientname.configure(text=patient_name)
        tstamp_latest_msg = ("ECG image uploaded at {}").\
            format(latest_ecg_tstamp)
        latest_tstamp.configure(text=tstamp_latest_msg)
        mhrno_selected.configure(text=selected_mhrno)
        hr_last_msg = ("| The calculated heart rate for"
                       " this ECG file is {} bpm |").format(last_hr)
        latest_hr.configure(text=hr_last_msg)

    def display_mhrno():
        """Updates the mhrno selection dropdown box

        This method will retrieve the mhr numbers from the
        mongoDB database. It will then update the mhrnumber
        selection dropdown box with these timestamps.
        """
        json_mhrno = download_mhrnumbers()
        mhrnumber_dropdown["values"] = process_mhrnumbers(json_mhrno)
        mhrnumber_dropdown.state(['readonly'])
        # Update list of MHR numbers every 5 seconds
        root.after(5000, display_mhrno)

    def display_ecgimg():
        """Updates ecgimg selection dropdown box

        This method is only intended to be called within the
        confirm_cmd method or for live updates.
        It will retrieve the timestamps
        at which ecg images were uploaded. It will then
        update the ecg image selection dropdown box with
        these timestamps.
        """
        selected_mhrno = mhrnumber.get()
        if selected_mhrno == "No patients in DB yet!":
            status_label.configure(text="No patients in database yet!")
            return
        if selected_mhrno == "":
            status_label.configure(text="Please select a medical health"
                                        " record number!")
            return
        patinfo_json = download_patient_info(selected_mhrno)
        patient_dict = jsonified_dict_parser(patinfo_json)
        ecg_tstmp_json = download_patient_ecg_times(selected_mhrno)
        ecg_tstmps = process_tstmp(ecg_tstmp_json)
        patient_name = patient_dict["name"]
        last_hr = patient_dict["last_hr"]
        latest_ecg = patient_dict["latest_ecg"]
        latest_ecg_tstamp = patient_dict["latest_ecg_tstamp"]
        if latest_ecg == "e":
            status_label.configure(text="No ECG image uploaded yet!")
            latest_ecg = b64string_test
            last_hr = "n/a"
            latest_ecg_tstamp = "n/a"
            ecg_tstamp_dropdown["values"] = ("Empty")
            ecg_tstamp_dropdown.state(['readonly'])
        else:
            convert_b64_to_image(latest_ecg, "temp.jpg")
            ecg_latest_image_raw = Image.open("temp.jpg")
            ecg_latest_image = ecg_latest_image_raw.resize((200, 200))
            ecg_latest_tk_image = ImageTk.PhotoImage(ecg_latest_image)
            ecg_latest_image_label.image = ecg_latest_tk_image
            ecg_latest_image_label.configure(image=ecg_latest_tk_image)
            status_label.configure(text="Patient info updated!")
            ecg_tstamp_dropdown["values"] = ecg_tstmps[1:len(ecg_tstmps)]
            ecg_tstamp_dropdown.state(['readonly'])
        # Update list of ECG images every 5 seconds
        root.after(5000, display_ecgimg)

    def save_latest_ecg():
        """Saves the latest ecg image that is displayed

        This function runs when the "save" button underneath
        the most recent ecg img window is clicked. This function
        will convert b64 string to image file and save to local
        folder. File extension must be specified when saving.
        """
        selected_mhrno = mhrnumber.get()
        patinfo_json = download_patient_info(selected_mhrno)
        patient_dict = jsonified_dict_parser(patinfo_json)
        latest_ecg = patient_dict["latest_ecg"]
        if latest_ecg == "e":
            status_label.configure(text="No ECG files have been uploaded yet!")
            return
        filename = latestecg_filename_entry.get()
        try:
            jpeg = filename.split(".")
        except Exception:
            status_label.configure(text='Please include file'
                                        ' extension in filename!')
            return
        if jpeg[-1] != "jpg":
            status_label.configure(text='Please specify filename'
                                        ' as "filename.jpg"')
            return
        convert_b64_to_image(latest_ecg, filename)
        status_label.\
            configure(text=("Latest ECG stored as {}").format(filename))
        latestecg_filename_entry.set('Desired Filename ("filename.jpg")')

    def confirm_ecg_select():
        """Displays the selected ecg image

        This function executes upon user clicking the "Confirm"
        button adjacent to the ecg image selection dropdown. It
        will display the selected image in the display window
        below the dropdown box. It will also display the heart
        rate of that ecg image. This assumes that only one
        ecg img can be uploaded at one time.
        """
        selected_ecgtstmp = ecg_tstamp.get()
        if selected_ecgtstmp == "Empty" or selected_ecgtstmp == "":
            status_label.configure(text="No ECG images uploaded yet!")
            return
        selected_mhrno = mhrnumber.get()
        ecg_tstmp_json = download_patient_ecg_times(selected_mhrno)
        ecg_tstmps = process_tstmp(ecg_tstmp_json)
        ecg_imgindex = ecg_tstmps.index(selected_ecgtstmp)
        ecgimg_hr_json = download_selected_ecg_img(selected_mhrno,
                                                   ecg_imgindex)
        ecgimg_hr_dict = jsonified_dict_parser(ecgimg_hr_json)
        ecgimgbytes = ecgimg_hr_dict["image"]
        hr = ecgimg_hr_dict["hr"]
        convert_b64_to_image(ecgimgbytes, "temp1.jpg")
        ecg_select_image_raw = Image.open("temp1.jpg")
        ecg_select_image = ecg_select_image_raw.resize((200, 200))
        ecg_select_tk_image = ImageTk.PhotoImage(ecg_select_image)
        ecg_select_image_label.image = ecg_select_tk_image
        ecg_select_image_label.configure(image=ecg_select_tk_image)
        hr_select_msg = ("| The calculated heart rate for"
                         " this ECG file is {} bpm |").format(hr)
        hr_select_label.configure(text=hr_select_msg)
        status_label.\
            configure(text="Now displaying ecg img uploaded"
                           " at timestamp {}".format(selected_ecgtstmp))

    def reset_ecg_select():
        """Resets selected ecg image when new patient is chosen

        This function is only used within the confirm_cmd() function. It
        resets the timestamp-selected ecg image to default blue box. It
        also resets the hr report text below the image to default.
        """
        ecg_select_image_raw = Image.open("test_image1.jpg")
        ecg_select_image = ecg_select_image_raw.resize((200, 200))
        ecg_select_tk_image = ImageTk.PhotoImage(ecg_select_image)
        ecg_select_image_label.image = ecg_select_tk_image
        ecg_select_image_label.configure(image=ecg_select_tk_image)
        hr_select_msg = ("| The calculated heart rate for"
                         " this ECG file is Empty bpm |")
        hr_select_label.configure(text=hr_select_msg)
        selectecg_filename_entry.set('Desired Filename ("filename.jpg")')

    def save_select_ecg():
        """Saves the selected ecg image that is displayed

        This function runs when the "save" button underneath the
        timestamp-selected ecg img window is clicked. This function
        will convert b64 string to image file and save to local folder.
        File extension must be specified when saving.
        """
        selected_mhrno = mhrnumber.get()
        selected_ecgtstmp = ecg_tstamp.get()
        if selected_ecgtstmp == "Empty" or selected_ecgtstmp == "":
            status_label.configure(text="No ECG image selected yet!")
            return
        ecg_tstmp_json = download_patient_ecg_times(selected_mhrno)
        ecg_tstmps = process_tstmp(ecg_tstmp_json)
        ecg_imgindex = ecg_tstmps.index(selected_ecgtstmp)
        ecgimg_hr_json = download_selected_ecg_img(selected_mhrno,
                                                   ecg_imgindex)
        ecgimg_hr_dict = jsonified_dict_parser(ecgimg_hr_json)
        ecgimgbytes = ecgimg_hr_dict["image"]
        filename = selectecg_filename_entry.get()
        try:
            jpeg = filename.split(".")
        except Exception:
            status_label.configure(text='Please include file'
                                        ' extension in filename!')
            return
        if jpeg[-1] != "jpg":
            status_label.configure(text='Please specify filename'
                                        ' as "filename.jpg"')
            return
        convert_b64_to_image(ecgimgbytes, filename)
        status_label.\
            configure(text=("ECG uploaded"
                            " at {} stored as {}").format(selected_ecgtstmp,
                                                          filename))
        selectecg_filename_entry.set('Desired Filename ("filename.jpg")')

    def display_medimg():
        """Updates medimg selection dropdown box

        This method is only intended to be called within the
        confirm_cmd method or for live updates.
        It will retrieve the timestamps
        at which medical images were uploaded. It will then
        update the medical image selection dropdown box with
        these timestamps.
        """
        selected_mhrno = mhrnumber.get()
        if selected_mhrno == "No patients in DB yet!":
            status_label.configure(text="No patients in database yet!")
            return
        if selected_mhrno == "":
            status_label.configure(text="Please select a medical health"
                                        " record number!")
            return
        med_tstmp_json = download_patient_med_times(selected_mhrno)
        med_tstmps = process_tstmp(med_tstmp_json)
        if len(med_tstmps) == 1:
            latest_ecg = b64string_test
            med_tstamp_dropdown["values"] = ("Empty")
            med_tstamp_dropdown.state(['readonly'])
        else:
            med_tstamp_dropdown["values"] = med_tstmps[1:len(med_tstmps)]
            med_tstamp_dropdown.state(['readonly'])
        # Update list of medical images every 5 seconds
        root.after(5000, display_medimg)

    def confirm_med_select():
        """Displays the selected med image

        This function executes upon user clicking the "Confirm"
        button adjacent to the med image selection dropdown. It
        will display the selected image in the display window
        below the dropdown box. This assumes that only one
        med img can be uploaded at one time.
        """
        selected_medtstmp = med_tstamp.get()
        if selected_medtstmp == "Empty" or selected_medtstmp == "":
            status_label.configure(text="No med images uploaded yet!")
            return
        selected_mhrno = mhrnumber.get()
        med_tstmp_json = download_patient_med_times(selected_mhrno)
        med_tstmps = process_tstmp(med_tstmp_json)
        med_imgindex = med_tstmps.index(selected_medtstmp)
        medimg_json = download_selected_med_img(selected_mhrno,
                                                med_imgindex)
        medimgbytes = medimg_json[1:-2]
        convert_b64_to_image(medimgbytes, "temp1.jpg")
        med_select_image_raw = Image.open("temp1.jpg")
        med_select_image = med_select_image_raw.resize((200, 200))
        med_select_tk_image = ImageTk.PhotoImage(med_select_image)
        med_select_image_label.image = med_select_tk_image
        med_select_image_label.configure(image=med_select_tk_image)
        status_label.\
            configure(text="Now displaying med img uploaded"
                           " at timestamp {}".format(selected_medtstmp))

    def reset_med_select():
        """Resets selected med image when new patient is chosen

        This function is only used within the confirm_cmd() function. It
        resets the timestamp-selected med image to default blue box.
        """
        med_select_image_raw = Image.open("test_image1.jpg")
        med_select_image = med_select_image_raw.resize((200, 200))
        med_select_tk_image = ImageTk.PhotoImage(med_select_image)
        med_select_image_label.image = med_select_tk_image
        med_select_image_label.configure(image=med_select_tk_image)
        selectmed_filename_entry.set('Desired Filename ("filename.jpg")')

    def save_select_med():
        """Saves the selected med image that is displayed

        This function runs when the "save" button underneath the
        timestamp-selected med img window is clicked. This function
        will convert b64 string to image file and save to local folder.
        File extension must be specified when saving.
        """
        selected_mhrno = mhrnumber.get()
        selected_medtstmp = med_tstamp.get()
        if selected_medtstmp == "Empty" or selected_medtstmp == "":
            status_label.configure(text="No med image selected yet!")
            return
        med_tstmp_json = download_patient_med_times(selected_mhrno)
        med_tstmps = process_tstmp(med_tstmp_json)
        med_imgindex = med_tstmps.index(selected_medtstmp)
        medimg_json = download_selected_med_img(selected_mhrno,
                                                med_imgindex)
        medimgbytes = medimg_json[1:-2]
        filename = selectmed_filename_entry.get()
        try:
            jpeg = filename.split(".")
        except Exception:
            status_label.configure(text='Please include file'
                                        ' extension in filename!')
            return
        if jpeg[-1] != "jpg":
            status_label.configure(text='Please specify filename'
                                        ' as "filename.jpg"')
            return
        convert_b64_to_image(medimgbytes, filename)
        status_label.\
            configure(text=("med uploaded"
                            " at {} stored as {}").format(selected_medtstmp,
                                                          filename))
        selectmed_filename_entry.set('Desired Filename ("filename.jpg")')

    def exit_cmd():
        """Closes GUI window upon click of "Exit" button

        When the user clicks on the "Exit" button, this function is
        run which closes the main root GUI window.
        """
        root.destroy()

    # Create window
    root = tk.Tk()
    root.title("Monitoring Station")
    root.geometry("1400x600")

    ttk.Label(root, text="Patient Monitoring Station").grid(
        column=2, row=0, columnspan=2)

    # Patient MHR Number Dropdown
    ttk.Label(root, text="Select from stored"
                         " patient medical record numbers").grid(column=0,
                                                                 row=1,
                                                                 columnspan=2)
    mhrnumber = tk.StringVar()
    mhrnumber_dropdown = ttk.Combobox(root, textvariable=mhrnumber)
    mhrnumber_dropdown.grid(column=0, row=2)
    # Pull IDs from MongoDB patient collection
    json_mhrno = download_mhrnumbers()
    mhrnumber_dropdown["values"] = process_mhrnumbers(json_mhrno)
    mhrnumber_dropdown.state(['readonly'])

    # Button to confirm patient MHR number selection
    ttk.Button(root, text="Confirm", command=confirm_cmd).grid(column=1, row=2)

    # MHR Label
    ttk.Label(root, text="Medical Health Record Number").grid(column=0,
                                                              row=4)
    # MHR Display Box
    mhrnumber_selected = "Empty"  # Takes whatever ID is selected
    mhrno_selected = ttk.Label(root, text=mhrnumber_selected)
    mhrno_selected.grid(column=0, row=5)

    # Name Label
    ttk.Label(root, text="Patient Name").grid(column=1, row=4)

    # Name Display Box
    patientname = ttk.Label(root, text="Empty")
    patientname.grid(column=1, row=5)

    # Timestamp of latest ECG image
    tstamp_latest = "Empty"  # Retrieve last timestamp entry
    tstamp_latest_msg = ("ECG image uploaded at {}").format(tstamp_latest)
    latest_tstamp = ttk.Label(root, text=tstamp_latest_msg)
    latest_tstamp.grid(column=2, row=4, columnspan=2)

    # Latest ECG image
    ecg_latest_image_raw = Image.open("test_image1.jpg")
    ecg_latest_image = ecg_latest_image_raw.resize((200, 200))
    ecg_latest_tk_image = ImageTk.PhotoImage(ecg_latest_image)
    ecg_latest_image_label = ttk.Label(root, image=ecg_latest_tk_image)
    ecg_latest_image_label.image = ecg_latest_tk_image
    ecg_latest_image_label.grid(column=2, row=5, rowspan=10, columnspan=2)

    # HR of latest ECG image
    hr_latest = "Empty"  # Retrieve last HR entry
    hr_latest_msg = ("| The calculated heart rate for"
                     " this ECG file is {} bpm |").format(hr_latest)
    latest_hr = ttk.Label(root, text=hr_latest_msg)
    latest_hr.grid(column=2, row=20, columnspan=2)

    # Button to save latest ECG image
    ttk.Button(root, text="Save Image", command=save_latest_ecg).\
        grid(column=3, row=21, sticky=tk.W)

    # Text entry box to specify desired filename of save image
    latestecg_filename_entry = tk.StringVar()
    latestecg_filename_entry.set('Desired Filename ("filename.jpg")')
    ttk.Entry(root, width=30, textvariable=latestecg_filename_entry).\
        grid(column=2, row=21)

    # ECG image timestamp dropdown
    ttk.Label(root, text="Select from stored ECG"
                         " file upload timestamps").grid(column=4,
                                                         row=3,
                                                         columnspan=2)
    ecg_tstamp = tk.StringVar()
    ecg_tstamp_dropdown = ttk.Combobox(root, textvariable=ecg_tstamp)
    ecg_tstamp_dropdown.grid(column=4, row=4)
    # Pull timestamps from MongoDB patient collection
    ecg_tstamp_dropdown["values"] = ("Empty")
    ecg_tstamp_dropdown.state(['readonly'])

    # Selected ECG image
    ecg_select_image_raw = Image.open("test_image1.jpg")
    ecg_select_image = ecg_select_image_raw.resize((200, 200))
    ecg_select_tk_image = ImageTk.PhotoImage(ecg_select_image)
    ecg_select_image_label = ttk.Label(root, image=ecg_select_tk_image)
    ecg_select_image_label.image = ecg_select_tk_image
    ecg_select_image_label.grid(column=4, row=5, columnspan=2,
                                rowspan=10)

    # Button to confirm ECG image selection
    ttk.Button(root, text="Confirm", command=confirm_ecg_select).\
        grid(column=5, row=4, sticky=tk.W)

    # HR of selected ECG image
    hr_select = "Empty"  # Retrieve last HR entry
    hr_select_msg = ("| The calculated heart rate for"
                     " this ECG file is {} bpm |").format(hr_select)
    hr_select_label = ttk.Label(root, text=hr_select_msg)
    hr_select_label.grid(column=4, row=20, columnspan=2)

    # Button to save selected ECG image
    ttk.Button(root, text="Save Image", command=save_select_ecg).\
        grid(column=5, row=21, sticky=tk.W)

    # Text entry box to specify desired filename of save image
    selectecg_filename_entry = tk.StringVar()
    selectecg_filename_entry.set('Desired Filename ("filename.jpg")')
    ttk.Entry(root, width=30, textvariable=selectecg_filename_entry).\
        grid(column=4, row=21)

    # Medical image timestamp dropdown
    ttk.Label(root, text="Select from stored"
                         " image upload timestamps").grid(column=6,
                                                          row=3,
                                                          columnspan=2)
    med_tstamp = tk.StringVar()
    med_tstamp_dropdown = ttk.Combobox(root, textvariable=med_tstamp)
    med_tstamp_dropdown.grid(column=6, row=4)
    # Pull timestamps from MongoDB patient collection
    med_tstamp_dropdown["values"] = ("Empty")
    med_tstamp_dropdown.state(['readonly'])

    # Selected med image
    med_select_image_raw = Image.open("test_image1.jpg")
    med_select_image = med_select_image_raw.resize((200, 200))
    med_select_tk_image = ImageTk.PhotoImage(med_select_image)
    med_select_image_label = ttk.Label(root, image=med_select_tk_image)
    med_select_image_label.image = med_select_tk_image
    med_select_image_label.grid(column=6, row=5, rowspan=10,
                                columnspan=2)

    # Button to confirm med image selection
    ttk.Button(root, text="Confirm", command=confirm_med_select).\
        grid(column=7, row=4, sticky=tk.W)

    # Button to save selected med image
    ttk.Button(root, text="Save Image", command=save_select_med).\
        grid(column=7, row=21)

    # Text entry box to specify desired filename of save image
    selectmed_filename_entry = tk.StringVar()
    selectmed_filename_entry.set('Desired Filename ("filename.jpg")')
    ttk.Entry(root, width=30, textvariable=selectmed_filename_entry).\
        grid(column=6, row=21)

    # Exit button
    ttk.Button(root, text="Exit", command=exit_cmd).grid(column=0, row=6,
                                                         columnspan=2)

    # Status indicator
    status_label = ttk.Label(root, text="Status")
    status_label.grid(column=0, row=20, sticky=tk.W)

    # Update list of MHR numbers, and if a MHR number is selected replace
    # outdated patient info with updated patient info (new latest images
    # and heart rate)

    # Update list of MHR numbers every 5 seconds
    root.after(5000, display_mhrno)

    # Update list of ECG images every 5 seconds
    root.after(5000, display_ecgimg)

    # Update list of medical images every 5 seconds
    root.after(5000, display_medimg)

    # Start GUI
    root.mainloop()


if __name__ == "__main__":
    main_window()
