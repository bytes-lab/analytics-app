import React from 'react'
import Sidebar from 'components/sidebar'
import Topology from 'modules/topology'

export default function TopologyScreen() {
  return (
    <div className="infrastructure-wrapper">
      <Sidebar />

      <div className="w-100 p-4">
        <div className="topology-container">
          <Topology />
        </div>
      </div>
    </div>
  )
}
