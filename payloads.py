payload = {
    "aggs" : {
        "0": {
            "terms": {
                "field": "serverName.keyword",
                "order": {
                    "_count": "desc"
                },
                # VAR
                "size": ""
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
                        # VAR
                        "gte": "",
                        "lte": "now"
                    }
                }
            },
            {
                "bool": {
                    "should": {
                        "match": {
                            # VAR
                            "serverId": ""
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