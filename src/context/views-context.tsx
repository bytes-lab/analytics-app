import React, { createContext, Dispatch, useReducer, useContext } from 'react'
import { View } from 'types/views'

export type ViewsState = { views: View[]; activeView: View }

type ViewsAction =
  | {
      type: 'SET_VIEWS'
      payload: View[]
    }
  | {
      type: 'NEW_VIEW'
      payload: View
    }
  | {
      type: 'ACTIVE_VIEW'
      payload: View
    }

export const ViewsReducer: React.Reducer<ViewsState, ViewsAction> = (
  state,
  action
) => {
  switch (action.type) {
    // setting views
    case 'SET_VIEWS': {
      let active = action.payload.filter(
        v => v.viewProperties.active === true
      )[0]
      return { ...state, views: action.payload, activeView: active }
    }

    // addin a view to existing list
    case 'NEW_VIEW': {
      return {
        ...state,
        views: [...state.views, action.payload],
        activeView: action.payload
      }
    }

    // setting a  new active/current view
    case 'ACTIVE_VIEW': {
      return {
        ...state,
        views: [...state.views],
        activeView: action.payload
      }
    }

    default:
      return state
  }
}

const initialState: ViewsState = {
  views: [
    // {
    //   createdBy: 1,
    //   createdTime: 1,
    //   entityType: 'idunno',
    //   updatedTime: 1,
    //   id: 1,
    //   orgId: 1,
    //   version: 1,
    //   viewProperties: {
    //     name: 'overview',
    //     label: 'Overview',
    //     active: false,
    //     query: '*', // let's pretend * = everything
    //     url: 'overview'
    //   },
    //   visibility: 'PUBLIC' // or 'PRIVATE'
    // },
    {
      createdBy: 0,
      createdTime: Date.now(),
      entityType: 'idunno',
      updatedTime: Date.now(),
      id: Math.floor(Math.random() * 100),
      orgId: 0,
      version: 0,
      viewProperties: {
        name: 'New View',
        label: '',
        active: true,
        query: '',
        url: ''
      },
      visibility: 'PUBLIC' // or 'PRIVATE'
    }
  ],
  activeView: {
    createdBy: 0,
    createdTime: Date.now(),
    entityType: 'idunno',
    updatedTime: Date.now(),
    id: Math.floor(Math.random() * 100),
    orgId: 0,
    version: 0,
    viewProperties: {
      name: '',
      label: '',
      active: true,
      query: '',
      url: ''
    },
    visibility: 'PUBLIC' // or 'PRIVATE'
  }
}

type IViewsContext = ViewsState | undefined
type IViewsDispatchContext = Dispatch<ViewsAction> | undefined

const ViewsContext = createContext<IViewsContext>(undefined)
const ViewsDispatchContext = createContext<IViewsDispatchContext>(undefined)

const ViewsProvider: React.FC = ({ children }) => {
  const [state, dispatch] = useReducer(ViewsReducer, initialState)
  return (
    <ViewsContext.Provider value={state}>
      <ViewsDispatchContext.Provider value={dispatch}>
        {children}
      </ViewsDispatchContext.Provider>
    </ViewsContext.Provider>
  )
}

const useViews = () => {
  const state = useContext(ViewsContext)
  const dispatch = useContext(ViewsDispatchContext)

  if (state === undefined || dispatch === undefined) {
    throw new Error('views must be used within ViewsProvider')
  }

  return { state, dispatch }
}

export { ViewsProvider, useViews, ViewsContext, ViewsDispatchContext }
