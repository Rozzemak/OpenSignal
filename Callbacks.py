
def changeGraphCb(attr, old, new, action, eleId):
    print(attr + " changed from:[" + old + "]to[" + new + "]")
    action(eleId, new, old)
    return 0
