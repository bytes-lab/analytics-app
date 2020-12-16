import React from 'react'
import clsx from 'clsx'
import matchSorter from 'match-sorter'
import { useTranslation } from 'react-i18next'
import MultiSelect from './index'
import { DefaultMultiSelectProps } from './default.api'
import 'components/dropdown/default.style.css'

function DefaultMultiSelectImpl(
  { data, defaultToggleLabel, onChange, ...rest }: DefaultMultiSelectProps,
  ref?: React.Ref<{ reset: () => void }>
) {
  const [selectedItems, setSelectedItems] = React.useState<
    string[] | undefined | null
  >(rest.initialValues)
  const { t } = useTranslation()

  function getToggleBtnLabel() {
    return (
      <>
        <span
          className={clsx('truncate', {
            'default-dropdown--placeholder': !selectedItems?.length
          })}
        >{`${
          selectedItems?.length
            ? selectedItems.length <= 2
              ? selectedItems.slice(0).join(', ')
              : `${selectedItems.length} ${t('selected')}`
            : defaultToggleLabel
        }`}</span>
      </>
    )
  }

  function filterHandler(source: string[], searchQuery?: string) {
    return searchQuery ? matchSorter(source, searchQuery) : source
  }

  function handleChange(selectedItems?: string[] | null) {
    setSelectedItems(selectedItems)
    onChange?.(selectedItems)
  }

  return (
    <MultiSelect
      ref={ref}
      items={data}
      toggleButtonLabel={getToggleBtnLabel()}
      toggleButtonClasses={clsx(
        'default-dropdown leading-snug overflow-x-hidden text-left flex justify-between'
      )}
      filterHandler={filterHandler}
      onChange={handleChange}
      {...rest}
    />
  )
}

type ForwardRefFn<R> = (
  props: DefaultMultiSelectProps & React.RefAttributes<R>
) => React.ReactElement | null

const DefaultMultiSelect = React.forwardRef(
  DefaultMultiSelectImpl
) as ForwardRefFn<{
  reset?: () => void
}>

export default DefaultMultiSelect
