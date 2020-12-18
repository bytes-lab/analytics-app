/// <reference types="react-scripts" />
declare namespace NodeJS {
  interface ProcessEnv {
    NODE_ENV: 'development' | 'production' | 'test'
    PUBLIC_URL?: string
    REACT_APP_HASH?: string
    REACT_APP_ANALYTICSAPPSUI_API_URI: string
    REACT_APP_JWT_TOKEN: string
    REACT_APP_WS_ANALYTICSAPPSUI_URI?: string
  }
}

declare function renderAnalyticsAppsUI(
  containerId: string,
  history: import('history').History,
  userNavInfo?: UserNavInfo
): void
declare function unmountAnalyticsAppsUI(containerId: string): void
