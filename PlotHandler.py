from enum import Enum
import os
from typing import Dict
import matplotlib.pyplot as plt

class X_label_options(Enum):
    NO_LIMIT = 1
    LIMIT = 2
    DAY = 3

class Plot:
    '''class representing a plot'''
    def __init__(self, data: Dict) -> None:
        self._check_data(data)
        self.data = data
        self.fig, self.ax = plt.subplots()

    def _check_data(self, data: Dict):
        keys = ["x_label", "y_label", "x_data", "y_data", "label"]
        for key in keys:
            if data[key] is None:
                raise KeyError("Input to plot is not correct. Needs to contain: x_label [str], y_label [str], x_data [List[List[int]]], y_data List[List[int]]], label [List[str]]")

        if not len(data["x_data"]) == len(data["y_data"]) == len(data["label"]):
            raise Exception("x_data, y_data, label needs to have the same length")

    def create_lineplot(self, limit_x_label=X_label_options.NO_LIMIT, color=None):
        '''Create a plot with the number of x,y sets defined'''
        plt.xlabel(self.data["x_label"])
        plt.ylabel(self.data["y_label"])
        for set in range(0, len(self.data["x_data"])):
            if color is not None:
                self.ax.plot(self.data["x_data"][set], self.data["y_data"][set], label=self.data["label"][set], color=color)
            else:
                self.ax.plot(self.data["x_data"][set], self.data["y_data"][set], label=self.data["label"][set])
        if limit_x_label == X_label_options.LIMIT:
            for label in self.ax.get_xaxis().get_ticklabels()[::2]:
                label.set_visible(False)
        if limit_x_label == X_label_options.DAY:
            for label in self.ax.get_xaxis().get_ticklabels():
                label.set_visible(False)
        plt.setp(self.ax.get_xticklabels(), rotation=45, ha='right')
        self.ax.legend()
        plt.show()

    def save_plot(self, path, plot_name):
        '''Save plot as png'''
        plot_name = plot_name + ".png"
        plt.savefig(os.path.join(path, plot_name))

if __name__ == "__main__":
    from DatabaseHandler import DataBaseHandler

    PLANTY_TABLE = "Planty_data"
    database_handler = DataBaseHandler()
    database_handler.connect_to_database("Planty2")
    data = database_handler.select_from_table(PLANTY_TABLE, ["Datetime","light","light_wo_regulator","moisture"], True, "Datetime", 47)

    if len(data) < 47:
        data = database_handler.select_from_table(PLANTY_TABLE, ["Datetime","light","light_wo_regulator","moisture"], True, "Datetime", len(data) - 1)
    time = [str(x[0].time().isoformat(timespec='minutes')) for x in data]
    light = [y[1] for y in data]
    light_wo_regulator = [y[2] for y in data]
    moisture = [y[3] for y in data]
    print(moisture)

    print("Test plot")
    x_label = "Time"
    y_label = "Light"
    x1 = [1,2,3,4,5,6,7,8,9,10]
    y1 = [1,2,3,4,5,6,7,8,9,10]
    x2 = [5,6,7,8,9,10,11,12,13,14]
    y2 = y1

    labels = ["Light", "light wo regulator"]
    light_dict = {"x_label" : x_label,
            "y_label" : y_label,
            "x_data" : [time, time],
            "y_data" : [light,light_wo_regulator],
            "label" : labels}
    path = ""
    name = "test_plot"
    #print(data)
    #plot = Plot(data)
    #plot.create_lineplot(limit_x_label=True)
    #plot.save_plot(path, name)

    '''    CAMERA_TABLE = "Camera_data"
    camera_data = database_handler.select_from_table(CAMERA_TABLE, ["Datetime","green_percent"], True, "Datetime", 30)
    if len(camera_data) <= 30:
        camera_data = database_handler.select_from_table(CAMERA_TABLE, ["Datetime","green_percent"], True, "Datetime", len(data))

    date = [str(x[0]) for x in camera_data]
    date.reverse()
    green = [y[1] for y in camera_data]
    green.reverse()
    data_dict = {"x_label" : "Date",
                "y_label" : "Growth percent",
                "x_data" : [date],
                "y_data" : [green],
                "label" : ["Growth"]}
    green_plot = Plot(data_dict)
    green_plot.create_lineplot(limit_x_label=False,color="green")'''

    mois_limit = [500] * len(data)
    print(mois_limit)
    moisture_data_dict = {"x_label" : "Time",
                "y_label" : "Moisture",
                "x_data" : [time, time],
                "y_data" : [moisture, [500] * len(data)],
                "label" : ["Moisture","Limit"]}
    moisture_plot = Plot(moisture_data_dict)
    moisture_plot.create_lineplot(limit_x_label=True)
