# Purpose: The purpose of this script is to complete the preprocessing phase using the spacy module.
# Steps Completed can be found in the following link:
# https://towardsdatascience.com/setting-up-text-preprocessing-pipeline-using-scikit-learn-and-spacy-e09b9b76758f

import json
from spacy.lang.en import English

def read_json_data(file="./data_by_category.json"):
    with open(file, "r") as link_file:
        data = json.load(link_file)

    return data


data = read_json_data()

nlp = English()
doc = nlp("Space Balls")

for word in doc:
    print(word)
