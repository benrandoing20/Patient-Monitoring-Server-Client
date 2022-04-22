import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from PIL import Image, ImageTk

import ecg_cont_processor as ecg
import matplotlib.pyplot as plt
import base64

ecg_b64 = ""
medIm_b64 = ""
hr = 0


def convert_file_to_b64_string(filename):
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string


def verify_GUI_inputs(input_id):
    try:
        id_integer = int(input_id)
    except ValueError:
        return False
    return id_integer


def verify_GUI_name_input(input_name):
    is_str = isinstance(input_name, str)
    return is_str


def is_name_empty(input_name):
    if input_name == "Enter a name here":
        input_name = ""
    return input_name


def main_window():
    """Creates and runs a GUI for the patient database

    This function creates a window that allows a user to enter patient
    information for eventual upload to a health database server. Entries
    on the GUI include patient name, medical record number, ECG data
    file, and a medical image file.

    """

    def ok_cmd():
        from patient_db_client import upload_patient_data_to_server
        # from client_design import upload_patient_data_to_server
        # print("Here is the data")
        entered_name = name_entry.get()
        # print("Name: {}".format(entered_name))
        entered_id = id_entry.get()
        # print("ID: {}".format(entered_id))
        entered_medical_image = medIm_b64
        # print(entered_medical_image)
        entered_ecg_image = ecg_b64
        entered_hr = hr
        # print("HR: {}".format(entered_hr))
        patient_number = verify_GUI_inputs(entered_id)
        patient_name = verify_GUI_name_input(entered_name)
        if patient_number is False:
            status_label.configure(text="Patient id must be an integer")
            return
        if patient_name is False:
            status_label.configure(text="Patient name must be an string")
            return
        out_name = is_name_empty(entered_name)
        status_string = upload_patient_data_to_server(entered_id,
                                                      out_name,
                                                      entered_medical_image,
                                                      entered_ecg_image,
                                                      entered_hr)
        status_label.configure(text="Push Successful")

    def image_cmd():
        try:
            image_labelMed.destroy()
        except NameError:
            pass
        # nonlocal tk_image
        filename = filedialog.askopenfilename()
        if filename == "":
            return
        pil_image_raw = Image.open(filename)
        pil_image = pil_image_raw.resize((200, 200))
        tk_image = ImageTk.PhotoImage(pil_image)
        create_image_labels_Med()
        image_labelMed.configure(image=tk_image)
        image_labelMed.image = tk_image
        global medIm_b64
        medIm_b64 = convert_file_to_b64_string(filename)

    def ecg_cmd():
        try:
            image_label.destroy()
        except NameError:
            pass
        # nonlocal tk_image
        filename = filedialog.askopenfilename()
        if filename == "":
            return
        time, voltage = ecg.analyze_data_file(filename)
        plt.close()
        plt.plot(time, voltage)
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.savefig("current_ecg.jpg")
        metrics = ecg.create_out_dict(time, voltage)
        heart_rate = int(metrics['mean_hr_bpm'])

        # HR Indicator
        hr_label.configure(text=str(heart_rate))
        global hr
        hr = heart_rate

        # ECG Image Display

        pil_image_raw = Image.open("current_ecg.jpg")
        pil_image = pil_image_raw.resize((200, 200))
        create_image_labels()
        tk_image = ImageTk.PhotoImage(pil_image)
        image_label.configure(image=tk_image)
        image_label.image = tk_image
        global ecg_b64
        ecg_b64 = convert_file_to_b64_string("current_ecg.jpg")

    def create_image_labels():
        # ECG Image
        global image_label
        image_label = ttk.Label(root)
        image_label.grid(column=5, row=2, rowspan=10)

    def create_image_labels_Med():
        # Medical Image
        global image_labelMed
        image_labelMed = ttk.Label(root)
        image_labelMed.grid(column=3, row=2, rowspan=10)

    def clear_cmd():
        name_entry.set("Enter a name here")
        id_entry.set("Enter medical record number")
        status_label.configure(text="Status")
        hr_label.configure(text="No ECG Selected")
        try:
            image_label.destroy()
        except NameError:
            pass
        try:
            image_labelMed.destroy()
        except NameError:
            pass
        global medIm_b64
        medIm_b64 = ""
        global ecg_b64
        ecg_b64 = ""
        global hr
        hr = 0

        return

    # Create root/base window
    root = tk.Tk()
    root.title("Health Database")
    root.geometry("1400x400")

    ttk.Label(root, text="Patient Input Database").grid(column=0, row=0,
                                                        columnspan=2,
                                                        sticky='w')

    # Patient Name Entry
    ttk.Label(root, text="Name:").grid(column=0, row=1, sticky=tk.E)
    name_entry = tk.StringVar()
    name_entry.set("Enter a name here")
    ttk.Entry(root, width=40, textvariable=name_entry).grid(column=1, row=1,
                                                            sticky=tk.W)

    # Medical Record ID Entry
    ttk.Label(root, text="ID:").grid(column=0, row=2, sticky=tk.E)
    id_entry = tk.StringVar()
    id_entry.set("Enter medical record number")
    ttk.Entry(root, textvariable=id_entry).grid(column=1, row=2, sticky=tk.W)

    # Buttons
    ttk.Button(root, text="Push", command=ok_cmd).grid(column=2, row=20)
    ttk.Button(root, text="Choose Medical Image", command=image_cmd).grid(
        column=3, row=20)
    ttk.Button(root, text="Choose ECG Data File", command=ecg_cmd).grid(
        column=5, row=20)
    ttk.Button(root, text="Clear", command=clear_cmd).grid(
        column=6, row=20)

    # Status Indicator
    status_label = ttk.Label(root, text="Status")
    status_label.grid(column=8, row=23, sticky=tk.W)

    # HR Label
    ttk.Label(root, text="ECG Heart Rate:").grid(column=0, row=5,
                                                 sticky=tk.W)
    hr_label = ttk.Label(root, text="No ECG Selected")
    hr_label.grid(column=1, row=5, sticky=tk.W)

    # Start GUI
    root.mainloop()


if __name__ == '__main__':
    main_window()
