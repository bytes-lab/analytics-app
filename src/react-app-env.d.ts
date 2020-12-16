/// <reference types="react-scripts" />
declare namespace NodeJS {
  interface ProcessEnv {
    NODE_ENV: 'development' | 'production' | 'test'
    PUBLIC_URL?: string
    REACT_APP_HASH?: string
    REACT_APP_INFRASTRUCTUREUI_API_URI: string
    REACT_APP_JWT_TOKEN: string
    REACT_APP_WS_INFRASTRUCTUREUI_URI?: string
  }
}

declare function renderInfrastructureUI(
  containerId: string,
  history: import('history').History,
  userNavInfo?: UserNavInfo
): void
declare function unmountInfrastructureUI(containerId: string): void
