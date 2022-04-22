import math as m
import logging
from ecgdetectors import Detectors
import json
import matplotlib.pyplot as plt


def analyze_data_file(filename):
    """Read and format the inputted ecg data

    analyze_data_file takes in a raw .csv file that has a time and voltage
    comma delimited data set and reads in all data that is properly
    formatted into float arrays for a time and voltage separately.

    :param filename: The filename and path of the raw .csv ecg data on the
    local machine

    :returns: The time and voltage float arrays without any empty, nan,
    or string cells
    """
    kickstart(filename)
    time = []
    voltage = []
    in_file = open(filename, 'r')
    keep_reading = True
    line_number = 0
    while keep_reading:
        data_line = in_file.readline()
        if data_line == "":  # ok to use because will have at least a comma
            keep_reading = False
        else:
            line_number += 1
            append, time_point, voltage_point = \
                process_line(data_line, line_number)
            if append is True:
                time.append(time_point)
                voltage.append(voltage_point)
                in_range(voltage_point, line_number)
    in_file.close()
    return time, voltage


def kickstart(filename):
    """Log an info entry when starting to analyze a new data file

    kickstart is a function that merely logs an info note when starting to
    analyze a new ECG data file.

    :param filename: The filename including the entire path of the data file
    """
    logging.info(
        "The file {} has started analysis."
        .format(filename))


def in_range(voltage_point, line_number):
    """Identify Voltage data outside +/- 300 mV

    in_range looks at a single float voltage data point to determine if it
    is within +/- 300mV. If the data point is outside this range, a warning
    is logged.

    :param voltage_point: The singular voltage data value
    :param line_number: The line number of the voltage point in raw data file
    """
    if abs(voltage_point) > 300.0:
        logging.warning(
            "The line {} has a voltage outside +/- 300 mV."
            .format(line_number))
    return


def process_line(data_line, line_no):
    """Format the data line if numerical and proper data entry

    process_line takes in a string of a time and voltage data line. This
    string is process via three trial cases to ensure there is not
    a string, nan, or empty cell for the data. This is then either returned
    or a warning is lgged with the line number.

    :param data_line: String line of time and voltage data points
    :param line_no: Line number int of current line

    :returns: a boolean of True when no problems exist with data
    Either two strings of 0.0 or the float data points from the data line
    """
    append = True
    data_points = data_line.strip("\n").split(",")
    time_point = data_points[0]
    voltage_point = data_points[1]
    if time_point == "" or voltage_point == "":
        logging.warning("The line {} has a missing time or voltage".
                        format(line_no))
        append = False
        time_point = "0.0"
        voltage_point = "0.0"
        return append, time_point, voltage_point
    time_nums = remove_period_neg(time_point)
    voltage_nums = remove_period_neg(voltage_point)
    try:
        if m.isnan(float(time_point)) is True or \
                m.isnan(float(voltage_point)) is True:
            logging.warning("The line {} has a NaN "
                            "time or voltage".format(line_no))
            append = False
            time_point = "0.0"
            voltage_point = "0.0"
            return append, time_point, voltage_point
    except ValueError:
        if not (time_nums.isnumeric() and voltage_nums.isnumeric()):
            logging.warning("The line {} has a string"
                            " time or voltage".format(line_no))
            append = False
            time_point = "0.0"
            voltage_point = "0.0"
            return append, time_point, voltage_point
    return append, float(time_point), float(voltage_point)


def remove_period_neg(string_entry):
    """Format a string to determine if the string isnumeric()

    remove_period_neg is a function that takes a string and removes any
    periods or dashes. Numerically, these represent a decimal point or a
    negative sign.

    :param string_entry: A string type of a time or voltage data point

    :returns: The final string with periods or dashes
    """
    new_string = string_entry.replace(".", "").replace("-", "")
    return new_string


def calculate_sampling_freq(time_array):
    """Identify the Sampling Frequency for the Peak Detecting Module
    Implemented

    calculate_sampling frequency looks at two time data points to quantify
    the sampling frequency of the ECG data.

    :param time_array: The float array of all raw time points

    :returns: The sampling frequency or inverse of sampling period
    """
    dt = time_array[1]-time_array[0]
    fs = 1/dt
    return fs


def calculate_total_time(time_array):
    """Identify the length of time of the data file

    calculate_total_time finds the differences in time between the first
    and last array entries to find the total time. This is logged after
    finishing to illustrate the code status.

    :param time_array: The formatted time input data from the ECG file

    :returns: The length of time float of the time array
    """
    total_time = time_array[-1]-time_array[0]
    logging.info("The total time has been calculated")
    return total_time


