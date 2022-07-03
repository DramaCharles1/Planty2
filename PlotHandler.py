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
        #plt.show()

    def save_plot(self, path, plot_name):
        '''Save plot as png'''
        plot_name = plot_name + ".png"
        plt.savefig(os.path.join(path, plot_name))

if __name__ == "__main__":
    from DatabaseHandler import DataBaseHandler
    print("test plot")
    DATABASE = "nano"
    TABLE = "nano_data"
    day_length = 23
    database_handler = DataBaseHandler()
    database_handler.connect_to_database(DATABASE)

    data = database_handler.select_from_table(TABLE, ["Datetime","moisture_1","moisture_2"], True, "Datetime", day_length)
    if len(data) < day_length:
        data = database_handler.select_from_table(TABLE, ["Datetime","moisture_1","moisture_2"], True, "Datetime", len(data) - 1)

    timex = [str(x[0].time().isoformat(timespec='minutes')) for x in data]
    moisture_plant1 = [y[1] for y in data]
    moisture_plant2 = [y[2] for y in data]

    print(len(moisture_plant1))
    print(len(timex))

    moisture_plant1_data_dict = {"x_label" : "Time",
                "y_label" : "test",
                "x_data" : [timex, timex],
                "y_data" : [moisture_plant1, [500] * len(data)],
                "label" : ["Moisture", "Limit"]}

    moisture_plot1 = Plot(moisture_plant1_data_dict)
    moisture_plot1.create_lineplot(limit_x_label=True)
    moisture_plot1.save_plot("/media/pi/USB/nano/test", "moisture_plant1_plot_day")
