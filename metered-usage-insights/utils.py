from analytics_sdk.utilities import get_run_result


def get_tenants(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('tenants', [])


def get_resource_types(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('resource_types', [])


def get_breakdown_resource_type(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('breakdown_resource_type', {})


def get_breakdown_client(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('breakdown_client', {})


def get_breakdown_time(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('breakdown_time', {})


def get_breakdown_resource_tier(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('breakdown_resource_tier', {})
