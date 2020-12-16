import axios from 'config/axios'
import { RawGraph } from 'models/topology'

export async function fetchTopology(
  _: string,
  clientId: string,
  resourceId: string,
  depth = 5
): Promise<RawGraph> {
  const url = `api/v2/tenants/${clientId}/resources/${resourceId}/topology/gettopology?depth=${depth}`
  const result = await axios.get(url)

  return result.data
}
