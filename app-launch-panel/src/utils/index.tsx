import {
  useReducer,
  SetStateAction,
  useCallback,
  useEffect,
  useRef,
  useState
} from 'react'

type Callback<T> = (value?: T) => void
type DispatchWithCallback<T> = (value: T, callback?: Callback<T>) => void

function useStateCallback<T>(
  initialState: T | (() => T)
): [T, DispatchWithCallback<SetStateAction<T>>] {
  const [state, _setState] = useState(initialState)

  const callbackRef = useRef<Callback<T>>()
  const isFirstCallbackCall = useRef<boolean>(true)

  const setState = useCallback(
    (setStateAction: SetStateAction<T>, callback?: Callback<T>): void => {
      callbackRef.current = callback
      _setState(setStateAction)
    },
    []
  )

  useEffect(() => {
    if (isFirstCallbackCall.current) {
      isFirstCallbackCall.current = false
      return
    }
    callbackRef.current?.(state)
  }, [state])

  return [state, setState]
}

const reducer = <T extends object>(
  previousState: T = {} as T,
  updatedState: Partial<T> = {}
): T => {
  return { ...previousState, ...updatedState }
}

const useSetState = <T extends object>(
  initialState: T = {} as T
): [T, (updatedState: Partial<T>) => void] => {
  const [state, dispatch] = useReducer<React.Reducer<T, Partial<T>>>(
    reducer,
    initialState
  )

  const setState = useCallback((updatedState: Partial<T>) => {
    dispatch(updatedState)
  }, [])
  return [state, setState]
}

// Convert upload file to a base64 string
function getBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve((reader.result as string).split('base64,')[1])
    reader.onerror = error => reject(error)
  })
}

export { useStateCallback, useSetState, getBase64 }
