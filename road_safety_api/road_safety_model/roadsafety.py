import pandas as pd
import numpy as np
from os import path

class RoadSafety(object):
    def __init__(self):
        self.data = pd.read_csv(path.join(path.abspath(__file__), "../1_crash_locations.csv"))

    def get_speed_str(self, speed):
        return "{} km/h".format(speed)
    
    def get_distribution(self, month=None, day=None, suburb=None, speed=None, weather=None, light=None):
        print(month, day, suburb, speed, weather, light )
        # Filter the Data
        filtered = self.data.copy()
        if month is not None:
            filtered = filtered[filtered.Crash_Month == month]
        if day is not None:
            filtered = filtered[filtered.Crash_Day_Of_Week == day]
        if suburb is not None:
            filtered = filtered[filtered.Loc_Suburb == suburb]
        if speed is not None:
            speed_str = self.get_speed_str(speed)
            filtered = filtered[filtered.Crash_Speed_Limit == speed_str]
        if weather is not None:
            filtered = filtered[filtered.Crash_Atmospheric_Condition == weather]
        if light is not None:
            filtered = filtered[filtered.Crash_Lighting_Condition == light]
        if len(filtered) == 0:
            return {
            "Fatal": 0,
            "Hospitalisation": 0,
            "Medical attention": 0,
            "Minor Injury": 0,
            "Property damage only": 0
        }
        # Get the proportions
        # counts = filtered.groupby("Crash_Severity")["Crash_Ref_Number"].nunique().to_numpy()
        
        # new version of counts
        counts = filtered["Crash_Severity"].value_counts().to_frame()
        proportions = counts.copy()
        proportions["Crash_Severity"] /= sum(proportions["Crash_Severity"])
        proportions = proportions.to_dict()["Crash_Severity"]

        for severity in self.data["Crash_Severity"].unique():
            if severity not in proportions.keys():
                proportions[severity] = 0
        
        # print(counts)

        return proportions

    def get_suburbs(self):
        return self.data["Loc_Suburb"].unique().tolist()

    def get_lightings(self):
        return self.data["Crash_Lighting_Condition"].unique().tolist()

    def get_weathers(self):
        return self.data["Crash_Atmospheric_Condition"].unique().tolist()

    def get_speeds(self):
        return self.data["Crash_Speed_Limit"].unique().tolist()
    

        


if __name__ == "__main__":
    rs = RoadSafety()
    print(rs.get_speeds())
    
