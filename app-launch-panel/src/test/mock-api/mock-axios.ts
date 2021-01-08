import axios from 'config/axios'
import data from 'test/mock-data/mock-response.json'
import * as _ from 'lodash'

const mockedAxios = axios as jest.Mocked<typeof axios>

const mockAxiosGet = (client: string, fail?: Boolean) =>
  mockedAxios.get.mockImplementation(async url => {
    if (
      _.find(data.mock.onboardStatus.clients, { id: client })?.response[0]
        .state !== 'NEW'
    ) {
      switch (url) {
        case `/api/v2/tenants/${client}/discoveryProfile/673/activityStatus`:
          return await Promise.resolve({
            data: data.mock.discoveryProfile.clients.find(
              el => el.id === client
            )?.response
          })

        case `api/v2/tenants/${client}/onboarding/status`:
          return await Promise.resolve({
            data: data.mock.onboardStatus.clients.find(el => el.id === client)
              ?.response[0].state
          })
        // case `api/v2/tenants/client_2/integrations/installed/search?pageNo=1&pageSize=100&queryString=category:CLOUD_INTEGRATION,STORAGE_INTEGRATION,NETWORK_INTEGRATION,COMPUTE_INTEGRATION`:
        //   return await Promise.resolve({
        //     data: data.mock.installedIntegrations.clients.filter(
        //       el => el.id === client
        //     )[0].result.data
        //   })

        case `api/v2/tenants/${client}/integrations/installed/search?pageNo=1&pageSize=100&queryString=category:CLOUD_INTEGRATION,STORAGE_INTEGRATION,NETWORK_INTEGRATION,COMPUTE_INTEGRATION`:
          return await Promise.resolve({
            data: data.mock.installedIntegrations.clients.filter(
              el => el.id === client
            )[0].result.data
          })
        case `${axios.defaults.baseURL}api/v2/tenants/client_2/integrations/installed/INTG-4d281b5b-5bbe-47eb-903b-63bcd61809d0/configFile/Kubernetes`:
          return await Promise.resolve({
            data: data.mock.Kubernetes.success.yaml.kubernetes
          })
        case `${axios.defaults.baseURL}api/v2/tenants/client_2/integrations/installed/INTG-4d281b5b-5bbe-47eb-903b-63bcd61809d0/configFile/statsDMonitoringKubernetes`:
          return await Promise.resolve({
            data: data.mock.Kubernetes.success.yaml.agent
          })

        case `${axios.defaults.baseURL}api/v2/tenants/client_2/integrations/installed/INTG-4d281b5b-5bbe-47eb-903b-63bcd61809d0/configFile/auto-detection-config-map`:
          return await Promise.resolve({
            data: data.mock.Kubernetes.success.yaml.agent
          })

        case `${axios.defaults.baseURL}api/v2/tenants/client_2/integrations/installed/INTG-4d281b5b-5bbe-47eb-903b-63bcd61809d0/configFile/creds-config-map`:
          return await Promise.resolve({
            data: data.mock.Kubernetes.success.yaml.agent
          })

        case `${axios.defaults.baseURL}api/v2/tenants/client_2/resources/a23c8a8d-7911-4ef4-b93e-cea7121fed9c`:
          if (fail) {
            return await Promise.resolve({
              status: 200,
              data: { agentInstalled: false, status: 'UNKNOWN' }
            })
          } else {
            return await Promise.resolve({
              data: { agentInstalled: true, status: 'INSTALLED' },
              status: 200
            })
          }
        default:
          return Promise.reject(new Error(`not found{${client} for ${url}}`))
      }
    } else {
      switch (url) {
        case `api/v2/tenants/${client}/onboarding/status`:
          return Promise.resolve({
            data: data.mock.onboardStatus.clients.find(el => el.id === client)
              ?.response[0].state
          })
        default:
          return Promise.reject(new Error(`not found{${client} for ${url}}`))
      }
    }
  })
const mockAxiosPost = (client: string) =>
  mockedAxios.post.mockImplementation(async url => {
    switch (url) {
      case `/api/v2/tenants/${client}/resources/advancedsearchES?pageNo=1&pageSize=100`:
        return await Promise.resolve({
          data: data.mock.advanceSearch.clients.find(el => el.id === client)
            ?.response
        })

      case `api/v2/tenants/${client}/onboarding/status`:
        return await Promise.resolve({ data: 'sucess' })
      case `/api/v2/tenants/${client}/integrations/install/KUBERNETES`:
        return await Promise.resolve({ data: data.mock.Kubernetes.success })
      default:
        return Promise.reject(new Error('not found'))
    }
  })
const mockAxiosDelete = (client: string, installedIntgId?: string) =>
  mockedAxios.delete.mockImplementation(async url => {
    switch (url) {
      case `/api/v2/tenants/${client}/integrations/installed/${installedIntgId}`:
        return await Promise.resolve({
          data: data.mock.advanceSearch.clients.find(el => el.id === client)
            ?.response
        })
      default:
        return Promise.resolve('Success')
    }
  })
export { mockAxiosGet, mockAxiosPost, mockAxiosDelete }
