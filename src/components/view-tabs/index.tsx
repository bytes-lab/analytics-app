import React from 'react'
import { Button } from 'opsramp-design-system'
import { useHistory } from 'react-router-dom'
import { View, ViewProperties } from 'types/views'
import { useViews } from 'context/views-context'

const Tabs: React.FC = () => {
  const history = useHistory()
  const { state: views, dispatch } = useViews()

  function logEvent(message: String) {
    console.log(message)
    return false
  }

  // when the Overview tab is clicked
  function handleOverviewClick() {
    history.push('/infra-ui/overview')
  }

  function handleViewClick(view: View) {
    let resetViews = resetActiveViews()
    resetViews.map(resetView => {
      if (view.viewProperties.name === resetView.viewProperties.name) {
        resetView.viewProperties.active = true
      }
    })
    dispatch({
      type: 'SET_VIEWS',
      payload: resetViews
    })
    // is this a static view tab?
    // if (view.viewProperties.name === 'overview') {
    //   history.push('/infra-ui/overview')
    // }
    // if (view.viewProperties.name === 'resources') {
    //   history.push('/infra-ui/resources')
    // }
  }

  function resetActiveViews() {
    let inactiveViews = views.views
    inactiveViews.map(view => {
      return (view.viewProperties.active = false)
    })
    return inactiveViews
  }

  function handleNewViewClick() {
    let newView: View = {
      createdBy: 0,
      createdTime: Date.now(),
      entityType: 'idunno',
      updatedTime: Date.now(),
      id: Math.floor(Math.random() * 100),
      orgId: 0,
      version: 0,
      viewProperties: {
        name: 'New View',
        label: '',
        active: true,
        query: '',
        url: ''
      },
      visibility: 'PUBLIC' // or 'PRIVATE'
    }

    // make all other tabs inactive, since new one is now active
    let inactiveViews = resetActiveViews()
    // replace whole set of views
    dispatch({
      type: 'SET_VIEWS',
      payload: [...inactiveViews, newView]
    })

    console.log('just chgd views...')

    // add one view to existing set
    dispatch({
      type: 'NEW_VIEW',
      payload: newView
    })
  }

  function displayViewTabLabel(view: ViewProperties) {
    let label: String | undefined = ''
    if (view.query && view.query.length > 0) {
      label = view.query
      if (view.query.length > 25) {
        label = label.substring(0, 25) + '...'
      }
    } else {
      label = view.name
    }
    return label
  }

  return (
    <div className="tabs">
      {/* <Button
        key="overview"
        variant="secondary"
        type="button"
        onClick={() => handleOverviewClick()}
        className="tab"
        title="Overview"
      >
        <span className="label">Overview</span>
      </Button> */}
      {views &&
        views.views.length > 0 &&
        views.views.map(view => (
          <Button
            key={`${view.id} ${view.viewProperties.name}`}
            variant="secondary"
            type="button"
            onClick={() => handleViewClick(view)}
            className={view.viewProperties.active ? 'tab active' : 'tab'}
            title={view.viewProperties.query}
          >
            <span className="label">
              {displayViewTabLabel(view.viewProperties)}
            </span>
            <span
              className="close"
              onClick={e =>
                e.stopPropagation &&
                logEvent('close tab: ' + view.viewProperties.query)
              }
            >
              <i className="icon-close"></i>
            </span>
          </Button>
        ))}

      {views &&
        views.activeView &&
        views.activeView.viewProperties &&
        views.activeView.viewProperties.query &&
        views.activeView.viewProperties.query.length > 0 && (
          <Button variant="icon" type="button" onClick={handleNewViewClick}>
            <i className="text-xl icon-add"></i>
          </Button>
        )}
    </div>
  )
}

export default Tabs
