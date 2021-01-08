import 'stop-runaway-react-effects/hijack'
import React from 'react'
import ReactDOM from 'react-dom'
import 'opsramp-design-system/lib/opsramp-design-system.css'
import 'opsramp-design-system/lib/tailwind.css'
import './index.scss'
import * as serviceWorker from './serviceWorker'
import { History, createBrowserHistory } from 'history'
import { Router } from 'react-router-dom'
import { AnalyticsAppsUI } from 'container'
import AppProvider from 'context'
import { UserNavInfo } from 'context/nav-context'
import './i18n'

window.renderAnalyticsAppsUI = (
  containerId: string,
  history: History = createBrowserHistory({
    basename: '/analytics-apps'
  }),
  userNavInfo: UserNavInfo
) => {
  ReactDOM.render(
    <Router history={history}>
      <AppProvider>
        <AnalyticsAppsUI userNavInfo={userNavInfo} />
      </AppProvider>
    </Router>,
    document.getElementById(containerId)
  )
}

window.unmountAnalyticsAppsUI = (containerId: string) => {
  if (document.getElementById(containerId)) {
    ReactDOM.unmountComponentAtNode(
      document.getElementById(containerId) as Element
    )
  }
}

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister()
