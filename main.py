#!/usr/bin/env python3

from bottle import template
from datetime import datetime
import json
from os import environ
import requests

forecastURL = environ["forecastURL"]
hourlyURL = environ["hourlyURL"]

def getWeatherData(url):
    user_agent = {'User-agent': 'weather forecast google cloud function'}
    response = requests.get(url, headers=user_agent)
    if response.status_code != 200:
        # raise an error
        print("Error - non-200 status code: %s" % response.status_code)
        return "error with API response"

    try:
        responseData = json.loads(response.content)
    except Exception as e:
        print(e)
        return "error parsing JSON"

    return responseData


htmlTemplate = """
<!DOCTYPE html>
<html>
<head>
<title>weather</title>
<style>
body {
    background: #333;
    {{!bodySize}}
}
.all {
    font-family: sans-serif;
    background: white;
    color: black;
    /*position:fixed;*/
    width:100%;
    height:100%;
    top:0px;
    left:0px;
    z-index:1000;
}
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
}
td, th {
    border: 1px solid #8E8E8E;
    text-align: left;
    padding: 8px;
}
@media (prefers-color-scheme: dark) {
  .all { background: #333; color: white; }
}
</style>
</head>

<body>
<div class="all">
{{!generalData}}
<br>
<table>
<tr>
  <th>Time</th>
  <th>Summary</th>
  <th>Temp</th>
</tr>
{{!hourlyData}}
</table>
</div>
</body>
</html>"""

generalTemplate = """
<h3>{name}</h3>
<p>{detailedForecast}</p>"""

hourlyTemplate = """
<tr>
  <td>{time}</td>
  <td>{summary}</td>
  <td>{temp}</td>
</tr>"""


def weatherForecast(request):
    if request.user_agent.platform == "android" or request.user_agent.platform == "iphone":
        bodySizeCSS = "font-size: 1.7em;"
    else:
        bodySizeCSS = ""

    general = getWeatherData(forecastURL)
    if type(general) == str:
        # then there was an error
        return("an error occurred while gathering data")

    generalData = ""
    for i in range(4):
        generalData = generalData + generalTemplate.format(
            name=general['properties']['periods'][i]['name'],
            detailedForecast=general['properties']['periods'][i]['detailedForecast']
        )

    hourly = getWeatherData(hourlyURL)
    if type(hourly) == str:
        # then there was an error
        return("an error occurred while gathering data")

    hourlyData = ""
    hourList = list(range(12)) + list(range(12, 36, 2))
    for i in hourList:
        timeRFC3339 = hourly['properties']['periods'][i]['startTime']
        t = datetime.strptime(timeRFC3339[:timeRFC3339.rfind('-')], '%Y-%m-%dT%H:%M:%S').strftime("%a %m-%d %H:%M")
        hourlyData = hourlyData + hourlyTemplate.format(
            time=t,
            summary=hourly['properties']['periods'][i]['shortForecast'],
            temp=hourly['properties']['periods'][i]['temperature']
        )

    return template(htmlTemplate, generalData=generalData, hourlyData=hourlyData, bodySize=bodySizeCSS)
