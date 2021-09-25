
## Analytics Apps

### Setup/Installation (Local)

### Python Version

This app is using python 3.x and pip3. Recommended to use virtual env.

### Setting environment variables

To run the metered-usage-insights app locally, you’ll want to set some environment variables in order for the local app to run successfully.

Set the following variables:

-   PLATFORM_ROUTE=analytics-apps (this is required for proper routing to assets when running in portal)
-   DATA_API_BASE_URL=[https://asura.opsramp.net](https://asura.opsramp.net)
-   APP_SERVICE_BASE_URL=[http://13.57.187.238:8001/oap-api/v1](http://13.57.187.238:8001/swagger) (analysis api service)
-   OAP_APP_ID=32a1bc14-c471-46a4-9b0a-835b4b80e58f (this is the installed app id)
-   INCLUDE_WRAPPER=true (this is required for the sidebar to show)
-   ON_PROXY=true (this is required for connecting api service)

**Setting a variable:** export PLATFORM_ROUTE=analytics-apps

**Reading a variable:** echo $PLATFORM_ROUTE

**Remove a variable:** unset PLATFORM_ROUTE

**Show all variables:** printenv

### Installing App requirements

You will need to run the following command to install the app’s required dependencies:

pip3 install -r requirements.txt

### Updating App requirements

To update to the latest version of the analytics-sdk utilities, you will need to run the following:

pip3 install --upgrade opsramp-analytics-utils

### Running the App

Go to analytics-app/metered-usage-insights and run the following:

python3 app.py

The app will be running on port 8050

### Docker

There is a Dockerfile included with the app:  
  
Build the image: docker build -t python-test-01 .

Run the image: docker run -d -p 8050:8050 python-test-01


## Running Application Portal & React Apps locally with a proxy

This document will explain how to run one or more of our React applications together in your local dev environment. The goal is to have the entire application running end to end under the hostname [https://localhost.](https://localhost.)


### Application Portal (required)

The Application Portal is required to run our other React apps as it wraps our other React micro-frontend applications (navbar + application listed above) and passes data between itom and our React applications. The Application Portal also contains the code to run our frontend proxy.

The proxy is key to running all our applications (which run on separate ports) under the same localhost domain. It is comprised of a Docker container that runs haproxy.

You will need to have Docker running in order to use the proxy. (Docker Desktop shown with proxy running)

### How to run proxy

-   Go to /proxy folder in the application-portal codebase
-   Choose an environment to run as your backend. Currently, shivalik and asura are configured
-   Run `sh start.sh shivalik` or `sh start.sh asura`
-   If you are using Windows, you can just look inside the .sh files and run the Docker commands directly that you find there

### How to stop proxy

-   Run the stop.sh script

**Steps for Install/run the applications (frontend only running locally, apis are remote)**

1.  Download all repos for the apps you want to run locally
2.  Do a yarn install and yarn start on new_ui (Application Portal), then for any of the following: dnm-ui, dash-ui, infra-ui etc

1.  All started apps should open new browser windows, and show [http://localhost:8888](http://localhost:8888)/portal (application-portal), [http://localhost:8889](http://localhost:8889)/dash-ui (everest-ui), [http://localhost:8891](http://localhost:8891) (infra-ui) and [http://localhost:8890/dnm-ui](http://localhost:8890/dnm-ui) (dnm-ui)
2.  _* All will likely display errors - THIS IS OK! - this is caused by the specified ports in the urls - ignore these errors and close the spawned windows for these applications. You won't be using them._

4.  Open [https://localhost](https://localhost) in your browser and if the proxy is running correctly you will see the OpsRamp login screen.
5.  Login using the appropriate environment credentials so you have a valid session
6.  Now if you visit any of the OpsRamp pages that are React pages, they'll be running from your local running version alongside the remote Opsramp - you're now basically running the entire stack locally.

### Getting proxy to run in Linux

We discovered an issue where the proxy did not seem to understand `host.docker.internal` and the fix required a change in the proxy/docker-compose.yml file  
  
You will need to add:

extra_hosts:

  -  'host.docker.internal:172.17.0.1'  #host and ip

### Deploy
It is pushed to a [Harbor Repository](https://hub.opsramp.com/harbor/projects/5/repositories) and a [helm chart](https://hub.opsramp.com/harbor/projects/5/helm-charts) is ready for it.

It can be deployed using the help chart on the server.

```
export HELM_EXPERIMENTAL_OCI=1
helm chart save metered-usage-insight-0.1.0.tgz hub.opsramp.com/analytics-apps/metered-usage-insight
helm chart push hub.opsramp.com/analytics-apps/metered-usage-insight:0.1.0
```

```
alias helm="microk8s helm3"
export HELM_EXPERIMENTAL_OCI=1
helm chart pull hub.opsramp.com/analytics-apps/metered-usage-insight:0.1.0
helm chart export hub.opsramp.com/analytics-apps/metered-usage-insight:0.1.0
helm install metered-usage-insight ./metered-usage-insight
```

To upgrade:

- pull and export the chart again.

```
helm upgrade metered-usage-insight ./metered-usage-insight
```

_In case, it does not work, try this_

```
helm uninstall metered-usage-insight
helm install metered-usage-insight ./metered-usage-insight
```
