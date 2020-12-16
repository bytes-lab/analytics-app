import React, { useEffect } from 'react'
import { Route, Router, useHistory } from 'react-router'
import ResourcesScreen from 'screens/resources'
import OverviewScreen from 'screens/overview'
import TopologyScreen from 'screens/topology'
import AppProvider from 'context'
import { UserNavInfo, useUserNavInfo } from 'context/nav-context'

type AppProps = {
  userNavInfo: UserNavInfo
}

const InfrastructureUI: React.FC<AppProps> = ({ userNavInfo }) => {
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
      <Route
        exact
        path="/resource"
        component={() => <ResourcesScreen userNavInfo={userNavInfo} />}
      />
      <Route
        path="/topology"
        component={() => <TopologyScreen />}
      />
    </Router>
  )
}

export { InfrastructureUI }
