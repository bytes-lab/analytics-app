import React, { useState, useEffect, useRef } from 'react'
import Tabs from '../components/view-tabs'
import QueryBuilder from '../modules/resources/queryBuilder'
import Sidebar from '../components/sidebar'
import Grid from '../modules/resources/grid'
import { UserNavInfo, useUserNavInfo } from 'context/nav-context'
import { useViews } from 'context/views-context'
import { useResourceGrid } from 'context/resource-grid-context'
import { Button, Divider, Popover } from 'opsramp-design-system'
import ColumnMgmt from '../modules/resources/grid-menu'
// import { Select } from '../components/select'
import { getStatuses } from 'api/resources-api'
import DropDown from '../components/dropdown'
import { resourceStates } from '../modules/resources/resource-states'
import { gridFilters } from '../modules/resources/grid-filters'
import { View } from '../types/views'
import { GridSummary } from '../modules/resources/grid-summary'
import { getInventory, getColumns } from 'api/resources-api'

type ResourcesScreenProps = {
  userNavInfo: UserNavInfo
}

const ResourcesScreen: React.FC<ResourcesScreenProps> = ({ userNavInfo }) => {
  console.log('resources screen loading')

  const { state: viewsState, dispatch: viewsDispatch } = useViews()
  const { state: gridContext, dispatch: gridDispatch } = useResourceGrid()
  const [activeView, setActiveView] = useState<View | undefined>(undefined)
  const popoverContainer = useRef(null)
  const userNavInfos = useUserNavInfo()

  // useEffect(() => {
  //   console.log('run once useEffect')
  //   // clear grid
  //   gridDispatch({
  //     type: 'UPDATE_GRID',
  //     payload: {
  //       columns: undefined,
  //       rows: undefined
  //     }
  //   })
  // }, [])

  function populateGrid(q: any) {
    console.log('pop grid?', q, viewsState.activeView)
    if (q) {
      // store in context
      let inactiveViews = viewsState.views
      inactiveViews.map(view => {
        return (view.viewProperties.active = false)
      })

      let currentView = viewsState.activeView
      currentView.viewProperties.query = q
      currentView.viewProperties.name = q
      currentView.viewProperties.label = q
      inactiveViews.push(currentView)
      viewsDispatch({
        type: 'SET_VIEWS',
        payload: inactiveViews
      })
      viewsDispatch({
        type: 'ACTIVE_VIEW',
        payload: currentView
      })
    }
    getColumns().then(cols => {
      getInventory(userNavInfo.clientId).then(rows => {
        gridDispatch({
          type: 'UPDATE_GRID',
          payload: {
            columns: cols,
            rows: rows
          }
        })
      })
    })
  }

  // userNavInfo.clientId, userNavInfo.mspId
  useEffect(() => {
    // console.log('clientId chgd', userNavInfo.clientId, userNavInfo.mspId)
    let unmounted = false
    if (!unmounted && userNavInfo.clientId !== 0 && userNavInfo.mspId !== 0) {
      getColumns().then(cols => {
        // remove bad properties from all items before passing to ag-grid
        // cols.selectedColumns.forEach(function (v) {
        //   delete v.customField
        //   delete v.formatter
        //   delete v.visible
        //   delete v.title
        //   delete v.id
        // })

        // let okColumns = [
        //   'name',
        //   'ipAddress',
        //   'osName',
        //   'make',
        //   'model',
        //   'technologies',
        //   'lassetManagedTime'
        // ]

        // const person = {
        //   fname: 'tom',
        //   lname: 'jerry',
        //   aage: 100
        // }

        // let newPerson = {}

        // ({ fname: newPerson.fname, lname: newPerson.lname } = person)

        // console.log(newPerson)

        getInventory(userNavInfo!.clientId).then(rows => {
          // TODO: filtering our rows...
          // setIpfilter(
          //   [...new Set(result.devices.map(item => item.ipAddress))].map(
          //     devices => ({
          //       value: devices,
          //       label: devices
          //     })
          //   )
          // )
          gridDispatch({
            type: 'UPDATE_GRID',
            payload: {
              columns: cols,
              rows: rows
            }
          })
        })
      })
    }
    return () => {
      unmounted = true
    }
  }, [gridDispatch, userNavInfo])

  // viewsState.views, viewsState.activeView
  useEffect(() => {
    function getActiveView() {
      if (
        viewsState.views.filter(v => v.viewProperties.active === true).length >
        0
      ) {
        return viewsState.views.filter(v => v.viewProperties.active === true)[0]
      } else {
        return undefined
      }
    }
    setActiveView(
      viewsState.views.filter(v => v.viewProperties.active === true)[0]
    )
  }, [viewsState])

  return (
    <div className="infrastructure-wrapper">
      <Sidebar></Sidebar>

      <div className="resources-wrapper w-100 p-4">
        <Tabs />

        <Divider variant="ops-divider-h" className="w-100 m-0 mt-5" />

        <QueryBuilder
          defaultValue={viewsState.activeView.viewProperties.query}
          onSearchClicked={populateGrid}
        />

        {/* <small>
          <table className="table-fixed w-100">
            <thead>
              <tr>
                <th className="whitespace-normal p-2">viewState.savedViews</th>
                <th className="whitespace-normal p-2">viewState.views</th>
                <th className="whitespace-normal p-2">viewState.activeView</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>n/a</td>
                <td>
                  {JSON.stringify(viewsState.views).replaceAll(',', ', ')}
                </td>
                <td>
                  {JSON.stringify(viewsState.activeView).replaceAll(',', ', ')}
                </td>
              </tr>
            </tbody>
          </table>
        </small>
        <Divider variant="ops-divider-h" className="w-100 m-0" /> */}

        {viewsState &&
          viewsState.activeView &&
          viewsState.activeView.viewProperties.query &&
          viewsState.activeView.viewProperties.query.length > 0 && (
            <div className="content-placeholder w-100 rounded">
              <div className="grid-container w-100">
                <div className="header-section p-4">
                  <div className="header-text">Resources</div>

                  <div className="header-tools flex justify-items-center items-center">
                    {/* <span className="reset-span">Reset</span> */}

                    {gridFilters &&
                      gridFilters.map(filter => (
                        <DropDown
                          key={filter.name}
                          // containerClasses="border-solid rounded-full border py-2 px-5"
                          disabled={false}
                          hideSearch={false}
                          items={filter.items}
                          initialValue={filter.name}
                          containerClasses="ml-3"
                          toggleButtonClasses="border-solid rounded-full border py-2 px-5"
                          filterHandler={(e, i) => {
                            console.log('filterHandler', e, i)
                            return filter.items
                          }}
                          onChange={e => {
                            console.log('onChange', e)
                          }}
                        />
                      ))}

                    <div ref={popoverContainer} className="ml-3">
                      <Popover
                        className="inline-block mx-auto"
                        placement="bottom"
                        action="click"
                        zIndex={20}
                        content={<ColumnMgmt />}
                      >
                        <Button type="button" variant="icon">
                          <i className="icon-more"></i>
                        </Button>
                      </Popover>
                    </div>
                  </div>
                </div>

                <div className="rounded shadow  overflow-hidden">
                  {/* <GridSummary /> */}
                  <Grid clientId={userNavInfo.clientId}></Grid>
                </div>
              </div>
            </div>
          )}
      </div>
    </div>
  )
}
export default ResourcesScreen
