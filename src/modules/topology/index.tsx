import React, { useState } from 'react'
import { Chart } from 'regraph'
import { useTopology } from 'data/topology'
import { useConvertDataIntoNode } from './use-convert-data-into-node'
import { useUserNavInfo } from 'context/nav-context'
import './index.scss'

export default function Topology() {
  const [resourceId, setResourceId] = useState<string>('228278')
  const [depth, setDepth] = useState(3)
  const [layout, setLayout] = useState<Chart.LayoutOptions['name']>('organic')

  const { clientUuid } = useUserNavInfo()
  const { data } = useTopology(clientUuid, resourceId, depth)
  const items = useConvertDataIntoNode(data)

  function onSelectResourceId(event: React.ChangeEvent<HTMLSelectElement>) {
    setResourceId(event.target.value)
  }

  function onSelectDepth(event: React.ChangeEvent<HTMLSelectElement>) {
    setDepth(parseInt(event.target.value))
  }

  function onSelectLayout(event: React.ChangeEvent<HTMLSelectElement>) {
    setLayout(event.target.value as Chart.LayoutOptions['name'])
  }

  return (
    <>
      <div>
        <label>HostName/IPAddress</label>
        <select
          onChange={onSelectResourceId}
          className="border mx-5"
          defaultValue={resourceId}
        >
          <option value="194923">everest-ubuntu-ui01 (172.25.20.80)</option>
          <option value="208058">K3S-containerd (10.42.1.4)</option>
          <option value="207958">K3S-Docker (10.42.1.3)</option>
          <option value="228278">OKD-Lab (10.129.0.2)</option>
          <option value="181703">TestforBalancing (10.4.2.23)</option>
        </select>

        <label>Depth</label>
        <select
          onChange={onSelectDepth}
          className="border mx-5"
          defaultValue={depth}
        >
          <option value={1}>1</option>
          <option value={2}>2</option>
          <option value={3}>3</option>
          <option value={4}>4</option>
          <option value={5}>5</option>
        </select>

        <label>Layout</label>
        <select
          onChange={onSelectLayout}
          className="border ml-5"
          defaultValue={layout}
        >
          <option value="organic">Default</option>
          <option value="sequential">Hierarchical</option>
        </select>
      </div>
      <div className="chart-wrapper">
        <Chart items={items} layout={{ name: layout }} />
      </div>
    </>
  )
}
