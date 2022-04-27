import os
from typing import Dict
import matplotlib.pyplot as plt

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

    def create_lineplot(self):
        '''Create a plot with the number of x,y sets defined'''
        plt.xlabel(self.data["x_label"])
        plt.ylabel(self.data["y_label"])
        for set in range(0, len(self.data["x_data"])):
            self.ax.plot(self.data["x_data"][set], self.data["y_data"][set], label=self.data["label"][set])
        self.ax.legend()
        plt.show()

    def save_plot(self, path, plot_name):
        '''Save plot as png'''
        plot_name = plot_name + ".png"
        plt.savefig(os.path.join(path, plot_name))

if __name__ == "__main__":
    from DatabaseHandler import DataBaseHandler

    database_handler = DataBaseHandler()
    database_handler.connect_to_database("Planty2")
    x_axis = database_handler.select_from_table("Planty_data", ["Datetime"], True, "Datetime", 10)
    y_axis = database_handler.select_from_table("Planty_data", ["light"], True, "Datetime", 10)
    print(type(x_axis[0][0]))
    time = x_axis[5][0].time()
    #print(datetime(x_axis[0][0]))
    for x in x_axis:
        print(x[0])
    for y in y_axis:
        print(y[0])

    for dt in x_axis:
        dt = dt[0].time()

    print("Test plot")
    x_label = "x"
    y_label = "y"
    x1 = [1,2,3,4,5,6,7,8,9,10]
    y1 = [1,2,3,4,5,6,7,8,9,10]
    x2 = [5,6,7,8,9,10,11,12,13,14]
    y2 = y1
    labels = ["label 1"]
    data = {"x_label" : x_label,
            "y_label" : y_label,
            "x_data" : [x_axis],
            "y_data" : [y_axis],
            "label" : labels}
    path = ""
    name = "test_plot"

    plot = Plot(data)
    plot.create_lineplot()
    plot.save_plot(path, name)