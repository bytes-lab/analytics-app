import React, { createContext, Dispatch, useReducer, useContext } from 'react'

type OnboardState = {
  onboardStatus?: string
}

type OnboardStateAction =
  | {
      type: 'FETCH_STATUS'
      payload: {
        onboardStatus?: string
      }
    }
  | {
      type: 'CLEAR_STATUS'
    }
  | {
      type: 'UPDATE_STATUS'
      payload: {
        onboardStatus?: string
      }
    }

export const OnboardStatusReducer: React.Reducer<
  OnboardState,
  OnboardStateAction
> = (state, action) => {
  switch (action.type) {
    case 'FETCH_STATUS':
      return { onboardStatus: action.payload.onboardStatus }

    case 'CLEAR_STATUS': {
      return { ...state, onboardStatus: undefined }
    }

    case 'UPDATE_STATUS': {
      return { ...state, onboardStatus: action.payload.onboardStatus }
    }

    default:
      return state
  }
}

const initialState: OnboardState = {
  onboardStatus: undefined
}

type IOnboardStatusContext = OnboardState | undefined
type IOnboardStatusDispatchContext = Dispatch<OnboardStateAction> | undefined

const OnboardStatusContext = createContext<IOnboardStatusContext>(undefined)
const OnboardStatusDispatchContext = createContext<
  IOnboardStatusDispatchContext
>(undefined)

const OnboardStatusProvider: React.FC = ({ children }) => {
  const [state, dispatch] = useReducer(OnboardStatusReducer, initialState)
  return (
    <OnboardStatusContext.Provider value={state}>
      <OnboardStatusDispatchContext.Provider value={dispatch}>
        {children}
      </OnboardStatusDispatchContext.Provider>
    </OnboardStatusContext.Provider>
  )
}

const useOnboardStatus = () => {
  const state = useContext(OnboardStatusContext)
  const dispatch = useContext(OnboardStatusDispatchContext)

  if (state === undefined || dispatch === undefined) {
    throw new Error(
      'useOnboardStatus must be used within OnboardStatusProvider'
    )
  }

  return { ...state, dispatch }
}

export {
  OnboardStatusProvider,
  useOnboardStatus,
  OnboardStatusContext,
  OnboardStatusDispatchContext
}
