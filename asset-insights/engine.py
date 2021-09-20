import flask
import requests_cache
import requests
import json
import os
from datetime import datetime
from collections import OrderedDict
from collections import defaultdict

from analytics_sdk.utilities import (
    BASE_API_URL,
    get_msp_id,
    call_get_requests,
    call_post_requests,
    get_jwt_token
)

from utils import get_epoc_from_datetime_string

requests_cache.install_cache('opsramp_cache', backend='sqlite', expire_after=3600*300, allowable_methods=("GET", "POST"))

APP_SERVICE_BASE_URL = os.getenv('APP_SERVICE_BASE_URL', '')

def get_tenants():
    flask.session['test-file'] = "New file"
    msp_id = get_msp_id()
    url = BASE_API_URL + f'/api/v2/tenants/{msp_id}/clients/minimal'
    res = call_get_requests(url, verify=False)
 
    if not res.ok:
        return []
    return res.json()


def get_metric_names():
    metric_names = {
        "inventoryOnly": {
            "unweighted": "usage_resource_InventoryOnly_unweighted",
            "weighted": "usage_resource_InventoryOnly_weighted"
        },
        "eventsOnly": {
            "unweighted": "usage_resource_EventsOnly_unweighted",
            "weighted": "usage_resource_EventsOnly_weighted"
        },
        "upDownOnly": {
            "unweighted": "usage_resource_UpDownOnly_unweighted",
            "weighted": "usage_resource_UpDownOnly_weighted"
        },
        "fullyManaged": {
            "unweighted": "usage_resource_FullyManaged_unweighted",
            "weighted": "usage_resource_FullyManaged_weighted"
        }
    }

    return metric_names

def get_metric_value(tenant_id, metric_name, function, resource_type, start, end):
    url = BASE_API_URL + f'/metricsql/api/v7/tenants/{tenant_id}/metrics'
    metric = f'{metric_name}{{resourceType="{resource_type}"}}' if resource_type else metric_name
    metric = f'{function}({metric})' if function else metric
    
    start_timestamp = int(get_epoc_from_datetime_string(start))
    end_timestamp = int(get_epoc_from_datetime_string(end))
    
    params = {
        "query": metric,
        "start": start_timestamp,
        "end": end_timestamp,
        "step": 86400, #not present in metered usage
        "encode": "true"  
    }
    
    res = call_get_requests(url, params, verify=False)
    
    if not res.ok:
        return {"status": "fail"}
    return res.json()


#Total managed resource types
def get_managed_resources():
    msp_id = get_msp_id()
    var=get_jwt_token()
    resource_types = []
    url = BASE_API_URL + f'/opsql/api/v7/tenants/{msp_id}/queries'
    data = {
    "objectType" : "resource",
    "filterCriteria": "",
    "groupBy": ["partnerId"],
    "aggregateFunction": "count",
    "sortBy" : "partnerId"
    }
    ACCESS_HEADER = {"Content-Type" : "application/json" ,"Accept" : "application/json" , "Authorization" : f'Bearer {get_jwt_token()}'}
    res =  requests.post(url , data=json.dumps(data), headers=ACCESS_HEADER, verify=False);
    if not res.ok:
        return[]

    resource_types = res.json()['results'][0]['count']
    
    return resource_types
    

def get_managed_resources_breakdown_time(start_date, end_date):
    tenants = get_tenants()
    metric_names = get_metric_names()
    resp = {}

    for metric_name, types in metric_names.items():
        for tenant in tenants:
            tenant_id = tenant['uniqueId']
            unweighted = get_metric_value(tenant_id, types['unweighted'], "", None, start_date, end_date)
            if unweighted['status'] == 'success' and unweighted['data']['result']:
                values = unweighted['data']['result'][0]['values']
    
                for value in values:
                    if value[0] in resp:  # EPOC
                        resp[value[0]] += float(value[1])
                    else:
                        resp[value[0]] = float(value[1])
    
    return resp


def get_breakdown_top_resource_type(start_date, end_date):
    msp_id = get_msp_id()
    resp = []
    count = 0
    page_no=1
    nextPage= True

    while (nextPage != False):
        url = BASE_API_URL + f'/opsql/api/v7/tenants/{msp_id}/queries'

        data={
                "objectType" : "resource",
                "filterCriteria": "",
                "groupBy": ["type"],
                "aggregateFunction": "count",
                "sortBy" : "type",
                "pageNo": page_no,
                "pageSize": 100
        }
        ACCESS_HEADER = {"Content-Type" : "application/json" ,"Accept" : "application/json" , "Authorization" : f'Bearer {get_jwt_token()}'}
        res =  requests.post(url , data=json.dumps(data), headers=ACCESS_HEADER, verify=False);

        if not res.ok:
            return resp

        if "results" not in res.json() or len(res.json()['results'])==0 :
            return resp

        for result in (res.json()['results']):
            if 'count' not in result:
                continue
            if 'type' not in result:
                continue
            _count=result['count']

            _type=result['type']

            if _count == []:
                _count=0
            if _type == []:
                _type='Other'

            resp.append({ 'name': _type, 'count': _count })
        if "nextPage" not in res.json():
            return resp

        nextPage=res.json()['nextPage']
        page_no+=1
    
    return resp


