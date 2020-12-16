import axios from 'config/axios'
import { Resources, Columns, Statuses } from 'types/resources'

export async function getInventory(
  clientId: Number,
  mspId?: Number
): Promise<Resources> {
  // const url = `/newInventory.do?sort=name&order=ASC&limit=40&offset=0&dir=ASC&_ajax=true&action=list&locationTab=false&resourceGroupTab=false&discovered=false&searchStr=&deviceTypeId=3&deviceType_CategoryTypeId=&deviceGroupId=&serviceGroupId=&deviceLocationId=&gatewayDevices=false&showVoIPDevices=false&showWirelessLANDevices=false&showWLANControllers=false&cloudProviderId=0&sType=&showThickApDevices=false&type=&clientId=${clientId}&mspId=18&status=&customAttrValue=`
  const url = 'https://run.mocky.io/v3/b0e22bd9-992d-44be-9ffa-708500312116'
  const result = await axios.get(url)
  return result.data
}

export async function getColumns(): Promise<Columns> {
  const url = `/getListingConfig.json?listingType=DEVICE&resourceGroupTab=false&_ajax=true`
  const result = await axios.get(url)
  return result.data
}

export async function getStatuses(
  clientId: Number,
  mspId: Number
): Promise<Statuses> {
  const url = `/device.do?action=inventoryStatus&_ajax=true&locationTab=false&resourceGroupTab=false&discovered=false&searchStr=&deviceTypeId=3&deviceType_CategoryTypeId=&deviceGroupId=&serviceGroupId=&deviceLocationId=&gatewayDevices=false&showVoIPDevices=false&showWirelessLANDevices=false&showWLANControllers=false&cloudProviderId=0&sType=&showThickApDevices=false&type=&clientId=${clientId}&mspId=${mspId}&status=&customAttrValue=&customAttrKey=&limit=300`
  const result = await axios.get(url)
  return result.data
}

export async function getResourceAttributes(clientId?: Number) {
  const url = 'https://run.mocky.io/v3/ee084b53-a2a5-40f8-a7f8-07b29a041ef6'
  const result = await axios.get(url)

  return result.data.resourceAttributes
}

// TODO: will post device ids, and get statuses for each back...
// post data like: ?deviceIds=25203&agentsInstalled=true&sourceTypes=Linux&...(repeats for each id) then ..._csrf: 1ab3ed7b-d55b-4618-aff5-b17da124c3ad
export async function getResourceStatuses() {
  const url = `/deviceStatus.json`
  const result = await axios.post(url)
  // response: {"devices":{"195203":-2,"77698":-2,"20163":-2,"195208":-2,"25553":-2,"19858":1,"19668":-2,"19863":-2,"70233":-2,"19868":-2,"70238":-2,"74593":-2,"19873":-2,"74528":-2,"74533":-2,"19878":1,"74598":-2,"82598":-2,"25193":-2,"19883":1,"19948":1,"25198":-2,"19888":1,"19953":1,"61873":-2,"25203":-2,"19893":1,"195188":-2,"61878":-2,"25208":-2,"12473":-2,"19898":1,"195193":-2,"195198":-2,"19903":1},"success":true}
  return result.data
}

// TODO: not used yet but in old resources screen...
// post data like: ?deviceIds=25203&deviceIds=195198&deviceIds=195208&...
export async function getResourceMaintenance() {
  const url = `/deviceMaintenance.json`
  const result = await axios.post(url)
  // response: {"devices":{"19863":{"isMaintenance":false},"70238":{"isMaintenance":false},"70233":{"isMaintenance":false},"12473":{"isMaintenance":false},"19883":{"isMaintenance":false},"195193":{"isMaintenance":false},"74533":{"isMaintenance":false},"74598":{"isMaintenance":false},"25203":{"isMaintenance":false},"74593":{"isMaintenance":false},"25208":{"isMaintenance":false},"195203":{"isMaintenance":false},"195208":{"isMaintenance":false},"77698":{"isMaintenance":false},"19948":{"isMaintenance":false},"19903":{"isMaintenance":false},"195188":{"isMaintenance":false},"19888":{"isMaintenance":false},"19668":{"isMaintenance":false},"19868":{"isMaintenance":false},"19873":{"isMaintenance":false},"74528":{"isMaintenance":false},"19898":{"isMaintenance":false},"19953":{"isMaintenance":false},"19893":{"isMaintenance":false},"20163":{"isMaintenance":false},"61873":{"isMaintenance":false},"25553":{"isMaintenance":false},"61878":{"isMaintenance":false},"25193":{"isMaintenance":false},"25198":{"isMaintenance":false},"82598":{"isMaintenance":false},"195198":{"isMaintenance":false},"19878":{"isMaintenance":false},"19858":{"isMaintenance":false}},"success":true}
  return result.data
}
