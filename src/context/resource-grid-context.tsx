import React, { createContext, Dispatch, useReducer, useContext } from 'react'
import { Columns, ResourceGrid } from 'types/resources'

type ResourceGridAction =
  | {
      type: 'UPDATE_GRID'
      payload: ResourceGrid
    }
  | {
      type: 'NEW_GRID'
      payload: ResourceGrid
    }

export const ResourceGridReducer: React.Reducer<
  ResourceGrid,
  ResourceGridAction
> = (state, action) => {
  switch (action.type) {
    case 'UPDATE_GRID': {
      return { ...state, ...action.payload }
    }

    default:
      return state
  }
}

const initialState: ResourceGrid = {
  columns: undefined,
  rows: undefined,
  defaultColumns: [],
  selectedColumns: [],
  data: [],
  filters: []
}

type IResourceGridContext = ResourceGrid | undefined
type IResourceGridDispatchContext = Dispatch<ResourceGridAction> | undefined

const ResourceGridContext = createContext<IResourceGridContext>(undefined)
const ResourceGridDispatchContext = createContext<IResourceGridDispatchContext>(
  undefined
)

const ResourceGridProvider: React.FC = ({ children }) => {
  const [state, dispatch] = useReducer(ResourceGridReducer, initialState)
  return (
    <ResourceGridContext.Provider value={state}>
      <ResourceGridDispatchContext.Provider value={dispatch}>
        {children}
      </ResourceGridDispatchContext.Provider>
    </ResourceGridContext.Provider>
  )
}

const useResourceGrid = () => {
  const state = useContext(ResourceGridContext)
  const dispatch = useContext(ResourceGridDispatchContext)

  if (state === undefined || dispatch === undefined) {
    throw new Error('views must be used within ResourceGridProvider')
  }

  return { state, dispatch }
}

export {
  ResourceGridProvider,
  useResourceGrid,
  ResourceGridContext,
  ResourceGridDispatchContext
}
