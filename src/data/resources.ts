import { useQuery } from 'react-query'
import * as resourcesApi from 'api/resources-api'

function useResourceAttributes(clientId?: number) {
  return useQuery(['resource-attributes'], () =>
    resourcesApi.getResourceAttributes(clientId)
  )
}
export { useResourceAttributes }
