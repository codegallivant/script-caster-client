import json
import os



def get_dict():
    f = open("CLIENT_CONSTANTS.json",'r')
    user_variables_dict = json.loads(f.read())
    f.close()
    return user_variables_dict


def get(user_variable_name):
    data = get_dict()
    return data[user_variable_name]


def update(user_variable_name, new_variable_value):
    data = get_dict()
    f = open("CLIENT_CONSTANTS.json", 'w')
    data[user_variable_name] = new_variable_value
    f.seek(0)  # rewind
    json.dump(data, f)
    f.truncate()
    f.close()
  