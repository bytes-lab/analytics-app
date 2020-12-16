import React, {
  Reducer,
  Dispatch,
  createContext,
  useContext,
  useReducer
} from 'react'

export type UserNavInfo = {
  mspId: number
  mspUuid: string
  clientId: number
  clientUuid: string
  orgId: number
  orgUuid: string
  user: User
}

type User = {
  loginName: string
  orgId: number
  userType?: string
  organizationName?: string
  lastName: string
  firstName: string
  email: string
  country: string
  profileImage: ProfileImage
  timeZone: Timezone
}

type Timezone = {
  name?: string
  label?: string
  code?: string
}

type ProfileImage = {
  logoPath: string
  thumbPath: string
  TinyThumbPath: string
}

type UserNavInfoAction = {
  type: 'SET_NAV_INFO'
  payload: UserNavInfo
}

const initialUserState = {
  loginName: 'opsramp.user',
  lastName: 'Profile',
  firstName: 'Opsramp',
  email: 'user@opsramp.com',
  country: 'United States',
  profileImage: {
    logoPath: 'https://everest.app.opsramp.net/img/nophoto.gif',
    thumbPath: 'https://everest.app.opsramp.net/img/nophoto.gif',
    TinyThumbPath: 'https://everest.app.opsramp.net/img/wall_img1.gif'
  },
  timeZone: {
    code: '',
    name: '',
    label: ''
  }
}

const initialUserNavInfoState = {
  mspId: 0,
  mspUuid: 'msp_0',
  clientId: 0,
  clientUuid: 'client_0',
  orgId: 0,
  orgUuid: 'org_0',
  user: initialUserState as User
}

const userNavInfoReducer: Reducer<UserNavInfo, UserNavInfoAction> = (
  state,
  action
) => {
  switch (action.type) {
    case 'SET_NAV_INFO':
      return { ...state, ...action.payload }

    default:
      return state
  }
}

type IUserNavInfoStateContext = UserNavInfo | undefined
type IUserNavInfoDispatchContext = Dispatch<UserNavInfoAction> | undefined

const UserNavInfoStateContext = createContext<IUserNavInfoStateContext>(
  undefined
)
const UserNavInfoDispatchContext = createContext<IUserNavInfoDispatchContext>(
  undefined
)

const useUserNavInfo = () => {
  const state = useContext(UserNavInfoStateContext)
  const dispatch = useContext(UserNavInfoDispatchContext)

  if (state === undefined || dispatch === undefined) {
    throw new Error('useUserNavInfo must be used within UserNavInfoProvider')
  }

  return { ...state, dispatch }
}

const UserNavInfoProvider: React.FC = ({ children }) => {
  const [state, dispatch] = useReducer(
    userNavInfoReducer,
    initialUserNavInfoState
  )

  return (
    <UserNavInfoStateContext.Provider value={state}>
      <UserNavInfoDispatchContext.Provider value={dispatch}>
        {children}
      </UserNavInfoDispatchContext.Provider>
    </UserNavInfoStateContext.Provider>
  )
}

export {
  initialUserNavInfoState,
  UserNavInfoStateContext,
  UserNavInfoDispatchContext,
  userNavInfoReducer,
  useUserNavInfo,
  UserNavInfoProvider
}
