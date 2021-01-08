import React, { useState, useImperativeHandle } from 'react'
import { useCombobox, useMultipleSelection } from 'downshift'
import { Checkbox } from 'opsramp-design-system'
import { useTranslation } from 'react-i18next'
import Popover from '@reach/popover'
import clsx from 'clsx'
import { MultiSelectProps } from './api'
import 'components/dropdown/style.css'

function MultiSelectImpl<T>(
  {
    disabled,
    items,
    initialValues = [],
    defaultValues,
    toggleButtonLabel,
    noFilterResultLabel,
    containerClasses,
    toggleButtonClasses,
    popoverClasses,
    inputClasses,
    menuClasses,
    itemToString = item => (item ? String(item) : ''),
    placeholder,
    onChange,
    filterHandler,
    selectAll
  }: MultiSelectProps<T>,
  refProps: React.Ref<{ reset?: () => void }>
) {
  const [inputValue, setInputValue] = useState<string | undefined>()
  const ref = React.useRef<HTMLButtonElement | null>(null)
  const { t } = useTranslation()

  function getFilteredItems(items: T[]) {
    return filterHandler(items, inputValue)
  }

  const {
    getDropdownProps,
    addSelectedItem,
    removeSelectedItem,
    selectedItems,
    reset,
    setSelectedItems
  } = useMultipleSelection<T>({
    initialSelectedItems: initialValues,
    onSelectedItemsChange: changes => onChange?.(changes?.selectedItems)
  })

  const {
    isOpen,
    getToggleButtonProps,
    getMenuProps,
    getInputProps,
    getComboboxProps,
    highlightedIndex,
    getItemProps,
    selectItem
  } = useCombobox<T>({
    items: getFilteredItems(items),
    onStateChange: ({ inputValue, type, selectedItem }) => {
      switch (type) {
        case useCombobox.stateChangeTypes.InputChange:
          setInputValue(inputValue)
          break
        case useCombobox.stateChangeTypes.InputKeyDownEnter:
        case useCombobox.stateChangeTypes.ItemClick:
        case useCombobox.stateChangeTypes.InputBlur:
          if (selectedItem) {
            setInputValue('')
            selectedItems.includes(selectedItem)
              ? removeSelectedItem(selectedItem)
              : addSelectedItem(selectedItem)
            // @ts-ignore
            selectItem(null)
          }
          break
        default:
          break
      }
    },
    stateReducer: (state, actionChanges) => {
      const { type, changes } = actionChanges

      switch (type) {
        case useCombobox.stateChangeTypes.InputKeyDownEnter:
        case useCombobox.stateChangeTypes.ItemClick: {
          return {
            ...changes,
            // Keep the menu open when user selects an item
            isOpen: true,
            highlightedIndex: state.highlightedIndex,
            inputValue: ''
          }
        }
        default: {
          return actionChanges.changes
        }
      }
    }
  })

  // useImperativeHandle let us call child callback from the prarent component
  // In our usecase, the parent component can reset all of dropdown children
  useImperativeHandle(refProps, () => {
    return {
      reset: () => {
        onChange?.(defaultValues)
        reset()
      }
    }
  })

  function isSelectedAllItems() {
    return selectedItems.length === items.length
  }

  function toggleButton() {
    return (
      <button
        {...getToggleButtonProps({
          ref: ref
        })}
        tabIndex={0}
        className={clsx(toggleButtonClasses, {
          'ops-toggle-button--open': isOpen
        })}
        disabled={disabled}
      >
        {toggleButtonLabel
          ? toggleButtonLabel
          : selectedItems.map(item => itemToString(item)).join(', ')}
        {isOpen ? (
          <i className="ml-auto icon-chevron-up" />
        ) : (
          <i className="ml-auto icon-chevron-down" />
        )}
      </button>
    )
  }

  function menu() {
    // In side the popover, the wrapper should have zIndex and position
    // relative/absolute so that the inner connet can will have auto focus
    // behavior when opening the popover
    return (
      <div
        className={clsx(
          'position-relative flex flex-column rounded-lg ',
          {
            'mt-1 border shadow-md ops-background': isOpen
          },
          popoverClasses
        )}
        style={{
          maxHeight: '24rem',
          zIndex: 1,
          overflowX: 'auto'
        }}
      >
        {items.length > 0 ? (
          <>
            <div
              className={clsx(
                'body-2 flex align-items-center',
                'pr-2 py-2 pl-8 border-b',
                { 'position-relative': isOpen },
                { 'visually-hidden': !isOpen }
              )}
              style={{ minWidth: 200, backgroundColor: '#fafafa' }}
              {...getComboboxProps({}, { suppressRefError: true })}
            >
              <i
                className={clsx('icon-search', { 'position-absolute': isOpen })}
                style={{ left: 4 }}
              />
              <input
                placeholder={placeholder}
                tabIndex={isOpen ? undefined : -1}
                style={{ backgroundColor: '#fafafa' }}
                className={clsx('flex-1 outline-none', inputClasses)}
                {...getInputProps(
                  getDropdownProps(
                    { preventKeyAction: true },
                    { suppressRefError: true }
                  ),
                  { suppressRefError: true }
                )}
              />
            </div>
            <ul
              className={clsx(
                'ops-list flex-1 overflow-y-auto',
                {
                  'p-0':
                    getFilteredItems(items).length === 0 && !noFilterResultLabel
                },
                menuClasses
              )}
              {...getMenuProps({}, { suppressRefError: true })}
            >
              {isOpen ? (
                <>
                  {selectAll ? (
                    <li
                      className={clsx('ops-list-item whitespace-no-wrap', {
                        'ops-list-item--selected font-weight-bold': isSelectedAllItems()
                      })}
                      onClick={() => {
                        isSelectedAllItems()
                          ? setSelectedItems([])
                          : setSelectedItems(items)
                      }}
                    >
                      <Checkbox checked={isSelectedAllItems()} />
                      {isSelectedAllItems()
                        ? t('deselect_all')
                        : t('select_all')}
                    </li>
                  ) : null}
                  {getFilteredItems(items).map((item, index) => (
                    <li
                      key={`${itemToString(item)}${index}`}
                      className={clsx(
                        'ops-list-item whitespace-no-wrap',
                        { 'is-active': highlightedIndex === index },
                        {
                          'ops-list-item--selected font-weight-bold': selectedItems.includes(
                            item
                          )
                        }
                      )}
                      {...getItemProps({ item, index })}
                    >
                      <Checkbox checked={selectedItems.includes(item)} />

                      <span className="ops-list-item__text">
                        {itemToString(item)}
                      </span>
                      {defaultValues?.includes(item) ? (
                        <span className="ml-1">({t('default')})</span>
                      ) : null}
                    </li>
                  ))}
                </>
              ) : null}

              {isOpen && getFilteredItems(items).length === 0 ? (
                <li className="ops-list-item ops-list-item--disabled whitespace-no-wrap">
                  <span className="ops-list-item__text">
                    {noFilterResultLabel ? noFilterResultLabel : t('no_result')}
                  </span>
                </li>
              ) : null}
            </ul>
          </>
        ) : (
          <div className={clsx('mx-4', { 'visually-hidden': !isOpen })}>
            {t('loading')}
          </div>
        )}
      </div>
    )
  }

  return (
    <div className={clsx(containerClasses)}>
      {toggleButton()}
      <Popover targetRef={ref}>{menu()}</Popover>
    </div>
  )
}

type ForwardRefFn<R> = <T>(
  props: MultiSelectProps<T> & React.RefAttributes<R>
) => React.ReactElement | null

const MultiSelect = React.forwardRef(MultiSelectImpl) as ForwardRefFn<{
  reset?: () => void
}>

export default MultiSelect
