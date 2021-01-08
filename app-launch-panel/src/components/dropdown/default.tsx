import React from 'react'
import clsx from 'clsx'
import matchSorter from 'match-sorter'
import Dropdown from './index'
import { DefaultDropdownProps } from './default.api'
import './default.style.css'

function DefaultDropdownImpl(
  {
    disabled,
    data,
    defaultToggleLabel,
    initialValue,
    placeholder,
    hideSearch,
    onChange
  }: DefaultDropdownProps,
  ref?: React.Ref<{ reset: () => void }>
) {
  const [selectedItem, setSelectedItem] = React.useState<
    string | undefined | null
  >(initialValue)

  function getToggleBtnLabel() {
    return (
      <>
        <span
          className={clsx('truncate', {
            'default-dropdown--placeholder': !selectedItem
          })}
        >{`${selectedItem ?? defaultToggleLabel}`}</span>
        <i className="ml-auto icon-chevron-down" />
      </>
    )
  }

  function filterHandler(source: string[], searchQuery?: string) {
    return searchQuery ? matchSorter(source, searchQuery) : source
  }

  function handleChange(value?: string | null) {
    setSelectedItem(value)
    onChange(value)
  }

  return (
    <Dropdown
      ref={ref}
      items={data}
      disabled={disabled}
      initialValue={initialValue}
      placeholder={placeholder}
      hideSearch={hideSearch}
      toggleButtonLabel={getToggleBtnLabel()}
      toggleButtonClasses={clsx(
        'default-dropdown leading-snug overflow-x-hidden text-left flex justify-between body-1'
      )}
      filterHandler={filterHandler}
      onChange={handleChange}
    />
  )
}

type ForwardRefFn<R> = (
  props: DefaultDropdownProps & React.RefAttributes<R>
) => React.ReactElement | null

const DefaultDropdown = React.forwardRef(DefaultDropdownImpl) as ForwardRefFn<{
  reset?: () => void
}>

export default DefaultDropdown
