import { Chart, Items, NodeLabel, LinkStyle } from 'regraph'
import { RawGraph, Vertice, Nodes, Edge, Links } from 'models/topology'

const nodeColor = 'rgb(100, 189, 100)'

const labelStyle: NodeLabel = {
  center: false
}

const linkStyle: LinkStyle<Chart> = {}

export function useConvertDataIntoNode(data?: RawGraph) {
  if (!data) {
    return
  }

  const items: Items = {
    ...makeNodes(data.vertices),
    ...makeLinks(data.edges)
  }

  return items
}

function makeNodes(vertices: Vertice[]): Nodes {
  const nodes: Nodes = {}

  vertices.forEach(vertice => {
    nodes[vertice.key.id] = {
      color: nodeColor,
      label: { text: vertice.properties.name, ...labelStyle },
      nodeData: vertice.properties
    }
  })

  return nodes
}

function makeLinks(edges: Edge[]): Links {
  const links: Links = {}

  edges.forEach(edge => {
    const id1 = String(edge.src.id)
    const id2 = String(edge.dest.id)
    const linkId = `${id1}-${id2}`

    links[linkId] = {
      id1,
      id2,
      end2: { arrow: true },
      ...linkStyle
    }
  })

  return links
}
