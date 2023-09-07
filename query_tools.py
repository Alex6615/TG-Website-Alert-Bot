import urllib3  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import json
import requests

from payloads import payload
from targets import wking_api, elastic_api


def Get_Wking_UserCount():
    session = requests.session()
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',  
    }
    response = session.get(wking_api, headers = headers, verify=False)
    user_count = json.loads(response.content).split()[-1]
    session.close()
    return user_count

def Get_Domain_Rank(serverId="9", size=5, range=1):
    session = requests.session()
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
    }
    # How many domains
    payload["aggs"]["0"]["terms"]["size"] = size
    # Time range
    payload["query"]["bool"]["filter"][0]["range"]["timeISO8601"]["gte"] = f"now-{str(range)}h"
    # Which Site
    payload["query"]["bool"]["filter"][1]["bool"]["should"]["match"]["serverId"] = serverId
    response = session.get(elastic_api, headers = headers, data = json.dumps(payload))
    domain_rank = json.loads(response.content)['aggregations']['0']['buckets']
    session.close()
    return domain_rank

if __name__ == "__main__" :
    pass
