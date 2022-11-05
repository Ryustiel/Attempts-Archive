"""
trying to use that as some kind of bot brain
"""

def send_query(): # IMPLEMENT REQUEST DELAYS TO REMAIN DESCREET
    ...

def chatbot_decision_making(): 
    """
    gives :
    - user query
    - list of categories of functions to get 
    
    returns the category name

    checks if the output is a category

    2nd roll : 
    - user query again
    - list of functions of the category queried

    returns the function to execute (one or many)

    checks if the output is a function


    if any check is false then repeat this function (until a trial limit)
    """
    ...


import requests
def api_call(url, method='post', parameters={}, **kwargs): # CREATE A GENERAL CLASS IN UTILITIES (to be modified in modules) =========>>>> MONITOR in and out web traffic

    first = True
    for (name, value) in parameters.items():
        if first:
            url += '?' + name + '=' + value.replace(' ', '+')
            first = False
        else:
            url += "&" + name + "=" + value.replace(' ', '+')

    print(url)

    for dict_ in kwargs.values():
        dict_ = {key.replace(" ", "+"): dict_[key].replace(' ', '+') for key in dict_.keys()} # kwargs values are mutable

    if method == "get":
        return requests.get(url, **kwargs)
    return requests.post(url, **kwargs)



url = 'https://api.openai.com/v1/edits/'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer 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'}
parameters = {}
json = {'model': '', 'input': 'hello world', 'instruction': ''}

#response = api_call(url, method='post', parameters=parameters, headers=headers, json=json)

with open('MODULES/codex/response.html', 'w') as f:
    #f.write(response.text)
    ...
