This project is licensed under the MIT license.

This project contains a jupyter notebook along with artifacts it produces. The ultimate end is to produce a graph of desktop and mobile pageviews of wikimedia (as well as combined 
views) from december 2007 until present.
In 2015 there was a contract change for the api used to obtain the data that allowed us to get more accurate results by excluding self disclosed web crawler requests. 
The original contract is later deprecated. For the periods where both data sources were collected, both are displayed. 
The first month for which mobile data is present is October 2014.

A csv file is output that is later used to create the graph. The schema is:
year, month, pagecount_all_views, pagecount_desktop_views, pagecount_mobile_views, pageview_all_views, pageview_desktop_views, pageview_mobile_views

Columns prefixed 'pagecount' are from the legacy api, whereas 'pageview' prefix denotes the modern endpoint. 
The pageview mobile views are the sum of both app and mobile web views.

The docs for the legacy api are here:https://wikitech.wikimedia.org/wiki/Analytics/AQS/Legacy_Pagecounts
The docs for the improved api are here:https://wikitech.wikimedia.org/wiki/Analytics/AQS/Pageviews
Terms of use are here:https://wikimedia.org/api/rest_v1/#/Pagecounts_data_(legacy)/get_metrics_legacy_pagecounts_aggregate_project_access_site_granularity_start_end
