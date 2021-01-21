import React, { useState, useEffect } from 'react'
import { UserNavInfo } from 'context/nav-context'
import { Divider, CardContainer } from 'opsramp-design-system'

type OverviewScreenProps = {
  userNavInfo: UserNavInfo
}

const OverviewScreen: React.FC<OverviewScreenProps> = ({ userNavInfo }) => {
  const [apps, setApps] = useState<any>(undefined)

  useEffect(() => {
    console.log('overview run once')

    let apps = [
      {
        id: 1,
        name: 'Metered Usage Insights',
        image: require('../assets/app-1.png'),
        link: 'https://localhost/metered-usage-insight',
        tag: 'Dashboard'
      },
      {
        id: 2,
        name: 'Asset Insights',
        image: require('../assets/app-2.png'),
        link: 'http://don-mk8s-lb-3c9b790ca6219e7e.elb.us-west-1.amazonaws.com/oap-h',
        tag: 'Financial'
      },
      {
        id: 3,
        name: 'Ops 360',
        image: require('../assets/app-3.png'),
        link: 'http://don-mk8s-lb-3c9b790ca6219e7e.elb.us-west-1.amazonaws.com/oap-g',
        tag: 'Geospatial'
      }
    ]
    setApps(apps)
  }, [])

  return (
    <div className="analytics-apps-wrapper">
      <div className="overview-wrapper w-100 p-4">
        <Divider variant="ops-divider-h" className="w-100 m-0" />

        <h4 className="heading">Available Analytics Apps</h4>

        <div>
          <CardContainer
            className="mx-20"
            cols={[4, 4, 3]}
            defaultCol={2}
            queries={[
              '(min-width: 1500px)',
              '(min-width: 1000px)',
              '(min-width: 800px)'
            ]}
            rows={5}
          >
            {apps &&
              apps.map((app: any, idx: number) => (
                <div
                  key={idx}
                  className="pb-4 border-gray-400 ops-text-grey-900"
                >
                  <div className="w-100">
                    <a
                      href={app.link}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <img
                        className="border-solid border-2 rounded-t-md w-100"
                        src={app.image}
                        alt=""
                      />
                    </a>
                  </div>
                  <div className="text-2xl text-center my-4">{app.name}</div>
                </div>
              ))}
          </CardContainer>
        </div>
        <Divider variant="ops-divider-h" className="w-100 m-0" />
      </div>
    </div>
  )
}
export default OverviewScreen
