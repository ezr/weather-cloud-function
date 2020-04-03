# weather-cloud-function
A google cloud function to fetch and display the weather forecast

### Motivation
I wanted a basic weather site to show me the forecast. It should load quickly on a poor data connection. I wasn't happy with available web sites which felt bloated or with Android apps that would run in the background and asked for unneeded permissions.
I also made this to learn about google cloud functions.

### Setup
- Download this git repo and cd into it
- Update urls.yaml with URLs for areas that you're interested in. [This link](https://www.weather.gov/documentation/services-web-api) has info on how to find URLs. If you don't update the URLs then you'll get the forecast for Fargo, ND.
- Set up your google account and the cloud SDK as described [here](https://cloud.google.com/functions/docs/first-python#creating_a_gcp_project_using_cloud_sdk).
- Once you have the gcloud command working, run `gcloud functions deploy weatherForecast --runtime python37 --trigger-http --allow-unauthenticated --env-vars-file urls.yaml`. Success should look something like this:
```$ gcloud functions deploy weatherForecast --runtime python37 --trigger-http --allow-unauthenticated --env-vars-file urls.yaml
Deploying function (may take a while - up to 2 minutes)...done.
availableMemoryMb: 256
entryPoint: weatherForecast
environmentVariables:
  forecastURL: https://api.weather.gov/gridpoints/FGF/99,57/forecast
  hourlyURL: https://api.weather.gov/gridpoints/FGF/99,57/forecast/hourly
httpsTrigger:
  url: https://us-region-projectname.cloudfunctions.net/weatherForecast
ingressSettings: ALLOW_ALL
labels:
  deployment-tool: cli-gcloud
name: projects/projectname/locations/us-region/functions/weatherForecast
runtime: python37
serviceAccountEmail: projectname@appspot.gserviceaccount.com
sourceUploadUrl: https://storage.googleapis.com/gcf-upload-us-region-UUID/UUID/UUID.zip?GoogleAccessId=service-blablablablablablablablablablablablablablablablablabla
status: ACTIVE
timeout: 60s
updateTime: '2020-04-03T18:00:04.164Z'
versionId: '9'
```
 
Visit the httpsTrigger in a browser to get the forecast.
