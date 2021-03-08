# Purpose: The purpose of this script is to complete the preprocessing phase using the spacy module.
# Steps Completed can be found in the following link:
# https://towardsdatascience.com/setting-up-text-preprocessing-pipeline-using-scikit-learn-and-spacy-e09b9b76758f
# Multiclass text classification: https://towardsdatascience.com/multi-class-text-classification-with-scikit-learn-12f1e60e0a9f


import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score

from spacy.lang.en import English
from io import StringIO

def read_json_data(file="./data.json"):
    with open(file, "r") as link_file:
        data = json.load(link_file)

    return data

def convert_catagories_to_int(data):
    dictionaries = data['app']
    temp = []

    for dict in dictionaries:

        values_list = {"Art and Design": 1,"Augmented Reality": 2, "Auto & Vehicles": 3, "Beauty": 4,
                       "Books and Reference": 5, "Business":6, "Comics": 7, "Communication":8,
                       "Dating":9, "Daydream": 10, "Education": 11, "Entertainment": 12, "Events": 13,
                       "Finance": 14, "Food & Drink": 15, "Health & Fitness": 16, "House & Home": 17,
                       "Libraries & Demo ": 18, "Lifestyle": 19, "Maps & Navigation":20, "Medical": 21,
                       "Music and Audio": 22, "Games ": 23}

        for item in values_list:
            if list(dict.values())[3] == item:
                dict["category"] = values_list[item]

    return dictionaries

# Read the data from the data.json data file
data=read_json_data()

# convert the categories from text to numeric values --> Dic with number categories.
# numeric_data = convert_catagories_to_int(data)

# Convert the dictionary format data to a pandas dataframe.
df = pd.DataFrame(data["app"])

# We will only use appTitle, mini_description and category.
# The following code reduces the data to only the above three columns.
col = ['category', 'app_mini_description']
df = df[col]

# Set the names of the columns and then add a column
# that creates unique category ids.
df.columns = ['category', 'app_mini_description']
df['category_id'] = df['category'].factorize()[0]

# General sorting. Variables to be used later in code.
category_id_df = df[['category', 'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'category']].values)


# We should evaluate the distribution of apps. The following code shows the
# distribution of apps by category with the frequency of mini-descriptions.
fig = plt.figure(figsize=(8,6))
df.groupby('category').app_mini_description.count().plot.bar(ylim=0)
plt.show()

# Create a tdif vectorizer with the following attributes.
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')

# fit the tfdidf model to the app_mini_descriptions
features = tfidf.fit_transform(df["app_mini_description"]).toarray()
labels = df['category_id']

# Each of the n app_mini_descriptions are now represented by m features which
# representing the tf-idf core for different uni-grams and bi-grams
print(features.shape)

# Now, let us use chi2 to find terms that are most correlated with each
# category

N =2
for category, category_id in sorted(category_to_id.items()):
    features_chi2 = chi2(features,labels==category_id)
    indicies = np.argsort(features_chi2[0])
    feature_names = np.array(tfidf.get_feature_names())[indicies]
    unigrams = [v for v in feature_names if len(v.split(' '))==1]
    bigrams = [v for v in feature_names if len(v.split(' ')) ==2]
    print("#{}".format(category))
    print(" .Most correlated unigrams:\n{}".format('\n'.join(unigrams[-N:])))
    print(" .Most correlated bigrams:\n{}".format('\n'.join(bigrams[-N:])))


# In prelimiary results, it is clear that unigram model
# is more representitive than bigram models.
# This shows that more often words in app descriptions appear alone
# More data may prove to change this conclusion.


# we will now develop a classifier. To use the classifier,
# we will need to vectorize our app_mini_descriptions.
# We will also need to determine what ML model we will choose.
# Naive Bayes is particularly suited for word counts
# We will text more ml models towards the end of this module

X_train, X_test, y_train, y_test = train_test_split(df["app_mini_description"], df["category"], random_state=0)
count_vec = CountVectorizer()
X_train_counts = count_vec.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

clf = MultinomialNB().fit(X_train_tfidf, y_train)

# Make a standard prediction. From here, we can tell that the mini_app_descriptions may not
# provide sufficient data to predict app catagories.
# TODO Consider changing mini app descriptions to just app descriptions.

print(clf.predict(count_vec.transform(["Plan your life"])))


# Let us now evaluate the results of our models and compare them to the following models:
# Logistic Regression
# (Multinomial Naive-Bayes)
# Linear Support Vector Machine
# Random Forest

models = [LogisticRegression(), MultinomialNB(), LinearSVC(), RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0)]

CV = 5

cv_df = pd.DataFrame(index=range(CV*len(models)))
entries=[]

for model in models:
    model_name = model.__class__.__name__
    accuracies = cross_val_score(model,features, labels, scoring="accuracy", cv=CV )

    for fold_idx, accuracy in enumerate(accuracies):
        entries.append((model_name,fold_idx, accuracy))

cv_df = pd.DataFrame(entries, columns=['model_name','fold_idx','accuracy'])

print("ACCURACY OF MODELS")
print(cv_df.groupby('model_name').accuracy.mean())

# TODO Find the best model and then optimize for the problem.
# TODO complete text preprocessing before the machine learning to imporve accuracy.
# We only removed stop words.


