import React from 'react'
import clsx from 'clsx'
import './styles.css'

type Props = {
  required?: boolean
} & React.LabelHTMLAttributes<HTMLLabelElement>

function Label({
  children,
  className,
  required,
  ...rest
}: React.PropsWithChildren<Props>) {
  return (
    <label
      className={clsx(
        'dnm-label',
        { 'dnm-label--required': required },
        className
      )}
      {...rest}
    >
      {children}
    </label>
  )
}

export default Label
