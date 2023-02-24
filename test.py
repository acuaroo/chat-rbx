def filter_text(string):
    string = string.replace("[","*[")
    string = string.replace("]:","]:*")

    split_string = string.split("*")

    res = []

    for i in split_string:
        if len(i)!=0:
            if (i.find("[") and i.find("]:")):
                res.append(i)
                
    res=" ".join(res)

    return res


print(filter_text("[su] [acuaro]: sus hahaha adhifbidahbfa"))