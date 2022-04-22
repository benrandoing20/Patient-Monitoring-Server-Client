# Heart Rate Sentinel Server Assignment

[![Pytest with Pycodestyle](https://github.com/BME547-Spring2022/final-project-gitrepoed/actions/workflows/pytest_runner.yml/badge.svg)](https://github.com/BME547-Spring2022/final-project-gitrepoed/actions/workflows/pytest_runner.yml)

### Team gitRepoed 
### Ben Randoing and Josh Li

phone: (214) 356-9043, (678) 313-0473

email: bar39@duke.edu, jyl23@duke.edu

## Video Demo Zoom Cloud Recording
https://duke.zoom.us/rec/share/KgAKkQIlX0_cWgJefY6liwJmdewEYfo_E-KS4NvtdiKudLc39hDAAL0Yp-C0xMir.WQI-_CZsc3HESRzQ?startTime=1649988655000

## Purpose

The purpose of the combined GUI and server modules is to implement a 
patient database. The database can take patient information such as the 
patient medical record, patient name, ecg data, and medical image 
information from one GUI, send this information to a server which saves 
each patient in a non-sql MondgoDB database. Then, the information may be 
pulled from a second GUI. 

Having a patient database in the modern medical climate is essential. 
Doctors are often overwhelmed and need a quick, friendly userface to input 
patient information. This database will take such information and provide 
informational outputs that are easy to digest.

## Notable Imported Packages

base64: The base64 system uses 64 characters to represent numbers. The 
numeric quantification of a jpg image may be converted to a base64 string 
that is saved in the MongoDB database. 

pymodym: The package imported to communicate with the MongoDB database

flask: The flask framework is imported to create a specific flask API 
server to interact with the two GUIs and to send information to the MongoDB 
database. 

## Server API

The server is constantly running at URL: `vcm-25826.vm.duke.edu:5001`

### POST URL/patient/dataupload

#### Purpose:
Uploads patient data to the mongoDB database. It must receive a JSON-encoded string
that looks like the following:

`patient_dict = {"mhrnumber": int, "name": str, "medimg": b64_string, "ecgimg": b64_string, "hr": int}`

- "mhrnumber": int - patient's medical health record ID number. REQUIRED PARAMETER  
- "name": str - patient's name, generally in format LastName.FirstName. OPTIONAL PARAMETER  
- "medimgbytes": b64_string - string variable containing the image bytes encoded as a base64 string. OPTIONAL PARAMETER  
- "ecgimgbytes": b64_string - string variable containing the image bytes encoded as a base64 string. OPTIONAL PARAMETER  
- "hr": int - the heart rate calculated from the provided ecgimg

#### Returns:
str summarizing what info was uploaded and int 200 if upload is successful, or str error message and int error code if
upload is not successful.

#### How to Call:
`r = requests.post(URL + "/patient/dataupload", json=patient_dict)`

### GET URL/get_ids

#### Purpose:
Retrieves all current medical record numbers in the health database.

#### Returns:
patient medical record number list and status code 200 if
successful.

#### How to Call:
`r = requests.get(URL + "/get_ids")`
This prompt will automatically get the list of patient medical record numbers

### GET URL/get_patient_info/<patient_id>

#### Purpose:
Retrieves the name, most recent ecg data image, and most recent heart_rate 
associate with a specific patient. 

#### Returns:
string patient name, b64 string ecg image, heart rate int,
and associated timestamp string with status code 200 if successful.
A string error message and status code of 400 are returned if the
patient_id is not an int or not found within the MongoDB database.

#### How to Call:
`r = requests.get(URL + "/get_patient_info/<patient_id>")`
where <patient_id> is an integer corresponding to the desired medical health record number

### GET URL/get_ecg_times/<patient_id>

#### Purpose:
Retrieves the ecg time stamps for a specific patient.

#### Returns:
list ecg timestamps with status code 200 if successful. A
string error message and status code of 400 are returned if the
patient_id is not an int or not found within the MongoDB database

#### How to Call:
`r = requests.get(URL + "/get_ecg_times/<patient_id>")`
where <patient_id> is an integer corresponding to the desired medical health record number

### GET URL/get_ecg_img/<patient_id>/<ecg_img_index>

#### Purpose:
Retrieves the specified ECG image and heart rate associated with that image for a given patient.

#### Returns:
status code 200 and jsonified dictionary containing b64 string image and hr if successful, error message
and status code 400 if not successful.

#### How to Call:
`r = requests.post(URL + "/get_ecg_img/<patient_id>/<ecg_img_index>")`  
where <patient_id> is an integer corresponding to the desired medical health record number, and <ecg_img_index>
is the index of the selected timestamp in the list of ecg image upload timestamps. This index will correspond to
the number automatically appended to each ecg image filename when uploaded.

### GET URL/get_med_times/<patient_id>

#### Purpose:
Retrieves the list of medical image upload timestamps for the specified medical health record number

#### Returns:
jsonified list of timestamps with status code 200 if successful. A string error message and status code of 400 are
returned if unsuccessful

#### How to Call:
`r = requests.get(URL + "/get_med_times/<patient_id>")`  
where <patient_id> is an integer corresponding to the desired medical health record number.

### GET URL/get_med_img/<patient_id>/<med_img_index>

#### Purpose:
Retrieves the specified medical image for a given patient.

#### Returns:
status code 200 and jsonified b64 string image if successful, error message
and status code 400 if not successful.

#### How to Call:
`r = requests.get(URL + "/get_med_img/<patient_id>/<med_img_index>")`  
where <patient_id> is an integer corresponding to the desired medical health record number, and <med_img_index>
is the index of the selected timestamp in the list of medical image upload timestamps. This index will correspond to
the number automatically appended to each medical image filename when uploaded.

## Repository Setup and Starting the Server 

This repository includes the software needed to run a simple patient health 
database, built using the Flask framework. 
The server should already be running on a Duke personal Ubuntu18 virtual machine with hostname and port:  
`vcm-25826.vm.duke.edu:5001` so no set up will be required to activate the server. However, if you wish to interact with the server locally, you must activate the server as follows:
1. Open a Git Bash window
2. Clone the git repository by typing the following in the terminal command 
   line:
    - `git clone <ssh>` where ssh may be copied from the repository on 
      github.com
3. Access the directory in which the heart-rate-sentinel-server-gitrepoed git repository is located
4. Activate a python virtual environment by typing the following into the terminal command line:
    - `python -m venv myvenv`
    - `source myvenv/Scripts/activate`(replace Scripts with `bin` if 
      operating on macOS)
5. Install the requirements.txt file by typing the following in the command line:  
    - `pip install -r requirements.txt`
6. Uncomment the local server address and comment the VM address at the top of `monitoring_station_client.py`
   and `patient_db_client.py`
7. At the very bottom of `patient_monitoring_sys_server.py`, change the `app.run(host='0.0.0.0', port=5001)`
   to `app.run()`
8. Save your edits
9. Type the following in the command line:  
    - `python patient_monitoring_sys_server.py`

## Running the Patient-Side GUI
1. Run patient_side_gui.py by typing the following in the command line:
   - `python patient_side_gui.py`
2. You must add a medical record number numeric quantity without decimals 
   to be able to push the data.
3. You may also add a patient name, select an ecg data file, and select a 
   medical image prior to pushing the patient to the database.
4. The medical image and ecg data will plot on the GUI after selection and 
   can be changed. 
5. The heart_rate calculated from ecg_cont_processor.py will be displayed.
6. At any point selecting the clear button will reset the GUI.
7. After pushing data, a status label will say "Push Successful". At this 
   point you may alter the information in the GUI if desired and push again.

## How the Patient-Side GUI Works

The Patient Side GUI implements the functionality of tkinter to have entry 
boxes for a patient name and patient medical record number. Additionally, 
ecg voltage/time data files may be selected using a push button. Medical 
images may also be selected. A clear button will remove and reset the 
screen, and the push button will send all medical information to the 
MongoDB database. 

## Running Monitoring Station GUI 

1. Run monitoring_station_gui.py by typing the following in the command line:
   - `python monitoring_station_gui.py`
2. Click the dropdown box and select your desired medical health record number. Press the
   "Confirm" button to confirm your selection.
   - The medical health record number dropdown box in the upper left corner of the
     gui will be updated every five seconds with any new medical health record numbers
     added to the database.
3. After pressing confirm, the GUI will update the most recent ecg data (the left most
   image column) with the most recent ecg image, ecg image upload timestamp, and hr uploaded
   to that patient medical health record number. The mhr number and name text boxes
   below the mhr number dropdown box.
4. Clicking the mhr number confirmation button will also update the list of all ecg img upload
   timestamps in the dropdown in the middle image column, and it will also update the list of
   all medical image upload timestamps in the dropdown in the right most image column. When
   on the selected mhrnumber GUI screen, the GUI will automatically update the
   timestamp lists with any newly uploaded images every 5 seconds
5. To display an image, select the desired timestamp in the dropdown and then click the
   "Confirm" button directly to the right of the dropdown window.
6. To save the displayed image, type the desired filename in the format "filename.jpg"
   into the filename box below the image window, and then click the "Save"
   button directly to the right of the filename box.
7. Switching to a different mhrnumber simply entails selecting another mhrnumber
   from the dropdown box and clicking the "Confirm" button directly to the right.
   This will repopulate or clear the image columns appropriately and automatically.
- Note: The default image displayed is a blue box to signify empty image window.
- Note: The latest ecg img, timestamp, and hr will live update every 5 seconds to show
   the latest ecg img data.

## How the Monitoring Station GUI Works

The Monitoring Station GUI implements the functionality of tkinter to have:
- Dropdown boxes for mhrnumber, ecg image timestamp, and medical image timestamp selection
- Buttons to confirm selections, to save images locally, and to exit the GUI
- Text input windows to allow specification of filename to download the image to
- Text display windows to display timestamp, heart rate, mhrnumber, patient name, and status

# ECG Data Analysis Information 

## Peak Detection Module

The py-ecg-detectors module is imported to allow for the calling the 
Detectors class via "from ecgdetectors 
import Detectors". This module features multiple peak detector functions. 
The function implemented in this code is the two_average_detector function. 
This function takes in a voltage array and outputs the index values in said 
array at which an R peak occurs. 

## How the Code Defines and Identifies a Beat

The two_average_detectors function identifies the peak of the QRS wave to 
define the presence of a beat. The general approach involves three main 
steps: bandpass filtering, generating potential blocks, and thresholding. 
The pass band of the filter is 8-20 Hz. Additionally, the filter is a 
second-order Butterworth filter. The second component to the peak detection 
is generating potential blocks of peaks. Using two-moving averages, the 
onset and offset of a peak block is established assuming the normal QRS 
peak duration in a healthy adult is 100±20 ms. With a known sampling 
frequency, the quantity of data points of each expected QRS peak may be 
identified. For example a frequency of 360 Hz would indicate an estimated 
QRS wave width of at least 44 data points. Finally, a threshold is 
implemented by accepting blocks of data greater than 44 data points where 
the two moving average results do not intersect. These segments are 
characterized as QRS waves and the maximum voltage is deemed the R peak. 
The index of this R peak is what constitutes a peak. 

https://www.scitepress.org/Papers/2010/27427/27427.pdf

## How the Code Calculates Heartrate

The code detects the Heartrate by using the number of R peaks and the time 
between the frst and last R peaks identified. By dividing the number of 
peaks by the time, a Heartrate in beats-per-second is identified. By diving 
by 60 the Heartrate in beats-per-minute is identified. 

# MIT License
Copyright (c) [2022] [Benjamin Alexander Randoing & Joshua Yao Li]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
