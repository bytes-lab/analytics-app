import React, { useCallback, useEffect, useLayoutEffect, useState } from 'react'
import { Button } from 'opsramp-design-system'
import QueryBuilderInput from './query-builder-input'
import { indexOf, isObject } from 'lodash'
import { useResourceAttributes } from '../../../data/resources'
import { useUserNavInfo } from 'context/nav-context'
import { useViews } from 'context/views-context'

type QueryBuilderProps = {
  defaultValue?: string
  onSearchClicked: any
}

const QueryBuilder: React.FC<QueryBuilderProps> = ({
  defaultValue,
  onSearchClicked
}) => {
  const queryRef = React.useRef<{ reset: () => void } | null>(null)
  const { state: viewsState, dispatch: viewsDispatch } = useViews()
  let operatorsMap = new Map<string, string[]>()

  type CompletionItem = {
    label: string
    key: string
    value: string
  }
  const { data: resourceAttribute } = useResourceAttributes()
  const state = useUserNavInfo()
  // console.log(state)

  let resourceTypeValue = [
    {
      id: 1,
      name: 'Work Station',
      path: 'Desktop >> Work Station'
    },
    {
      id: 59,
      name: 'Android',
      path: 'Mobile >> Android'
    }
  ]

  let couldServiceProviderValue = [
    {
      providerType: 'AZURE',

      accounts: ['apple_ID', 'Banana_ID', 'cherry_ID'],
      resources: [
        {
          loadBalanaces: 1,
          models: 2,
          operationManagement: 5
        }
      ]
    },
    {
      providerType: 'GOOGLE CLOUD',
      accounts: ['Apple_ID', 'Banana_ID', 'Cherry_ID'],
      resources: [
        {
          loadBalanaces: 1,
          models: 2,
          operationManagement: 5
        }
      ]
    }
  ]

  let valueTypeList = [
    'string',
    'keyword',
    'number',
    'boolean',
    'data',
    'collection'
  ]
  operatorsMap.set('stringOperators', [
    '=',
    '!=',
    'IS',
    'CONTAINS',
    'NOT CONTAINS',
    'IN',
    'IS NULL',
    'IS NOT NULL'
  ])
  operatorsMap.set('keywordOperators', [
    '=',
    '!=',
    'IS',
    'CONTAINS',
    'NOT CONTAINS',
    'IN',
    'IS NULL',
    'IS NOT NULL'
  ])
  operatorsMap.set('numberOperators', [
    '<',
    '<=',
    '>',
    '>=',
    '=',
    '!=',
    'IN',
    'IS',
    'IS NULL',
    'IS NOT NULL'
  ])
  operatorsMap.set('booleanOperators', ['IS'])
  operatorsMap.set('dateOperators', ['=', '<', '<=', '>', '>='])
  operatorsMap.set('collectionOperators', [
    'CONTAINS',
    'NOT CONTAINS',
    'IS NULL',
    'IS NOT NULL'
  ])
  operatorsMap.set('logicalOperators', ['AND', 'OR'])
  operatorsMap.set('booleanValues', ['true', 'false'])
  operatorsMap.set('restTaskOperators', [
    '<',
    '<=',
    '>',
    '>=',
    '=',
    '!=',
    'IS',
    'IS NULL',
    'IS NOT NULL',
    'CONTAINS',
    'NOT CONTAINS'
  ])

  const [items, setItems] = useState([] as any[])
  const [onSelectEnd, setOnSelectEnd] = useState('')
  const [currentQuery, setCurrentQuery] = useState('')
  // let selectObject = {} as CompletionItem
  const [onSelectObject, setOnSelectObject] = useState({} as CompletionItem)
  useEffect(() => {
    if (resourceAttribute) {
      setItems(resourceAttribute)
    }
  }, [resourceAttribute])

  useEffect(() => {
    queryRef?.current?.reset()
  }, [defaultValue])

  useEffect(() => {
    let couldServiceProviderValueArray: string[] = []
    couldServiceProviderValue.forEach(value => {
      couldServiceProviderValueArray.push(value.providerType)
    })
    operatorsMap.set(
      'couldServiceProviderValues',
      couldServiceProviderValueArray
    )
  }, [couldServiceProviderValue, operatorsMap])

  useEffect(() => {
    let resourceTypeValueArray: string[] = []
    resourceTypeValue.forEach(value => {
      resourceTypeValueArray.push(value.name)
    })
    operatorsMap.set('resourceTypeValues', resourceTypeValueArray)
  }, [resourceTypeValue, operatorsMap])

  const checkListsCallback = useCallback(
    (onSelectEnd, value, key) => {
      let inputArray = onSelectEnd.split(/AND |OR /)
      let currentStringArray = inputArray[inputArray.length - 1].split(
        /[()\s]+/
      )

      let currentStringArrayLength = currentStringArray.length
      let preWord = currentStringArray[currentStringArrayLength - 2]
      let operator =
        valueTypeList.indexOf(value) === -1
          ? 'restTaskOperators'
          : `${value}Operators`

      if (
        preWord &&
        preWord.length > 1 &&
        (preWord.endsWith('"') || preWord.endsWith(')'))
      ) {
        setItems(operatorsMap.get('logicalOperators')!)
        return
      }

      if (currentStringArrayLength === 1 && resourceAttribute) {
        setItems(resourceAttribute)
      } else if (currentStringArrayLength === 2) {
        setItems(operatorsMap.get(operator)!)
      } else {
        if (
          key &&
          indexOf(['resourceType', 'cloudServiceProvider'], key) !== -1
        ) {
          if (operatorsMap.get(`${key}Values`)) {
            setItems(operatorsMap.get(`${key}Values`)!)
          }
        } else if (value === 'boolean') {
          setItems(operatorsMap.get(`${value}Values`)!)
        } else {
          setItems([])
        }
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [resourceAttribute]
  )

  useLayoutEffect(() => {
    checkListsCallback(onSelectEnd, onSelectObject.value, onSelectObject.key)
  }, [onSelectEnd, onSelectObject, checkListsCallback])

  function getEnterPress(e: any) {
    if (e.nativeEvent.code === 'Enter') {
      onSearchClicked(currentQuery)
    }
  }

  function clickTest() {
    console.log('click test', currentQuery)
    onSearchClicked(currentQuery)
  }

  useEffect(() => {
    console.log('query updated', currentQuery)
  }, [currentQuery])

  return (
    <div className="search-section py-4 flex items-center">
      <div className="bg-white w-full flex search-bar items-center">
        <div className="search-icon mr-2 ml-3">
          <Button type="button" variant="icon" onClick={clickTest}>
            <i className="icon-search" style={{ fontSize: '1rem' }}></i>
          </Button>
        </div>
        <div className="w-full pr-4">
          <QueryBuilderInput
            defaultValue={defaultValue}
            ref={queryRef}
            items={items}
            onChange={query => {
              setCurrentQuery(query)
            }}
            onSelectEnd={onSelectEnd => {
              setOnSelectEnd(onSelectEnd)
            }}
            onSelectObject={object => {
              setTimeout(() => {
                if (isObject(object)) {
                  setOnSelectObject(object)
                }
              })
            }}
            placeholder="Select"
            onKeyDown={getEnterPress}
          />
        </div>
        {/* TODO save and pin the advance search */}
        {/* <div className="favorite-toggle mr-2">
          <Button type="button" variant="icon">
            <i className="icon-star" style={{ fontSize: '1rem' }}></i>
          </Button>
        </div> */}
      </div>

      {/* <div className="query-actions ml-4">
        <Button className="m-1 disabled" type="button" variant="icon">
          <i className="text-xl icon-pin"></i>
        </Button>
        <Button className="m-1 disabled" type="button" variant="icon">
          <i className="text-xl icon-notepad"></i>
        </Button>
        <Button className="m-1 disabled" type="button" variant="icon">
          <i className="text-xl icon-more"></i>
        </Button>
      </div> */}
    </div>
  )
}

export default QueryBuilder
