import json
import requests
from constants import VizType, ChartType

class RedashClient(object):
  BASE_URL = "https://sql.telemetry.mozilla.org/api"

  def __init__(self, api_key):
    self.api_key = api_key

  def new_query(self, name, query_string, data_source_id):
    r0 = requests.post(
      self.BASE_URL + "/queries?api_key=" + self.api_key,
      data = json.dumps({"name": name, "query": query_string, "data_source_id": data_source_id}), 
    ).json()

    query_id = r0["id"]

    r1 = requests.post(
      self.BASE_URL + "/queries/" + str(query_id) + "/refresh?api_key=" + self.api_key
    ).json()

    return query_id


  def new_visualization(self, query_id, title="New Visualization", viz_type=VizType.CHART, chart_type=ChartType.BAR):
    return requests.post(
      self.BASE_URL + "/visualizations?api_key=" + self.api_key, 
      data = json.dumps({
        "type": viz_type,
        "name": title,
        "options":{
          "globalSeriesType": chart_type,
          "sortX":True,
          "legend": {"enabled":True},
          "yAxis": [{"type": "linear"}, {"type": "linear", "opposite":True}],
          "xAxis": {"type": "category","labels": {"enabled":True}},
          "seriesOptions":{"count": {
            "type": chart_type,
            "yAxis": 0,
            "zIndex":0, 
            "index":0
          }},
          "columnMapping":{"event":"x","count":"y"},"bottomMargin":50},"query_id":query_id}), 
    ).json()["id"]

  def new_dashboard(self, name):
    return requests.post(
      self.BASE_URL + "/dashboards?api_key=" + self.api_key,
      data = json.dumps({"name": name}), 
    ).json()["id"]

  def append_viz_to_dash(self, dash_id, viz_id, viz_width):
    requests.post(
      self.BASE_URL + "/widgets?api_key=" + self.api_key,
      data = json.dumps({
        "dashboard_id": dash_id,
        "visualization_id": viz_id,
        "width": viz_width,
        "options":{},
        "text":""
      }), 
    ).json()
