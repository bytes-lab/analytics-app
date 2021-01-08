import React from 'react'

export type Option = {
  value: string
  label: string
}

type SelectProps = Omit<
  React.InputHTMLAttributes<HTMLSelectElement>,
  'onChange'
> & {
  placeholder?: string
  value?: string
  options: Option[]
  onChange: (value: string, event: React.ChangeEvent<HTMLSelectElement>) => void
}

function Select({
  value,
  placeholder,
  options,
  onChange,
  name,
  ...rest
}: SelectProps) {
  function handleChange(event: React.ChangeEvent<HTMLSelectElement>) {
    onChange?.(event.currentTarget.value, event)
  }

  return (
    <select
      name={name}
      value={value}
      onChange={handleChange}
      className="block px-3 py-2 border mx-3"
      {...rest}
    >
      {placeholder && <option value="">{placeholder}</option>}
      {options.map((o: Option) => (
        <option value={o.value} key={o.value}>
          {o.label}
        </option>
      ))}
    </select>
  )
}

export { Select }
