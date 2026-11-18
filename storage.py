import json
import os



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EXPENSES_FILE = os.path.join(BASE_DIR, 'expenses.json')
GROUPS_FILE = os.path.join(BASE_DIR, 'groups.json')
SETTLEES_FILE = os.path.join(BASE_DIR, 'settlements.json')



def initialize_storage():
    """ Create JSON files if they don't exist. """


    files = [
        EXPENSES_FILE,
        GROUPS_FILE,
        SETTLEES_FILE

    ]

    for file_path in files:
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4)

def load_data(file_path):
    """ Load data from a JSON file. """

    initialize_storage()

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        print(f"Warning : Unexpected data format in {file_path}")
        return []


    except (json.JSONDecodeError, OSError) as error:
        print(f"Error loading data : {error}")
        return []


def save_data(file_path, data):
    """ Save data to a JSON file. """

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4 , ensure_ascii=False)

        return True

    except (OSError, TypeError, ValueError) as error:
        print(f"Error saving data : {error}")
        return False
    


def load_expenses():
    return load_data(EXPENSES_FILE)

def save_expenses(expenses):
    """ Save personal expenses to the JSON file. """
    return save_data(EXPENSES_FILE, expenses)

def load_groups():
    """ Load Splitwise groups from the JSON file. """
    return load_data(GROUPS_FILE)

def save_groups(groups):
    """ Save Splitwise groups to the JSON file. """
    return save_data(GROUPS_FILE,  groups)

def load_settlements():
    """ Load settlements from the JSON file. """
    return load_data(SETTLEES_FILE)

def save_settlements(settlements):
    """ Save settlements to the JSON file. """
    return save_data(SETTLEES_FILE, settlements)

initialize_storage()