
import json
import pandas as pd

def read_json_data(file="./data.json"):
    with open(file, "r") as link_file:
        data = json.load(link_file)

    return data


data = read_json_data()
frame = pd.json_normalize(data, "app")

frame.to_excel("/Users/brandonarchuleta/Desktop/App_Data_Catagories.xlsx")


