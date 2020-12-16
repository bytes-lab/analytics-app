import React, {
  forwardRef,
  useState,
  useEffect,
  useRef,
  Ref,
  useImperativeHandle,
  ReactElement
} from 'react'
import { useCombobox } from 'downshift'
import matchSorter from 'match-sorter'
import { usePrevious } from 'opsramp-design-system/lib/utils'
import { useTranslation } from 'react-i18next'
import isString from 'lodash/isString'
import isEqual from 'lodash/isEqual'
import remove from 'lodash/remove'
import min from 'lodash/min'
import './index.scss'
import { indexOf } from 'lodash'

export type QueryBuilderProps = Omit<
  React.HTMLAttributes<HTMLInputElement>,
  'onChange'
> & {
  onChange?: (value: string) => void
  onSelectEnd?: (selectionEnd: string) => void
  onSelectObject?: (selectObject: CompletionItem) => void
  items: any[]
  defaultValue?: string
  onFocus?: (event?: React.MouseEvent) => void
  onBlur?: (event?: React.MouseEvent) => void
  placeholder?: string
  error?: string
  dropDownMetricLabel?: boolean
  dropDownLabel?: React.ReactNode
  onKeyPress?: (event?: React.KeyboardEvent) => void
}
type CompletionItem = {
  label: string
  key: string
  value: string
}