def calculate_min_max(voltage_array):
    """Find the min and max voltages

    calculate_min_max uses the min and max functions in python
    to identify the largest and smallest (including negatives)
    voltage data points. This is then logged.

    :param voltage_array: The formatted voltage input data from the ECG file
    in mV

    :returns: a tuple of the float min and max
    voltages
    """
    max_voltage = max(voltage_array)
    min_voltage = min(voltage_array)
    logging.info("The min and max voltages have been calculated")
    return (min_voltage, max_voltage)


def find_peak_attributes(voltage_array, time_array):
    """Identify the Peak Indexes and Number of Peaks

    find_peak_attributes implements the two_average_detector function to
    identify the index points of each R peak. The resultant array length
    represents the number of peaks. This is then logged.

    :param voltage_array: The formatted voltage input data array
    :param time_array: The formatted time input data array

    :return: an array of index values for when the  peaks occur and an int
    quantity of the number of peaks.
    """
    detectors = Detectors(calculate_sampling_freq(time_array))
    r_peaks = detectors.two_average_detector(voltage_array)
    num_peaks = len(r_peaks)
    logging.info("The number of peaks has been calculated")
    return r_peaks, num_peaks


def find_peak_times(time_array, peak_array):
    """Identify the time points when peaks occur

    find_peak_times searches for the time points in the time_array
    that correspond to the index values of the peaks. This is then logged.

    :param time_array: The formatted time input data array
    :param peak_array: The array of peak index locations

    :returns: An array of float time values for when the peaks occurred
    """
    peak_times = []
    for i in range(len(peak_array)):
        peak_times.append(time_array[peak_array[i]])
    logging.info("The peak times have been calculated")
    return peak_times


def find_mean_hr(num_peaks, peak_times):
    """Identify the heartrate in bpm

    find_mean_hr Divides the time between the outer most R peaks by the
    number of peaks to determine the average heart rate. This is then scaled
    to bpm and logged.

    :param num_peaks: The int number of peaks in the data set
    :param peak_times: The array of times corresponding to each R peak

    :returns: The float of the mean heart rate
    """
    time_diff_between_peaks = peak_times[-1]-peak_times[0]
    time_in_min = time_diff_between_peaks/60
    mean_hr = num_peaks/time_in_min
    logging.info("The mean hr has been calculated")
    return mean_hr


def create_out_dict(time_array, voltage_array):
    """Create a dictionary with all specified outputs

    create_out_dict runs the calculation functions for all of the desired
    metrics. This is followed by adding these metrics to a dictionary and
    calling a function to log the status.

    :param time_array: The formatted time input data array
    :param voltage_array: The formatted voltage input data array

    :returns: a dictionary of desired outputs from ECG analysis
    """
    duration = calculate_total_time(time_array)
    voltage_extremes = calculate_min_max(voltage_array)
    num_beats = find_peak_attributes(voltage_array, time_array)[1]
    peaks = find_peak_attributes(voltage_array, time_array)[0]
    beats = find_peak_times(time_array, peaks)
    mean_hr_bpm = find_mean_hr(num_beats, beats)

    metrics = {
               "duration": duration,
               "voltage_extremes": voltage_extremes,
               "num_beats": num_beats,
               "mean_hr_bpm": mean_hr_bpm,
               "beats": beats,
              }
    dict_log()
    return metrics


def dict_log():
    """Log info after creating dictionary

    dict_log creates a log entry to be called after writing metrics to a
    dictionary.
    """
    logging.info("The dictionary has been filled with data values")


def output_json(dictionary, filename):
    """Create a .json with the metrics dictionary

    output_json merely takes a dictionary of metrics and creates a .json as
    the desired output format.

    :param dictionary: The metrics dictionary
    :param filename: The string name of the filename
    """
    new_name = filename.strip(".csv")+".json"
    out_file = open(new_name, "w")
    json.dump(dictionary, out_file)
    out_file.close()


if __name__ == "__main__":
    logging.basicConfig(filename="log_example", level=logging.INFO)
    filename = "test_data23.csv"
    path = "/Users/benrandoing/Documents/BME_547" \
           "/class_repos/ecg-analysis-benrandoing20/" \
           "test_data/"+filename
    time, voltage = analyze_data_file(path)
    # plt.plot(time,voltage)
    # plt.show()
    metrics = create_out_dict(time, voltage)
    output_json(metrics, filename)
