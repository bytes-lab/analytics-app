import React, {
  useState,
  forwardRef,
  Ref,
  ReactElement,
  useImperativeHandle,
  useEffect
} from 'react'
import { useTranslation } from 'react-i18next'
import { useCombobox } from 'downshift'
import Popover from '@reach/popover'
import clsx from 'clsx'

import { DrowdownProps } from './api'
import { usePrevious } from 'opsramp-design-system/lib/utils'
import './style.css'

function DropDownImpl<T>(
  {
    disabled,
    items,
    initialValue,
    defaultValue,
    hideSearch,
    toggleButtonLabel,
    noFilterResultLabel,
    containerClasses,
    toggleButtonClasses,
    popoverClasses,
    inputClasses,
    menuClasses,
    itemToString = item => (item ? String(item) : ''),
    placeholder = '',
    onChange,
    filterHandler
  }: DrowdownProps<T>,
  refProps: Ref<{ reset: () => void }>
) {
  const { t } = useTranslation()
  const [showItems, setShowItems] = useState<T[]>(items)
  const previousItems = usePrevious(items)
  const ref = React.useRef<HTMLButtonElement | null>(null)

  useEffect(() => {
    if (previousItems?.length && items.length) {
      setShowItems(items)
    }
  }, [items, previousItems])

  const {
    isOpen,
    highlightedIndex,
    selectedItem,
    getComboboxProps,
    getInputProps,
    getItemProps,
    getMenuProps,
    getToggleButtonProps,
    setInputValue,
    reset
  } = useCombobox<T>({
    items: showItems,
    initialSelectedItem: initialValue,
    defaultSelectedItem: defaultValue,
    itemToString,
    // trigger onChange whenever the selected item change
    onSelectedItemChange: changes => onChange?.(changes.selectedItem),

    // When re-opening the dropdown, empty the search input and scroll into view
    // to the previous selected item.
    onIsOpenChange: changes => {
      setInputValue('')
    },

    // Filter items base on search input's value
    onInputValueChange: ({ inputValue }) => {
      setShowItems(filterHandler(items, inputValue))
    },

    // Override default behavior when user press escape key from reset value =>
    // not change value
    stateReducer: (state, actionChanges) => {
      const { type, changes } = actionChanges
      switch (type) {
        case useCombobox.stateChangeTypes.InputKeyDownEscape: {
          // Press escapse, move focus to the toggle button
          ref?.current?.focus()
          return { ...changes, selectedItem: state.selectedItem }
        }
        case useCombobox.stateChangeTypes.InputKeyDownEnter: {
          // Press enter, move focus to the toggle button
          ref?.current?.focus()
          return changes
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
        onChange?.(defaultValue)
        reset()
      }
    }
  })

  function toggleButton() {
    return (
      <button
        {...getToggleButtonProps({
          ref: ref,
          tabIndex: 0,
          className: clsx(toggleButtonClasses, {
            'ops-toggle-button--open': isOpen
          }),
          disabled
        })}
      >
        {toggleButtonLabel ?? itemToString(selectedItem)}
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
            'mt-1 py-3 border shadow-md ops-background': isOpen
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
                'pt-1 pr-2 pb-1 pl-6 rounded-full mx-4',
                { 'position-relative': isOpen },
                { 'visually-hidden': !isOpen },
                { border: !hideSearch }
              )}
              style={{ minWidth: 200 }}
              {...getComboboxProps({}, { suppressRefError: true })}
            >
              <i
                className={clsx(
                  'icon-search',
                  { 'position-absolute': isOpen },
                  { hidden: hideSearch }
                )}
                style={{ left: 4 }}
              />
              <input
                placeholder={placeholder}
                tabIndex={isOpen ? undefined : -1}
                className={clsx('flex-1 outline-none', inputClasses, {
                  'h-0': hideSearch
                })}
                {...getInputProps({}, { suppressRefError: true })}
              />
            </div>
            <ul
              className={clsx(
                'ops-list flex-1 overflow-y-auto',
                {
                  'p-0': showItems.length === 0 && !noFilterResultLabel
                },
                menuClasses
              )}
              {...getMenuProps({}, { suppressRefError: true })}
            >
              {isOpen &&
                showItems.map((item, index) => (
                  <li
                    key={`${itemToString(item)}${index}`}
                    className={clsx(
                      'ops-list-item whitespace-no-wrap',
                      { 'is-active': highlightedIndex === index },
                      {
                        'ops-list-item--selected font-weight-bold':
                          itemToString(selectedItem) === itemToString(item)
                      }
                    )}
                    {...getItemProps({ item, index })}
                  >
                    <span className="ops-list-item__text">
                      {itemToString(item)}
                    </span>
                    {itemToString(defaultValue) === itemToString(item) && (
                      <span className="ml-1">(Default)</span>
                    )}
                  </li>
                ))}

              {isOpen && showItems.length === 0 && (
                <li className="ops-list-item ops-list-item--disabled whitespace-no-wrap">
                  <span className="ops-list-item__text">
                    {noFilterResultLabel ? noFilterResultLabel : t('no_result')}
                  </span>
                </li>
              )}
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
  props: DrowdownProps<T> & React.RefAttributes<R>
) => ReactElement | null

const DropDown = forwardRef(DropDownImpl) as ForwardRefFn<{
  reset: () => void
}>

export default DropDown
