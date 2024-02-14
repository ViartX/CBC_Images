# this is an executable code for CBC detection model


import sys
import os
import glob
import time
import shutil
from ultralytics import YOLO

# global variables
ECHO = 1
model_filename = ""
source_path = ""
workdir_path = ""
results_path = ""


def main():
    # read ini file to get 4 paths
    if process_ini_file() != 4:
        print("missing data from ini file")
        return

    # launch the YOLO model
    model = ""
    if not os.path.exists(model_filename):
        print(f'Error: File {model_filename} does not exist')
        return -1
    else:
        model = YOLO(model_filename)
        if model != "":
            printout("Model successfully uploaded")
            printout(model.info())

    # check source folder for files

    print("Input folder scanning started")

    value = ""
    while True:
        printout("new step started")
        time.sleep(10)
        source_file = scan_dir(source_path, "jpg")
        if source_file == "":
            continue
        printout(source_file)
        process_source_file(source_file, model)
        # break

    return


# output value with entry request before the next step
def action(query):
    value = input(query + " :")
    return value


# quick optional print call for verbose values
def printout(text):
    if ECHO:
        print(text)


# processes ini filename, to get work settings
# model_filename = "path\model.pt"
# work_directory = "path"
# source_directory = "path"
# results_directory = "path"
def process_ini_file(ini_filename="model.ini"):

    number_of_lines_found = 0
    global model_filename, source_path, workdir_path, results_path

    printout("current folder: " + os.getcwd())
    ini_filename = os.getcwd()+"\\"+ini_filename    # concatenate folder name and file name
    if not os.path.exists(ini_filename):
        print(f'Error: File {ini_filename} does not exist')
        quit

    f = open(ini_filename)
    for line in f:
        initial_text = line
        line = line.replace(" ", "")
        line = line.replace("\n", "")
        if line.find("model_filename=") > -1:
            model_filename = line[16:]
            model_filename = model_filename.replace('"', '')
            number_of_lines_found +=1
        elif line.find("work_directory=") > -1:
            workdir_path = line[16:]
            workdir_path = workdir_path.replace('"', '')
            number_of_lines_found +=1
        elif line.find("source_directory=") > -1:
            source_path = line[17:]
            source_path = source_path.replace('"', '')
            number_of_lines_found +=1
        elif line.find("results_directory=") > -1:
            results_path = line[18:]
            results_path = results_path.replace('"', '')
            number_of_lines_found +=1

    printout("ini file processed with " + str(number_of_lines_found) + " values")
    printout("model_filename: " + model_filename)
    printout("workdir_path: " + workdir_path)
    printout("source_path: " + source_path)
    printout("results_path : " + results_path)

    f.close()

    return number_of_lines_found


# scans input folder for any new file, returns filename
def scan_dir(path, extention) -> str:
    filename = ""
    if not os.path.exists(path):
        print(f'Error: Folder {path} does not exist')
        return ""
    else:
        files_list = glob.glob(path+"/*."+extention)   # return the list of files in folder
        if len(files_list) > 0:
            filename = files_list[0]            # get the first element from non empty list

    return filename


# process source file
# 1. Copy source file to work folder, that also checks if file is completely ready for processing
# 2. Run detection with model
def process_source_file(filename, model):
    # get full file name in workdir
    if not os.path.exists(workdir_path):
        print(f'Error: Work folder {workdir_path} does not exist')
        quit

    # move source file to work folder
    work_file = filename.replace(source_path, workdir_path)
    printout("Work filename is: " + work_file)
    try:
        shutil.move(filename, work_file)
    except Exception:
        printout("Error while coping file to work folder")
        quit

    results = model.predict(work_file, save=True, save_txt=True)

    # find detection results in current_folder + "runs\detect\predict"
    # after reading is complete, folder should be removed
    path_to_model_results = os.getcwd() + "\\runs\\detect\\predict"
    if process_detection_results(path_to_model_results) < 0:
        printout("Error: Result folder not found. " + path_to_model_results)


# process txt results file to format applicable for LIMS system, creates new text file in proper format
def process_txt_results(filename):
    if not os.path.exists(filename):
        return -1

    head, tail = os.path.split(filename)
    result_filename = filename.replace(tail, "Result_" + tail)
    f = open(filename, "r")         # txt result from model
    r = open(result_filename, "w")  # txt result updated

    rbcs = 0
    wbcs = 0
    platellets = 0

    while True:
        line = f.readline()
        if not line:
            break
        if line[0] == '0':
            platellets += 1
        elif line[0] == '1':
            rbcs += 1
        elif line[0] == '2':
            wbcs += 1

    r.write("RBC: "+str(rbcs)+"\n")
    r.write("WBC: " + str(wbcs) + "\n")
    r.write("Platelet: " + str(platellets) + "\n")

    f.close()
    r.close()


# move processed detection results from work folder to results folder
def move_folder(folder_from, folder_to):
    if not os.path.exists(folder_from):
        return -1

    # find unique name for folder_to
    destination = folder_to
    suffix = 0
    while True:
        if os.path.exists(destination):
            suffix += 1
            destination = folder_to + "_" + str(suffix)
        else:
            break

    files_list = glob.glob(folder_from + "/*")  # return the list of files in folder

    try:
        shutil.move(folder_from, destination)
        os.makedirs(folder_from)
    except Exception:
        printout("Error while coping file to result folder")
        quit


def process_detection_results(path):
    if not os.path.exists(path):
        return -1

    path_to_jpg = ""    # path to jpg file with detection results
    path_to_txt = ""    # path to text file with detection results

    path_to_jpg = scan_dir(path, "jpg")
    path_to_txt = scan_dir(path+"\\labels", "txt")

    # move source file to work folder
    path_to_result_jpg = path_to_jpg.replace(path, workdir_path)
    head, tail = os.path.split(path_to_result_jpg)
    path_to_result_jpg = path_to_result_jpg.replace(tail, "Result_"+tail)
    head, tail = os.path.split(path_to_txt)
    path_to_result_txt = workdir_path+"\\"+tail

    try:
        shutil.move(path_to_jpg, path_to_result_jpg)
        shutil.move(path_to_txt, path_to_result_txt)
        shutil.rmtree(path)
    except Exception:
        printout("Error while coping file to work folder")
        quit

    # process txt file to specify numeric values
    process_txt_results(path_to_result_txt)

    # copy work folder to results for that sample
    folder_name = tail.split(".")
    move_folder(workdir_path, results_path + "\\" + folder_name[0])

    return 0


# main function processing
if __name__ == '__main__':
    main()