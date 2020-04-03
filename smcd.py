#! python3
# smcd.py - (Selective Move/Copy/Delete) Allows user to move/copy/delete file(s) based on regex filter
# Created by Teng Mao @https://github.com/TengCXXI

import os, re, shutil, send2trash
import pyinputplus as pyip
from pathlib import Path

# Create a while loop to check for an absolute folder path input
while True:
    print("On what absolute folder path would you like to perform the action?")
    folder_path = input()
    if Path(folder_path).exists() == True:
        break
    else:
        print("Please enter a valid absolute folder path.")
        continue

# Input choice for action to perform
print("What action would you like to perform on the files in the folder: Move, Copy, or Delete?")
action = pyip.inputChoice(['Move', 'Copy', 'Delete'])

if action in 'MoveCopy':

    # Create a while loop for the destination folder which will:
    #     -Check to see if the folder path currently exists
    #     -If it doesn't exist, ask user whether they want to create the folder path
    #     -If user wants to create folder path, check to see if the absolute folder path is valid
    #     -Ask user to provide a valid path if an invalid one was entered

    while True:
        print("What is the destination folder?")
        destination_folder = input()
        if Path(destination_folder).exists() == True:
            break

        print("This folder path does not currently exist. Would you like to create it - (y)es or (n)o? ")
        create_path = pyip.inputYesNo()
        if create_path == "yes" and os.path.isabs(destination_folder) == True:
            os.makedirs(destination_folder)
            print(f"{destination_folder} folder created.")
            break

        else:
            print("Please enter a valid absolute folder path.")
            continue


# Create a while loop for the regex input which will:
#     -Use regex to select files for action
#     -Print out the number of actionable files
#     -Ask if the user would like to proceed with the selected files, or re-write the regex statement


while True:
    # Input regex for filter to select files for action
    print("Please enter the regex to select the files for action:")
    print('Examples: "\w*\.txt$"(all ".txt" files), "^XyZ\S*"(begins with "XyZ"), \w*XyZ\S*(contains "XyZ"), "|" to add filter')
    regex_input = input()
    file_regex = re.compile(r'{0}'.format(regex_input), re.IGNORECASE)

    printout_width = 50
    print('NUMBER OF ACTIONABLE FILES'.center(printout_width, '='))

    total_files_count = 0

    # Create a loop to count the number of files selected based on regex

    for folder_name, subfolders, files in os.walk(folder_path):
        folder_files_count = 0

        # Loop to count the files within the folder
        for file in files:
            if file_regex.search(file) != None:
                folder_files_count += 1

        # Increment the total_files by the folder_files count
        total_files_count += folder_files_count
        print(folder_name + ': ' + str("{:,}".format(folder_files_count)))

    print('=' * printout_width)
    print('THE TOTAL NUMBER OF ACTIONABLE FILES: ' + str("{:,}".format(total_files_count)))
    print('=' * printout_width)

    print("Proceed - (y)es or (n)o?")
    proceed_with_regex = pyip.inputYesNo()
    if proceed_with_regex == "yes":
        break

# Create a loop to COPY the files based on regex

if action == "Copy":
    for folder_name, subfolders, files in os.walk(folder_path):
        for file in files:
            if file_regex.search(file) != None:
                shutil.copy(str(Path(folder_name)/file), destination_folder)

    print(str("{:,}".format(total_files_count)) + ' file(s) copied.')

# Create a loop to MOVE the files based on regex

if action == "Move":
    for folder_name, subfolders, files in os.walk(folder_path):
        for file in files:
            if file_regex.search(file) != None:
                shutil.move(str(Path(folder_name)/file), destination_folder)

    print(str("{:,}".format(total_files_count)) + ' file(s) moved.')

# Create a loop to DELETE the files based on regex

if action == "Delete":
    for folder_name, subfolders, files in os.walk(folder_path):
        for file in files:
            if file_regex.search(file) != None:
                send2trash.send2trash(str(Path(folder_name)/file))

    print(str("{:,}".format(total_files_count)) + ' file(s) deleted.')
