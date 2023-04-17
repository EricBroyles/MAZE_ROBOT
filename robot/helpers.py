from constants import ROBOT

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
