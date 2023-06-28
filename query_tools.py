import urllib3  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import json
import requests

from payloads import payload



def Get_Wking_UserCount():
    session = requests.session()
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer glsa_qOHsDNPG4z8Hr87LlXgpBzQokb91s2Xn_79ffa6a3'   
    }
    #response = session.get('https://wking-users.owin.info/api/User/onlineusers', headers = headers, verify=False)
    response = session.get('http://192.168.82.160:30196/api/User/onlineusers', headers = headers, verify=False)
    user_count = json.loads(response.content).split()[-1]
    session.close()
    return user_count

def Get_Domain_Rank(serverId="9", size=5, range=1):
    session = requests.session()
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer glsa_qOHsDNPG4z8Hr87LlXgpBzQokb91s2Xn_79ffa6a3'   
    }
    # How many domains
    payload["aggs"]["0"]["terms"]["size"] = size
    # Time range
    payload["query"]["bool"]["filter"][0]["range"]["timeISO8601"]["gte"] = f"now-{str(range)}h"
    # Which Site
    payload["query"]["bool"]["filter"][1]["bool"]["should"]["match"]["serverId"] = serverId
    response = session.get('https://elastic.owin.info/goedge-*/_search', headers = headers, data = json.dumps(payload))
    domain_rank = json.loads(response.content)['aggregations']['0']['buckets']
    session.close()
    return domain_rank

if __name__ == "__main__" :
    x = Get_Wking_UserCount()
    print(x)