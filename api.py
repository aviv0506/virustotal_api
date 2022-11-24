import logging
import os
import requests
import time
import logging
import datetime
import json

logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG)

json_obj_list = []


def operation():
    try:
        operation = input("Choose operation\n1. One file.\n2. Multiple files.\n3. Recursively a folder.\n")
        operation_handler_validate(operation)
        apikey = input("Enter your API key:\n")

        if operation == "1":
            one_file(apikey)

        elif operation == "2":
            multiple_files(apikey)

        elif operation == "3":
            recursively_folder(apikey)

    except Exception as e:
        logging.warning("function operation_handler failed: %s", f'{e}')
        return e


def one_file(apikey):
    try:
        file_full_path = input("Enter the full file path: ")
        file_name = file_full_path.split('/',)[-1]
        one_file_req(apikey, file_name, file_full_path)
        save_json_file(json_obj_list)

    except Exception as e:
        logging.warning("function one_file failed: %s", f'{e}')
        return e


def multiple_files(apikey):
    try:
        files_full_paths = input("Enter all files paths separated by space  \n")
        files_list = files_full_paths.split(" ")
        for file in files_list:
            file_name = files_full_paths.split('/', )[-1]
            one_file_req(apikey, file_name, file)
        save_json_file(json_obj_list)

    except Exception as e:
        logging.warning("function multiple_files failed: %s", f'{e}')
        return e


def recursively_folder(apikey):
    try:
        folder_full_path = input("Enter folder full path  \n")

        for root, dirnames, filenames in os.walk(f'{folder_full_path}'):
            for filename in filenames:
                file = os.path.join(root, filename)
                file_name = file.split('/', )[-1]
                one_file_req(apikey, file_name, file)

        save_json_file(json_obj_list)

    except Exception as e:
        logging.warning("function recursively_folder failed: %s", f'{e}')
        return e


def one_file_req(apikey, file_name, file_path):
    try:
        time.sleep(20)
        params = {'apikey': f'{apikey}'}
        files = {'file': (file_name, open(file_path, 'rb'))}
        response = requests.post('https://www.virustotal.com/vtapi/v2/file/scan', files=files, params=params)
        json_response = response.json()
        print(json_response)
        json_obj_list.append({'results': json_response})


    except Exception as e:
        logging.warning("function one_file_req failed: %s", f'{e}')
        return e


def save_json_file(json_obj_list):
    current_time = datetime.datetime.now()
    with open(f'{current_time}.json', 'w', encoding='utf-8') as f:
        json.dump(json_obj_list, f, ensure_ascii=False, indent=4)


def operation_handler_validate(operation):
    try:
        int(operation)
        if operation != "1" and operation != "2" and operation != "3":
            logging.warning('function operation_handler failed: %s' 'Please enter a number between 1 - 3')
            raise Exception("Please enter a number between 1 - 3")

    except ValueError:
        logging.warning("function input_validator failed: ValueError")
        raise Exception("Please provide a number!")

    except Exception as e:
        logging.warning("function input_validator failed: %s", f'{e}')
        return e
