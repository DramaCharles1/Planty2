from typing import Dict

def PlantyModel() -> Dict[str,str]:
    '''SQL planty Table model'''
    model = {"entry" : "entry INT NOT NULL",
    "plant" : "plant VARCHAR(10) NOT NULL",
    "motor_duration" : "motor_duration INT NOT NULL",
    "motor_power" : "motor_power INT NOT NULL",
    "temperature" : "temperature FLOAT NOT NULL",
    "humidity" : "humidity FLOAT NOT NULL",
    "light" : "light INT NOT NULL",
    "light_wo_regulator" : "light_wo_regulator INT NOT NULL",
    "moisture" : "moisture FLOAT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"
    }
    return model

def CameraModel() -> Dict[str,str]:
    '''SQL camera Table model'''
    model = {"entry" : "entry INT NOT NULL",
    "original_pixel" : "original_pixel INT NOT NULL",
    "green_pixel" : "green_pixel INT NOT NULL",
    "green_percent" : "green_percent FLOAT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"}
    return model

def PlantySettingsModel() -> Dict[str,str]:
    '''SQL settings Table model'''
    model = {"motor_duration" : "motor_duration INT NOT NULL",
    "motor_power" : "motor_power INT NOT NULL",
    "moisture_samples" : "moisture_samples FLOAT NOT NULL",
    "moisture_threshold" : "moisture_threshold FLOAT NOT NULL",
    "kp" : "kp FLOAT NOT NULL",
    "ki" : "ki FLOAT NOT NULL",
    "integration_time" : "integration_time INT NOT NULL",
    "light_setpoint" : "light_setpoint INT NOT NULL",
    "max_light" : "max_light INT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"}
    return model

def CameraSettingsModel() -> Dict[str,str]:
    model = {"picture_directory" : "picture_directory VARCHAR(20) NOT NULL",
    "picture_copy_directory" : "picture_copy_directory VARCHAR(20) NOT NULL",
    "l1" : "l1 INT NOT NULL",
    "l2" : "l2 INT NOT NULL",
    "l3" : "l3 INT NOT NULL",
    "u1" : "u1 INT NOT NULL",
    "u2" : "u2 INT NOT NULL",
    "u3" : "u3 INT NOT NULL",
    "datetime" : "datetime DATETIME NOT NULL"}
    return model