def fill_parameters(text, parameters):
    filtered = []
    for t in text.split('{'):
        for p in t.split('}'):
            filtered.append(p)

    for i in range(len(filtered)):
        if i % 2 == 1:
            keyword = filtered[i]

            if keyword in parameters.keys():
                filtered[i] = parameters[keyword][0]

            elif keyword[:-1] in parameters.keys(): # naming parameters "blah2", "blah3"...
                indice = int( keyword[-1] )
                if indice <= len(parameters[keyword[:-1]]):
                    filtered[i] = parameters[keyword[:-1]][ indice - 1 ]
                else:
                    filtered[i] = "[NOT FOUND]"

            else:
                filtered[i] = "[NOT FOUND]"

    # building back the text
    text = ""
    for t in filtered:
        text += t
    return text

parameters = {
    "bleh": ["OwO"],
    "blih": ["EwE"],
    "blah": ["Blawaw", "Blawow", "IwI"]
}

line = "{bleh} blah {blih} blooh lbowh {blah} {blah2}{blah3} {blah4} b"

a = fill_parameters(line, parameters)

print(a)