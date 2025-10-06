# Data dictionary for Interline Transitland route-oriented dataset

If delivered as a CSV file, this data dictionary refers to the columns in the file.

If delivered as a GeoJSON file, this data dictionary refers to the properties on each feature.

## Schema in brief

The route-oriented tabular output includes three sets of columns:

1) **Route record and metadata \-** e.g., stop name, latitude/longitude  
2) **Agency record and metadata \-** e.g., name of one or more transit agencies serving the stop; name of one or more routes serving the stop; type of vehicle(s) serving the stop  
3) **Route headway data –** quantitative summary of route frequency, based upon service as at a representative stop along the route 
4) **Feed metadata** \- can be used to reference the feed dataset from which relevant records were sourced

## Route record and metadata

* `route_onestop_id` \- Transitland's ID for the route. For more information open https://www.transit.land/routes/\<replace with stop\_onestop\_id​\>    
* `route_short_name` \- A rider facing short name for this route. One or both of (route\_short\_name,route\_long\_name) will be provided.  
* `route_long_name` \- A rider facing longer, descriptive name for this route.  
* `route_desc` \- A rider facing description of the route.  
* `route_type` \- An enum describing the route type. See [Route types](#route-types)
* `route_id` \- GTFS ID for this route (from the source feed)
* `route_intid` \- internal ID for this route _(debug field)_
* `route_color` \- A hex RGB value for representing this route on a map


## Agency information

* `agency_id` \- GTFS ID for this agency  
* `agency_name` \- The rider facing name fo this agency
* `agency_intid`  \- internal ID for this agency _(debug field)_

## Route headway data

Route headway data is calculated for each route direction (routes can have trips in two directions). and day-of-week category (Monday-Friday, Saturday, and Sunday). Route headways are calculated by looking at all service scheduled on a particular day, and selecting a representative stop with the most departing trips. The departure time for each trip visiting that stop in that direction, on that day, is then tallied and stored. Headways are then calculated as the median number of seconds between departing trips within a time window. For example, "headway\_7am\_9am" is the median number of seconds between trips that depart between 7am and 9am. At least 4 trips must occur within the window for a valid result; otherwise it will be left empty. The complete list of departure times is provided if you would like to calculate headways for an arbitrary time of day.

For example, using departure times of \["08:00:00", "08:10:00", "08:18:00", "08:30:00", "08:45:00", "08:52:00"\], we get headway values of \[600, 480, 720, 900, 420\] seconds. The median value in this list (after sorting) is 600 seconds.

Columns:

* `<prefix>_selected_service_date` \- the date selected as having representative service for this route, day of week category, and trip direction  
* `<prefix>_departure_times` \- The departure times from this stop, on this service date, in this direction, as a space-separated list  
* `<prefix>_headway_7am_9am_mean` \- Average calculated headway, in seconds, between the hours of 7am to 9am   
* `<prefix>_headway_9am_4pm_mean` \- Average calculated headway, in seconds, between the hours of 9am to 4pm  
* `<prefix>_headway_4pm_6pm_mean` \- Average calculated headway, in seconds, between the hours of 4pm to 6pm  
* `<prefix>_headway_6pm_7am_mean` \- Average calculated headway, in seconds, between the hours of 6pm to 7am (overnight)  
* `<prefix>_headway_7am_9am_median` \- Median calculated headway, in seconds, between the hours of 7am to 9am   
* `<prefix>_headway_9am_4pm_median` \- Median calculated headway, in seconds, between the hours of 9am to 4pm  
* `<prefix>_headway_4pm_6pm_median` \- Median calculated headway, in seconds, between the hours of 4pm to 6pm  
* `<prefix>_headway_6pm_7am_median` \- Median calculated headway, in seconds, between the hours of 6pm to 7am (overnight)  
* `<prefix>_selected_stop_id` \- GTFS ID of the stop used for headway calculations _(debug field)_
* `<prefix>_selected_stop_intid` \- internal ID for this stop _(debug field)_
* `<prefix>_selected_stop_name` \- A rider facing name for this stop _(debug field)_

Prefixes:

* `hw_best` \- The prefix below with the most number of departures  
* `hw_dow1_dir0` \- Headways for day-of-week category Monday-Friday, in trip direction 0   
* `hw_dow1_dir1` \- Headways for day-of-week category Monday-Friday, in trip direction 1  
* `hw_dow6_dir0` \- Headways for day-of-week category Saturday, in trip direction 0  
* `hw_dow6_dir1` \- Headways for day-of-week category Saturday, in trip direction 1  
* `hw_dow7_dir0` \- Headways for day-of-week category Sunday, in trip direction 0  
* `hw_dow7_dir1` \- Headways for day-of-week category Sunday, in trip direction 1

## Feed metadata

**Columns about the feed from which the route was sourced:**  
This information is primarily used to evaluate data freshness and for debugging purposes.

* `feed_id` \- Transitland's Onestop ID for the source feed. For more information open https://www.transit.land/feeds/\<replace with feed\_id\>  
* `feed_version_sha1` \- identifies the feed version from which the route was sourced
* `feed_version_fetched_at` \- The date and time this feed version was fetched from the source
* `feed_intid` \- internal ID for the feed _(debug field)_
* `feed_version_intid` \- internal ID for the feed version _(debug field)_

## Route types

These are the definitions for the enum integers provided in the `route_type` column.

Defined by the GTFS static specification: [https://gtfs.org/reference/static\#routestxt](https://gtfs.org/reference/static#routestxt)

* `0` \- Tram, Streetcar, Light rail. Any light rail or street level system within a metropolitan area.  
* `1` \- Subway, Metro. Any underground rail system within a metropolitan area.  
* `2` \- Rail. Used for intercity or long-distance travel.  
* `3` \- Bus. Used for short- and long-distance bus routes.  
* `4` \- Ferry. Used for short- and long-distance boat service.  
* `5` \- Cable tram. Used for street-level rail cars where the cable runs beneath the vehicle, e.g., cable car in San Francisco.  
* `6` \- Aerial lift, suspended cable car (e.g., gondola lift, aerial tramway). Cable transport where cabins, cars, gondolas or open chairs are suspended by means of one or more cables.  
* `7` \- Funicular. Any rail system designed for steep inclines.  
* `11` \- Trolleybus. Electric buses that draw power from overhead wires using poles.  
* `12` \- Monorail. Railway in which the track consists of a single rail or a beam.

## Debug fields

Some fields are marked as _(debug field)_ above. These fields are sometimes only in the Transitland Datasets for debugging purposes, but not typically distributed publicly.

## License

Unless otherwise noted, Interline licensed this dataset to users under the [Transitland Terms](https://www.transit.land/terms)