function QueryBuilderInputTmp(
  {
    onChange,
    onSelectEnd,
    onSelectObject,
    items,
    defaultValue,
    onFocus,
    onBlur,
    placeholder,
    dropDownLabel,
    onKeyDown
  }: QueryBuilderProps,
  ref: Ref<{ reset: () => void }>
) {
  const [inputItems, setInputItems] = useState(items)
  const inputRef = useRef<HTMLInputElement | null>(null)
  const inputContainerRef = useRef<HTMLDivElement | null>(null)
  const listClassName = 'px-5 py-2 body-2 ops-text-global-grey-700 truncate'
  const [splitIndex, setSplitIndex] = useState(0)
  const { t } = useTranslation()
  const previousItems = usePrevious(items)
  const specialCharsArray = ['$']

  const dropDownList = (item: any, index: number) => {
    return (
      <li
        className={listClassName}
        style={
          highlightedIndex === index
            ? { backgroundColor: 'rgba(0, 119, 200,0.05)' }
            : {}
        }
        key={`${item}${index}`}
        {...getItemProps({ item, index })}
      >
        <span className="opacity-100"> {item}</span>
      </li>
    )
  }
  const showObjectList = (itemList: CompletionItem[]) => {
    return (
      <>
        {itemList.map((item, index) => {
          if (!isString(item)) {
            return (
              <li
                className={listClassName}
                style={
                  highlightedIndex === index
                    ? { backgroundColor: 'rgba(0, 119, 200,0.05)' }
                    : {}
                }
                key={`${item}${index}`}
                {...getItemProps({ item, index })}
              >
                <span className="opacity-100">
                  {' '}
                  {item.label} ({item.key})
                </span>
              </li>
            )
          }
          // eslint-disable-next-line array-callback-return
          return
        })}
      </>
    )
  }

  const showMetricList = (itemList: string[]) => {
    let MetricLabel = false
    itemList.forEach(item => {
      if (isString(item) && item.indexOf('=') === -1) {
        MetricLabel = true
      }
    })

    return (
      <>
        {MetricLabel && dropDownLabel}
        {itemList.map((item, index) => {
          if (isString(item) && item.indexOf('=') === -1) {
            return dropDownList(item, index)
          }
          // eslint-disable-next-line array-callback-return
          return
        })}
      </>
    )
  }

  const showVariableList = (itemList: string[]) => {
    return (
      <>
        {itemList.map((item, index) => {
          if (isString(item) && item.indexOf('=') !== -1) {
            return dropDownList(item, index)
          }
          // eslint-disable-next-line array-callback-return
          return
        })}
      </>
    )
  }

  const {
    isOpen,
    getMenuProps,
    getInputProps,
    getComboboxProps,
    highlightedIndex,
    getItemProps,
    reset
  } = useCombobox({
    items: inputItems,

    defaultInputValue: defaultValue,

    onInputValueChange: ({ inputValue }) => {
      let lastInput = ''
      const stringArray: string[] = []
      const objArray: CompletionItem[] = []
      items.forEach(item => {
        if (isString(item)) {
          stringArray.push(item)
        } else {
          objArray.push(item)
        }
      })

      if (inputValue !== undefined) {
        const selectedEnd = inputRef.current?.selectionEnd
          ? inputRef.current?.selectionEnd
          : 0
        const inputValueSelection = inputValue.slice(0, selectedEnd)
        const inputValueArray: string[] = inputValueSelection.split(
          /[()$="\s*/%+-]+/
        )

        lastInput = inputValueArray[inputValueArray.length - 1]
        setSplitIndex(inputValueSelection.length - lastInput.length)
        onChange?.(inputValue)
        onSelectEnd?.(inputValueSelection)
      }

      setInputItems(
        handleFilterInSearch(objArray, lastInput, {
          keys: ['key']
        }).concat(handleFilterInSearch(stringArray, lastInput))
      )
    },

    stateReducer: (state, actionChanges) => {
      const { type, changes } = actionChanges
      var operators = [
        '<',
        '>',
        '<=',
        '<=',
        '=',
        '!=',
        'IN',
        'IS',
        'CONTAINS',
        'IS NULL',
        'IS NOT NULL',
        'NOT CONTAINS'
      ]

      let logicOperators = ['AND', 'OR']

      function clickItem() {
        inputRef.current?.focus()
        const endString = state.inputValue.slice(
          splitIndex,
          state.inputValue.length
        )
        let array: number[] = []

        specialCharsArray.forEach(char => {
          array.push(endString.indexOf(char))
        })

        array = remove(array, function (n: number) {
          return n !== -1
        })

        const closest = array.length === 0 ? endString.length : min(array)

        const subEndString = endString.slice(closest, endString.length)

        onSelectObject?.(changes.selectedItem)
        if (!isString(changes.selectedItem)) {
          return {
            ...changes,
            inputValue:
              state.inputValue.slice(0, splitIndex) +
              changes.selectedItem.key +
              ' ' +
              subEndString,
            isOpen: true
          }
        } else {
          if (indexOf(operators, changes.selectedItem) !== -1) {
            return {
              ...changes,
              inputValue:
                state.inputValue.slice(0, splitIndex) +
                changes.selectedItem +
                ' ' +
                subEndString,
              isOpen: true
            }
          } else if (indexOf(logicOperators, changes.selectedItem) !== -1) {
            return {
              ...changes,
              inputValue:
                state.inputValue.slice(0, splitIndex) +
                changes.selectedItem +
                ' ' +
                subEndString
            }
          } else {
            return {
              ...changes,
              inputValue:
                state.inputValue.slice(0, splitIndex) +
                '"' +
                changes.selectedItem +
                '" ' +
                subEndString,
              isOpen: true
            }
          }
        }
      }
      switch (type) {
        case useCombobox.stateChangeTypes.InputKeyDownArrowUp:
        case useCombobox.stateChangeTypes.InputKeyDownArrowDown: {
          if (changes?.inputValue === undefined) {
            return { ...changes, isOpen: false }
          }
          let inputValueArray = changes?.inputValue!.split(/AND |OR /)
          let lastStringStartWith$ = inputValueArray[
            inputValueArray.length - 1
          ].startsWith('$')

          return { ...changes, isOpen: true && lastStringStartWith$ }
        }

        case useCombobox.stateChangeTypes.InputKeyDownEnter: {
          if (changes?.selectedItem !== state.selectedItem) {
            return clickItem()
          }
          return {}
        }
        case useCombobox.stateChangeTypes.ItemClick: {
          return clickItem()
        }
        case useCombobox.stateChangeTypes.InputChange: {
          const lastIndex = inputRef.current?.selectionEnd
            ? inputRef.current?.selectionEnd - 1
            : 0

          if (changes?.inputValue!.length === 0) {
            return { ...changes, isOpen: false }
          }

          let inputValueArray = changes?.inputValue!.split(/AND |OR /)
          let lastStringStartWith$ = inputValueArray[
            inputValueArray.length - 1
          ].startsWith('$')

          switch (changes?.inputValue![lastIndex]) {
            default:
              return { ...changes, isOpen: lastStringStartWith$ && true }
          }
        }
        default: {
          return actionChanges.changes
        }
      }
    }
  })
  useImperativeHandle(ref, () => {
    return {
      reset: () => {
        reset()
      }
    }
  })

  useEffect(() => {
    if (!isEqual(previousItems, items)) {
      setInputItems(items)
    }
  }, [items, previousItems])

  return (
    <>
      <div
        ref={inputContainerRef}
        {...getComboboxProps({ className: 'w-full' })}
      >
        <input
          style={{
            display: 'block'
          }}
          {...getInputProps({
            className:
              'outline-none body-2 m-0 w-full ops-text-grey-800 pl-1 overflow-x-scroll',
            ref: inputRef,
            onFocus,
            onBlur,
            placeholder
          })}
          // defaultValue={defaultValue}
          type="text"
          spellCheck={false}
          onKeyDown={onKeyDown}
        />
      </div>

      {items.length > 0 ? (
        <div
          {...getMenuProps()}
          className={`absolute`}
          style={
            isOpen
              ? {
                  display: 'grid',
                  zIndex: 100,
                  marginTop: '0.25rem',
                  width: '45%'
                }
              : { display: 'none' }
          }
        >
          <ul
            className="shadow-sm rounded-sm ops-background body-1 cursor-default relative"
            style={{
              minWidth: '300px',
              border: '1px solid var(--color-grey-200)',
              maxHeight: '330px',
              overflow: 'auto'
            }}
          >
            {isOpen && showObjectList(inputItems)}
            {isOpen && showVariableList(inputItems)}
            {isOpen && showMetricList(inputItems)}
          </ul>
        </div>
      ) : (
        <div
          {...getMenuProps()}
          className={`absolute`}
          style={
            isOpen
              ? {
                  display: 'grid',
                  zIndex: 100,
                  marginTop: '0.25rem',
                  width: '45%'
                }
              : { display: 'none' }
          }
        >
          <ul
            className="shadow-sm rounded-sm ops-background body-1 cursor-default relative"
            style={{
              minWidth: '300px',
              border: '1px solid var(--color-grey-200)',
              maxHeight: '330px',
              overflow: 'auto'
            }}
          >
            <li className={listClassName}>
              <span className="opacity-100">{t('query_builder.no_items')}</span>
            </li>
          </ul>
        </div>
      )}
    </>
  )
}
type ForwardRefFn<R> = <T>(
  props: QueryBuilderProps & React.RefAttributes<R>
) => ReactElement | null

const QueryBuilderInput = forwardRef(QueryBuilderInputTmp) as ForwardRefFn<{
  reset: () => void
}>
export default QueryBuilderInput

export function handleFilterInSearch(
  defaultData: any[],
  searchQuery?: string,
  key?: any
) {
  let threshold = { threshold: matchSorter.rankings.CONTAINS }
  let options = Object.assign(key ? key : {}, threshold)

  const result = searchQuery
    ? matchSorter(defaultData, searchQuery, options)
    : defaultData

  return result
}
