from analytics_sdk.utilities import get_run_result


#get total managed resources
def get_managed_resources(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('managed_resources', {})

#Managed Resources(bar-graph)
def get_managed_resources_breakdown_time(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('breakdown_time', {})

#Top Resource types
def get_breakdown_top_resource_type(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('breakdown_top_resource_type', {})

#Top clients by total managed resources
def get_breakdown_top_clients_total_managed_resources(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('breakdown_top_clients_managed_resource', {})

#Public cloud vs data center
def get_breakdown_public_cloud_data_center(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('public_cloud_data_center', {})

#Resource cmposition by public cloud
def get_breakdown_resource_composition_public_cloud(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('resource_composition', {})

#Breakdown by operating system (servers)
def get_breakdown_by_operating_system(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('breakdown_operating_system', {}) 