#Top Clients By Total Managed Resources
def get_breakdown_top_clients_total_managed_resources(start_date, end_date):
    msp_id = get_msp_id()
    
    resp = []
    count = 0
    page_no=1
    nextPage= True
    while (nextPage != False):
        url = BASE_API_URL + f'/opsql/api/v7/tenants/{msp_id}/queries'

        data={
               "objectType" : "resource",
               "filterCriteria": "",
               "groupBy": ["clientId"],
               "aggregateFunction": "count",
               "sortBy" : "clientId",
               "pageNo": page_no,
               "pageSize": 100
           }
        ACCESS_HEADER = {"Content-Type" : "application/json" ,"Accept" : "application/json" , "Authorization" : f'Bearer {get_jwt_token()}'}
        res =  requests.post(url , data=json.dumps(data), headers=ACCESS_HEADER, verify=False);
        if not res.ok:
            return resp

        if "results" not in res.json() or len(res.json()['results'])==0 :
            return resp

        for result in (res.json()['results']):
            if 'count' not in result:
                continue
            if 'clientId' not in result:
                continue
            _count=result['count']

            _clientId=result['clientId']

            if _count == []:
                _count=0
            if _clientId == []:
                _clientId='Other'

            resp.append({ 'clientId': _clientId, 'count': _count })
        if "nextPage" not in res.json():
            return resp

        nextPage=res.json()['nextPage']
        page_no+=1
    
    return resp



def get_breakdown_public_cloud_data_center(start_date, end_date):
    msp_id = get_msp_id()
    pc_resp = []
    dc_resp = []
    resp = []
    pc_count=0
    dc_count=0
    page_no=1
    nextPage= True

    while (nextPage != False):
        url = BASE_API_URL + f'/opsql/api/v7/tenants/{msp_id}/queries'

        data={
                "objectType" : "resource",
                "filterCriteria": "",
                "groupBy": ["make"],
                "aggregateFunction": "count",
                "sortBy" : "make",
                "pageNo": page_no,
                "pageSize": 100
            }
        ACCESS_HEADER = {"Content-Type" : "application/json" ,"Accept" : "application/json" , "Authorization" : f'Bearer {get_jwt_token()}'}
        res =  requests.post(url , data=json.dumps(data), headers=ACCESS_HEADER, verify=False);
        if not res.ok:
            return resp

        if "results" not in res.json() or len(res.json()['results'])==0 :
            return resp

        for result in (res.json()['results']):
            if 'count' not in result:
                continue
            if 'make' not in result:
                continue
            _count=result['count']

            _make=result['make']

            if _count == []:
                _count=0
            if _make == []:
                _make='Other'

            if (_make == 'AZURE' or _make == 'AWS' or _make == 'GOOGLE' or _make == 'Google' or _make == 'ALIBABA' or _make == 'Google\n'):
                pc_resp.append({ 'make': _make, 'count': _count })
            else:
                dc_resp.append({ 'make': _make, 'count': _count })

        if "nextPage" not in res.json():
            return resp

        nextPage=res.json()['nextPage']
        page_no+=1
    for i in range (len(pc_resp)):
        pc_count+=pc_resp[i]['count']
    
    for j in range (len(dc_resp)):
        dc_count+=dc_resp[j]['count']
    
    resp.append({'name': 'Public Cloud', 'count': pc_count})
    resp.append({'name': 'Data Center', 'count': dc_count})

    return resp


