import React from 'react'

const Sidebar: React.FC = () => {
  // for new nav
  // const sidebarLinks = [
  //   {
  //     icon: 'icon-resource',
  //     label: 'Resources'
  //   },
  //   {
  //     icon: 'icon-event',
  //     label: 'Alerts'
  //   },
  //   {
  //     icon: 'icon-alert',
  //     label: 'Incidents'
  //   },
  //   {
  //     icon: 'icon-service-map',
  //     label: 'Service Map'
  //   },
  //   {
  //     icon: 'icon-patching',
  //     label: 'Patching'
  //   },
  //   {
  //     icon: 'icon-infra-topology',
  //     label: 'Topology'
  //   },
  //   {
  //     icon: 'icon-graph-honeycomb',
  //     label: 'Honeycomb'
  //   }
  // ]

  const itomSidebarLinks = [
    {
      id: 'devicetype',
      title: 'Resources',
      className: 'tbIcon resources',
      href: '/newInventory.do?action=layout&showTab=devicetype'
    },
    {
      id: 'devicegroup',
      title: 'Groups',
      className: 'tbIcon resourceGroups',
      href: '/newInventory.do?action=layout&showTab=devicegroup'
    },
    {
      id: 'devicelocation',
      title: 'Sites',
      className: 'tbIcon sites',
      href: '/newInventory.do?action=layout&showTab=devicelocation'
    },
    {
      id: 'servicegroup',
      title: 'Services',
      className: 'tbIcon services',
      href: '/newInventory.do?action=layout&showTab=servicegroup'
    },
    {
      id: 'nwmap',
      title: 'Topology',
      className: 'tbIcon nwmap',
      href: '/newInventory.do?action=layout&showTab=nwmap'
    },
    {
      id: 'main',
      title: 'Maint',
      className: 'tbIcon maint',
      href: '/newInventory.do?action=layout&showTab=main'
    },
    {
      id: 'activity',
      title: 'Activity',
      className: 'tbIcon activity',
      href: '/newInventory.do?action=layout&tab=activity'
    },
    {
      id: 'containers',
      title: 'Containers',
      className: 'tbIcon containers',
      href: '/newInventory.do?action=layout&tab=containers'
    }
  ]

  return (
    <>
      {/*
      // this is the new sidebar
      <div className="sidebar mr-4 rounded">
        <ul className="sidebar-links">
          {sidebarLinks &&
            sidebarLinks.map(link => (
              <li className="sidebar-link" key={link.label}>
                <i className={link.icon}></i>
                <span className="sidebar-link-label">{link.label}</span>
              </li>
            ))}
        </ul>
      </div>
      */}

      <div id="leftDiv" style={{height: '100vh'}}>
        <div title="Resource Search" className="resourceSearch">
          <a href="/portal/analytics-apps/resources">
            <i className="icon-search"></i>
            <span>Search</span>
          </a>
        </div>
        {itomSidebarLinks.map(link => (
          <a
            id={link.id}
            key={link.id}
            title={link.title}
            className={link.className}
            href={link.href}
          >
            <span>{link.title}</span>
          </a>
        ))}
      </div>
    </>
  )
}

export default Sidebar
