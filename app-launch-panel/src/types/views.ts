export type View = {
  createdBy: Number
  createdTime: Number
  entityType: String
  id: Number
  orgId: Number
  updatedTime?: Number
  version: Number
  viewProperties: ViewProperties
  visibility: String
}

export type ViewProperties = {
  active?: Boolean
  label?: String
  name?: String
  query?: string
  url?: String
}
