import React, {
  SetStateAction,
  Dispatch,
  createContext,
  useState,
  useContext,
  ReactElement
} from 'react'
import { Dialog } from 'opsramp-design-system'
import { wrapEvent } from '@reach/utils'

type IModalContext = {
  isOpen: boolean
  setIsOpen?: Dispatch<SetStateAction<boolean>>
}

const ModalContext = createContext<IModalContext | undefined>(undefined)

export type ModalProps = {
  isOpen?: boolean
}

const Modal: React.FC<ModalProps> = ({
  children,
  isOpen: controlledIsOpen
}) => {
  const [isOpen, setIsOpen] = useState(false)
  let value

  if (controlledIsOpen !== undefined) {
    value = { isOpen: controlledIsOpen }
  } else {
    value = { isOpen, setIsOpen }
  }

  return <ModalContext.Provider value={value} children={children} />
}

const ModalDismissButton: React.FC<{ children: ReactElement }> = ({
  children: child
}) => {
  const { setIsOpen } = useContext(ModalContext) as IModalContext
  return React.cloneElement(child, {
    onClick: wrapEvent(child.props.onClick, () => setIsOpen?.(false))
  })
}

const ModalOpenButton: React.FC<{ children: ReactElement }> = ({
  children: child
}) => {
  const { setIsOpen } = useContext(ModalContext) as IModalContext
  return React.cloneElement(child, {
    onClick: wrapEvent(child.props.onClick, () => setIsOpen?.(true))
  })
}

const ModalContents: React.FC<React.HTMLAttributes<HTMLDivElement>> = props => {
  const { isOpen } = useContext(ModalContext) as IModalContext

  return <Dialog isOpen={isOpen} {...props} />
}

export { Modal, ModalDismissButton, ModalOpenButton, ModalContents }
