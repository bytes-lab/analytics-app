from analytics_sdk.utilities import (
    BASE_API_URL,
    get_msp_id,
    call_get_requests
)


def get_clients_count():
    total_clients = '-'
    msp_id = get_msp_id()
    if msp_id:
        url = BASE_API_URL + f'/api/v2/tenants/{msp_id}/clients/search'
        res = call_get_requests(url, {}, False)
        total_clients = res.json()['totalResults']

    return total_clients


def get_resources_count():
    total_resources = '-'
    msp_id = get_msp_id()
    if msp_id:
        url = BASE_API_URL + f'/api/v2/tenants/{msp_id}/resources/search'
        res = call_get_requests(url, {}, False)
        total_resources = res.json()['totalResults']

    return total_resources
