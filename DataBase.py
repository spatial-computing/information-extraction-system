__author__ = 'shilpagulati'

import json

JsonObj = open("SimilarityResults.json").read()
data = json.loads(JsonObj)


def update_file(country, user_input, similarities_list):

    flag = 0
    if country not in data:
        data[country] = [{"UserInput": user_input,"Similarities": similarities_list}]
    else:
        for each in data[country]:
            if user_input == each["UserInput"]:
                each["Similarities"] = similarities_list
                flag = 1
                break
        if flag == 0:
            data[country].append({"UserInput": user_input,"Similarities": similarities_list})
    with open('SimilarityResults.json', 'w') as outfile:
        json.dump(data,outfile)
    outfile.close()


def get_data(country, user_input):
    if country in data:
        for each in data[country]:
            if user_input == each["UserInput"]:
                return each["Similarities"]










