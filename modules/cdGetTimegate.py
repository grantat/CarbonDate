import requests
import json

moduleTag = "timegate"

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) \
    Gecko/20100101 Firefox/48.0'}


def getMementos(uri):

    try:
        baseURI = ('http://memgator.cs.odu.edu/memento/json/19950101000000/' +
                   uri)
        response = requests.get(baseURI, headers=headers)
        resp = json.loads(response.text)
        earliest = resp["mementos"]["first"]["datetime"]
        return earliest
    except KeyboardInterrupt:
        exit()
    except:
        return ""


def getTimegate(url, outputArray, outputArrayIndex, verbose=False, **kwargs):
    estimated_date = getMementos(url)
    output = {"earliest": estimated_date}

    outputArray[outputArrayIndex] = estimated_date
    kwargs['displayArray'][outputArrayIndex] = output
    return output
