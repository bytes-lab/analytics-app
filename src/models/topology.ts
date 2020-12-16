import { Index, Node, Link, Chart } from 'regraph'

export type Nodes = Index<Node<Chart> & { nodeData?: any }>

export type Links = Index<Link<Chart>>

export type RawGraph = {
  vertices: Vertice[]
  edges: Edge[]
}

export type Vertice = {
  key: VerticeKey
  properties: VerticeProperties
}

type VerticeKey = {
  id: number
  entityType: string
}

type VerticeProperties = {
  name: string
} & any

export type Edge = {
  src: VerticeKey
  dest: VerticeKey
  label: string
}
