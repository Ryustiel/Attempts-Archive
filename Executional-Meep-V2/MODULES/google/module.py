import requests
from bs4 import BeautifulSoup

def google_get(query, display=False):
    """
    fetch
    return structure : 
    """
    url = "http://www.google.com/search?"
    url += "start=0"
    url += "&num=" + str(10)
    url += "&q=" + query.replace(" ", "+")
    url += "&cr=" + "countryUS" # option list : https://developers.google.com/custom-search/docs/xml_results_appendices#countryCollections
    url += "&lr=" + "lang_en"

    response = requests.get(url)

    if display:
        with open("MODULES/google/visualize.html", "w") as f:
            f.write(response.text)

    return response


def google_get_results(query):
    """
    returns : {name: url}
    """
    soup = BeautifulSoup( google_get(query, display=True).text, "html.parser" )
    results = soup.find_all('div', attrs={"class": "Gx5Zad fP1Qef xpd EtOod pkphOe"}) # "egMi0 kCrYT" : only search result (and no peek related additionnal links)

    data = []

    for result in results:
        data_link = result.find('a')['href'][7:]
        data_text = result.find('div', attrs={'class': 'BNeawe vvjwJb AP7Wnd'}).string # that one is necessary
        data_desc = result.find('div',attrs={'class': "BNeawe s3v9rd AP7Wnd"})
        data_link_desc = result.find('div', attrs={'class': "BNeawe UPmit AP7Wnd"})

        if data_link_desc is not None:
            data_link_desc = data_link_desc.string
        else:
            data_link_desc = ""

        if data_desc is not None:
            data_desc = data_desc.string
        else:
            data_desc = "" 

        data.append( {"text": data_text, "link": data_link, "desc": data_desc, "link_desc": data_link_desc} )

    return data


    domain = url.split("/")[2][4:]

