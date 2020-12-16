export type Resources = {
  csrfParam: String
  customAttrKey: String
  customAttrValue: String
  devices: Resource[]
  filterInfo: []
  newTab: Boolean
  success: Boolean
  summary: {}
  total: Number
}

export type ResourceGrid = {
  columns?: {
    autoMonitoring: Boolean
    columnsList: any
    selectedColumns: Column[]
    success: Boolean
    total: Number
  }
  rows?: Resources
  defaultColumns?: any[]
  selectedColumns?: any[]
  data?: any[]
  filters?: any[]
}

export type Resource = {
  activeStatus: String
  agentInstalled: Boolean
  agentPolicy: AgentPolicy
  policy: String
  agentType: Number
  aliasName: String
  alternateIP: String
  assetManagedTime: String
  assetManagedTimeStr: String
  associatedAlerts: String
  associatedIncidents: String
  classCode: String
  clientName: String
  cpu: {}
  currentLoggedOnUser: CurrentLoggedOnUser
  description: String
  deviceClass: DeviceClass
  deviceGroupName: String
  deviceState: String
  deviceType: DeviceType
  deviceUrl: String
  dnsName: String
  firmware: String
  firstAssetManagedTime: String
  firstAssetManagedTimeStr: String
  hostName: String
  id: Number
  instanceName: String
  ipAddress: String
  isDevice: Boolean
  lastPatchInstallDate: String
  make: String
  memory: {}
  model: String
  modifiedTime: String
  modifiedTimeStr: String
  name: String
  notes: String
  osName: String
  purchaseDate: String
  resourceIconTitle: String
  resourceUrl: String
  select: String
  serialNumber: String
  site: String
  sku: String
  snmp: Boolean
  sourceType: String
  status: Number
  storage: {}
  technologies: Technology[]
  type: String
  unSelectable: false
  underMaintenance: false
  warrantyDate: String
  wmi: false
  wsusEnabled: false
}

export type Columns = {
  autoMonitoring: Boolean
  columnsList: ColumnsList
  menuTitles: {}
  permissions: {}
  selectedColumns: Column[]
  success: Boolean
  total: Number
}

export type ColumnsList = {
  aliasName: Column
  alternateIP: Column
  assetManagedTime: Column
  associatedAlerts: Column
  associatedIncidents: Column
  consoles: Column
  currentLoggedOnUser: Column
  description: Column
  deviceType: Column
  firmware: Column
  firstAssetManagedTime: Column
  hostName: Column
  instanceName: Column
  instanceState: Column
  instanceType: Column
  ipAddress: Column
  launchTime: Column
  make: Column
  memoryINGB: Column
  model: Column
  modifiedTime: Column
  name: Column
  notes: Column
  osName: Column
  provisionSpace: Column
  serialNumber: Column
  site: Column
  sku: Column
  technologies: Column
  traits: Column
  usedSpace: Column
}

export type Column = {
  cellRenderer?: String | Function
  cellRendererFramework?: String | Function
  checkboxSelection?: Boolean
  customField?: Boolean
  field?: String
  formatter?: String
  headerCheckboxSelection?: Boolean
  headerCheckboxSelectionFilteredOnly?: Boolean
  id?: Number
  lockPosition?: Boolean
  sortable?: Boolean
  suppressMovable?: Boolean
  switchable?: Boolean
  title?: String
  visible?: Boolean
  width?: Number
}

type AgentPolicy = {
  id: Number
  policy: String
}

type CurrentLoggedOnUser = {
  name: String
}

type DeviceClass = {
  tip: String
  iconClass: String
}

type DeviceType = {
  id: Number
  name: String
  iconImg: String
}

type Technology = {
  tip: String
  iconClass: String
}

export type Statuses = {
  detailsURL: String
  pageNo: Number
  pageSize: Number
  success: String
  total: Number
  totalPages: Number
  data: Status
}

export type Status = {
  color: String
  id: String
  label: String
  name: String
  showEmpty: String
  value: Number
}
