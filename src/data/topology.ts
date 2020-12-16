import { useQuery } from 'react-query'
import { fetchTopology } from 'api/topology'

export function useTopology(
  clientId: string,
  resourceId: string,
  depth?: number
) {
  return useQuery(['topology', clientId, resourceId, depth], fetchTopology, {
    enabled: clientId !== 'client_0'
  })
}
