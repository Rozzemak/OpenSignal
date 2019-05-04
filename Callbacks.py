
def changeGraphCb(attr, old, new, action, eleId):
    print(attr + " changed from:[" + old + "]to[" + new + "]")
    action(eleId, new)
    return 0
