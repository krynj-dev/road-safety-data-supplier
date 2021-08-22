import json, math

import requests

import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

class RoadSafetyModel(object):
    """This class is not configured for use with the front end.
        This file should not be evaluated as part of the GovHack 2021 Competition.
        It remains here as an indicator of a considered idea (ML model to predict crashes) that could be expanded on in the future.
    """
    def __init__(self):
        '''
            Initialises the model
        '''
        self.limit = 5000
        self.data = self.retrieve_data()

        if self.data is None:
            raise Exception

        # Print columns and their indicies
        for i in range(len(self.data.columns)):
            print("{}: {}".format(i, self.data.columns[i]))

        self.model = self.nn_train()


    def nn_train(self):
        # Sample the data randomly
        data_sample = self.data.sample(2000)
        selected_columns = [3, 4, 5, 13, 30, 32, 33]
        # Printing selected columns
        print(self.data.columns[selected_columns])
        # Transform data into scikit learn friendly data
        one_hot = pd.get_dummies(data_sample.iloc[:,[4, 5, 6, 14, 16]], drop_first=True)
        # Split into train and test data
        X_train, X_test, y_train, y_test = train_test_split(one_hot.values, data_sample["Crash_Severity"].values, random_state=0)
        # Train ANN
        N_h = math.ceil( self.limit/(2*(len(one_hot.columns)+len(pd.unique(data_sample["Crash_Severity"])))) )
        print("N_h = {}".format(N_h))
        clf = MLPClassifier(solver="lbfgs", alpha=1e-5, hidden_layer_sizes=(N_h, N_h), random_state=1, max_iter=4000)
        clf.fit(X_train, y_train)

        # Predict Test data
        print(clf.classes_)
        score = clf.score(X_test, y_test)
        probs = clf.predict_proba(X_test)
        np.set_printoptions(suppress=True)
        print(probs[0])
        print(y_test[0])
        print(score)



    def retrieve_data(self, online=False):
        '''
            Grabs the data from the QLD Open Data website and parses it as JSON.
        '''
        if online:
            req = requests.get("https://www.data.qld.gov.au/api/3/action/datastore_search?resource_id=e88943c0-5968-4972-a15f-38e120d72ec0&limit={}&sort={}".format(
                self.limit,
                ""))
            if req.status_code != 200:
                print("Failed to get the data from the server")
                return None
            else:
                data_text = req.text
                data_json = json.loads(data_text)
                return pd.json_normalize(data_json["result"]["records"])
        else:
            return pd.read_csv("1_crash_locations.csv")

if __name__ == "__main__":
    rsm = RoadSafetyModel()