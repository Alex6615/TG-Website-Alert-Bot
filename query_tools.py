import requests
import urllib3  
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def Get_Wking_UserCount():
    session = requests.session()
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer glsa_qOHsDNPG4z8Hr87LlXgpBzQokb91s2Xn_79ffa6a3'   
    }
    response = session.get('https://wking-users.owin.info/api/User/onlineusers', headers = headers, verify=False)
    user_count = json.loads(response.content).split()[-1]
    session.close()
    return user_count

def Get_Domain_Rank(size=5):
    session = requests.session()
    headers = {
        'Accept' : 'application/json',
        'Content-Type' : 'application/json',
        'Authorization' : 'Bearer glsa_qOHsDNPG4z8Hr87LlXgpBzQokb91s2Xn_79ffa6a3'   
    }
    payload = {
        "aggs" : {
            "0": {
                "terms": {
                    "field": "serverName.keyword",
                    "order": {
                        "_count": "desc"
                    },
                    "size": size
                }
            }
        },
        "size": 0,
        "script_fields": {},
        "stored_fields": [
            "*"
        ],
        "runtime_mappings": {},
        "query": {
            "bool": {
                "must": [],
                "filter": [
                {
                    "range": {
                        "timeISO8601": {
                            "format": "strict_date_optional_time",
                            "gte": "now-1h",
                            "lte": "now"
                        }
                    }
                },
                {
                    "bool": {
                        "should": {
                            "match": {
                                "serverId": "9"
                            }
                        }
                    }
                }
                ],
                "should": [],
                "must_not": []
            }
          }
        }
    response = session.get('https://elastic.owin.info/goedge-*/_search', headers = headers, data = json.dumps(payload))
    domain_rank = json.loads(response.content)['aggregations']['0']['buckets']
    session.close()
    return domain_rank

if __name__ == "__main__" :
    x = Get_Domain_Rank(10)
    print(x)