import pytest
import timeit
# import modules.cdGetArchives as tmap
import modules.cdGetTimegate as tgate
import json
import csv


def test_getTimegate():
    uri = "http://www.apple.com"
    date = tgate.getTimegate(uri, [''], 0, verbose=True,
                             displayArray={"": ""})
    assert len(date) > 0


@pytest.mark.skip(reason="Long wait time")
def test_longRunTimeGate():
    """ Long run testing gold standard data on Timegate """
    with open("./tests/data/gold_standard.csv", "r") as f, \
            open("./tests/data/timegate_responses.json", "w") as out:
        outJson = []
        reader = csv.reader(f)
        for row in reader:
            uri = row[0]

            start = timeit.default_timer()
            earliest = tgate.getMementos(uri)
            finish = timeit.default_timer()
            runtime = finish - start

            temp = {"uri": uri,
                    "earliest": earliest,
                    "runtime": runtime}
            outJson.append(temp)

        json.dump(outJson, out, indent=2)
