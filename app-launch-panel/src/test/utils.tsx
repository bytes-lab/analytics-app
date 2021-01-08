import React, { useReducer } from 'react'
import { render as rtlRender } from '@testing-library/react'
import { createMemoryHistory, History } from 'history'
import { Router, Route } from 'react-router-dom'
import { I18nextProvider } from 'react-i18next'
import i18n from 'i18n'
import {
  UserNavInfoStateContext,
  UserNavInfoDispatchContext,
  userNavInfoReducer
} from 'context/nav-context'

const render = (
  ui: React.ReactElement,
  {
    route = '/',
    path = '/',
    history = createMemoryHistory({ initialEntries: [route] })
  }: {
    route?: string
    path?: string
    history?: History
  } = {}
) => {
  const Wrapper: React.FC = ({ children }) => {
    const userNavInfo: any = {
      mspId: 1,
      mspUuid: 'msp_1',
      clientId: 1,
      clientUuid: 'client_1',
      orgId: 1,
      orgUuid: 'org_1',
      user: {}
    }

    const [userNavInfoState, userNavDispatch] = useReducer(
      userNavInfoReducer,
      userNavInfo
    )

    return (
      <UserNavInfoStateContext.Provider value={userNavInfoState}>
        <UserNavInfoDispatchContext.Provider value={userNavDispatch}>
          <Router history={history}>
            <I18nextProvider i18n={i18n}>
              <Route path={path}>{children}</Route>
            </I18nextProvider>
          </Router>
        </UserNavInfoDispatchContext.Provider>
      </UserNavInfoStateContext.Provider>
    )
  }

  return { ...rtlRender(ui, { wrapper: Wrapper }), history }
}

export * from '@testing-library/react'
export { render }
