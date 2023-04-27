import numpy as np
from constants import ROBOT, NORM_ENCODERS_FUNC

def getLocType(item, method = "item"):
    """
    @item = Robot item = {"name": "loc_type", ...} or @item = string = "loc_type"
    @method = "item" for robot item or "string" for string

    returns (loc, type)

    fails -> get None error
    """
    split = None
    if method == "item":
        split = item["name"].split("_")
    else:
        split = item.split("_")

    loc, type = split[0], split[-1]
    return loc, type

def getItemByName(name, arrayDicts = ROBOT):
    """
    Returns the dictionary in array_of_dicts that has a "name" key with the value of name.
    If no dictionary is found with a matching name, returns None.
    """
    for d in arrayDicts:
        if d.get("name") == name:
            return d
        
    print(f"ERROR @getItemBYNAME: no item of name: {name} found")
    return None

# return the wheel_dia that reduces the error for the encoders based on the data collected from experiment
#NOTE this takes in the encoder value difference from a start stop sequence, will not normalize correctly if just passed the current encoder readings
def normEncodersFunc(encoder_ticks, func = NORM_ENCODERS_FUNC):

    func_output = 0
    for i, coef in enumerate(func):
        func_output += coef * np.log(encoder_ticks)**(len(func) - (i+1))

    return func_output


