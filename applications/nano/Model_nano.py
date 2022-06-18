from typing import Dict

def NanoModel() -> Dict[str,str]:
    '''SQL test Table model'''
    model = {"plant" : "plant VARCHAR(10) NOT NULL",
    "motor_duration" : "motor_duration INT NOT NULL",
    "motor_power" : "motor_power INT NOT NULL"}
    return model
