import React, { useEffect } from 'react'
import { Route, Router, useHistory } from 'react-router'
import OverviewScreen from 'screens/overview'
// import AppProvider from 'context'
import { UserNavInfo, useUserNavInfo } from 'context/nav-context'

type AppProps = {
  userNavInfo: UserNavInfo
}

const AnalyticsAppsUI: React.FC<AppProps> = ({ userNavInfo }) => {
  const { dispatch } = useUserNavInfo()
  const history = useHistory()

  useEffect(() => {
    if (userNavInfo && userNavInfo.clientId !== 0) {
      dispatch({
        type: 'SET_NAV_INFO',
        payload: userNavInfo
      })
    }
  }, [dispatch, userNavInfo])

  return (
    <Router history={history}>
      <Route
        path="/"
        component={() => <OverviewScreen userNavInfo={userNavInfo} />}
      />
    </Router>
  )
}

export { AnalyticsAppsUI }
