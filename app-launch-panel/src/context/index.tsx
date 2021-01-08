import React from 'react'

import { ReactQueryConfigProvider, ReactQueryConfig } from 'react-query'
import { UserNavInfoProvider } from './nav-context'

const queryConfig: ReactQueryConfig = {
  queries: {
    retry: 0,
    staleTime: 60000
  }
}

const AppProvider: React.FC = ({ children }) => {
  return (
    <ReactQueryConfigProvider config={queryConfig}>
      <UserNavInfoProvider>{children}</UserNavInfoProvider>
    </ReactQueryConfigProvider>
  )
}

export default AppProvider
