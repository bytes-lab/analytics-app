import React from 'react'
import { resourceStates } from './resource-states'

export const GridSummary: React.FC = () => {
  return (
    <div className="grid-summary">
      <div className="summaries">
        {resourceStates &&
          resourceStates.map(resourceState => (
            <div className="summary" key={resourceState.name}>
              <span className="name">{resourceState.name}</span>
              <span className="value" style={{ color: resourceState.color }}>
                {resourceState.total}
              </span>
            </div>
          ))}
      </div>
    </div>
  )
}