#Resource Composition By Public Cloud
def get_breakdown_resource_composition_public_cloud(start_date, end_date):
    msp_id = get_msp_id()

    pc_resp = []

    nextPage= True
    page_no=1

    while (nextPage != False):
        url = BASE_API_URL + f'/opsql/api/v7/tenants/{msp_id}/queries'

        data={
                "objectType" : "resource",
                "filterCriteria": "",
                "groupBy": ["make"],
                "aggregateFunction": "count",
                "sortBy" : "make",
                "pageNo": page_no,
                "pageSize": 100
            }
        ACCESS_HEADER = {"Content-Type" : "application/json" ,"Accept" : "application/json" , "Authorization" : f'Bearer {get_jwt_token()}'}
        res =  requests.post(url , data=json.dumps(data), headers=ACCESS_HEADER, verify=False);

        if not res.ok:
            return pc_resp

        if "results" not in res.json() or len(res.json()['results'])==0 :
            return pc_resp

        for result in (res.json()['results']):
            if 'count' not in result:
                continue
            if 'make' not in result:
                continue
            
            _count=result['count']

            _make=result['make']


            if _count == []:
                _count=0
            if _make == []:
                _make='Other'

            if (_make == 'AZURE' or _make == 'AWS' or _make == 'GOOGLE' or _make == 'Google' or _make == 'ALIBABA' or _make == 'Google\n'):
                pc_resp.append({ 'make': _make, 'count': _count })

        if "nextPage" not in res.json():
            return pc_resp

        nextPage=res.json()['nextPage']
        page_no+=1

    return pc_resp



#Breakdown by operating system
def get_breakdown_by_operating_system(start_date, end_date):
    msp_id = get_msp_id()

    resp = []
    page_no=1
    nextPage= True
    while (nextPage != False):
        url = BASE_API_URL + f'/opsql/api/v7/tenants/{msp_id}/queries'
        data={
                "objectType" : "resource",
                "filterCriteria": "type = 'Server'",
                "groupBy": ["osName"],
                "aggregateFunction": "count",
                "sortBy" : "osName",
                "descendingOrder": "true",
                "pageNo": page_no,
                "pageSize": 100
            }

        ACCESS_HEADER = {"Content-Type" : "application/json" ,"Accept" : "application/json" , "Authorization" : f'Bearer {get_jwt_token()}'}
        res =  requests.post(url , data=json.dumps(data), headers=ACCESS_HEADER, verify=False);
        
        if not res.ok:
            return resp

        if "results" not in res.json() or len(res.json()['results'])==0 :
            return resp

        for result in (res.json()['results']):
            if 'count' not in result:
                continue
            if 'osName' not in result:
                continue
            _count=result['count']

            _osName=result['osName']


            if _count == []:
                _count=0
            if _osName == [] or _osName == '' :
                _osName='Other'


            resp.append({ 'osName': _osName, 'count': _count })
        if "nextPage" not in res.json():
            return resp

        nextPage=res.json()['nextPage']
        page_no+=1
    
    return resp

#Get Excel Data
def get_excel_data(data):
    data_1 = [["Resource Tier", "Usage (Unweighted)", "Usage (Weighted)"]]
    for key, val in data['breakdown_time'].items():
        data_1.append([key.title(), val['unweighted'], val['weighted']])

    resp = {
        'sheets': [
            {
                'title': 'Overview',
                'header': {},
                'sections': [
                    {
                        'type': 'table',
                        'title': 'Usage Breakdown by resource tier',
                        'title-color': 'red',
                        'start-row': 1,
                        'start-col': 1,
                        'data': data_1
                    }
                ]
            }
        ]
    }

    return resp


def _compute(start_date, end_date):

    resp = {
        'managed_resources': get_managed_resources(),
        'breakdown_time': get_managed_resources_breakdown_time(start_date, end_date),
        'breakdown_top_resource_type': get_breakdown_top_resource_type(start_date, end_date),
        'breakdown_top_clients_managed_resource': get_breakdown_top_clients_total_managed_resources(start_date, end_date),
        'public_cloud_data_center': get_breakdown_public_cloud_data_center(start_date, end_date),
        'resource_composition': get_breakdown_resource_composition_public_cloud(start_date, end_date),
        'breakdown_operating_system': get_breakdown_by_operating_system(start_date, end_date)
    }
    
    excel_data = get_excel_data(resp)
    resp['excel-data'] = excel_data

    return resp
    
def compute():
    params = flask.request.get_json()
    start_date = params.get('start_date', None)
    end_date = params.get('end_date', None)
    analysis_id = params.get('analysis_id', None)   

    # analysis run
    url = APP_SERVICE_BASE_URL + '/analysis-runs/'
    data = {
        'analysis': analysis_id,
        'params': json.dumps(params),
    }

    analysis_run = requests.post(url, data).json()
    run_id = analysis_run["id"]   

    # run compute
    result = _compute(start_date, end_date)
    flask.session[run_id] = json.dumps(result.copy())   

    # update the run  
    url = APP_SERVICE_BASE_URL + f'/analysis-runs/{run_id}/' 
    data = {
        'date_completed': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        'result': json.dumps(result.copy())
    }
    requests.patch(url, data).json()    

    resp = {
        'analysis': analysis_id,
        'analysis-run': run_id  
    }
    return resp

