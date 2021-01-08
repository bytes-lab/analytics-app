import React from 'react'
import clsx from 'clsx'

type Props = {
  show?: boolean
} & React.HTMLAttributes<HTMLDivElement>

function ErrorMessage({
  show = true,
  children,
  className,
  ...rest
}: React.PropsWithChildren<Props>) {
  return (
    <>
      {show ? (
        <div className={clsx('body-3 ops-text-red', className)} {...rest}>
          {children}
        </div>
      ) : null}
    </>
  )
}

export default ErrorMessage
