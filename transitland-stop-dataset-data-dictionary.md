# Data dictionary for Interline Transitland stop-oriented dataset

If delivered as a CSV file, this data dictionary refers to the columns in the file.

If delivered as a GeoJSON file, this data dictionary refers to the properties on each feature.

## Schema in brief

The stop-oriented tabular output includes four sets of columns:

1) **Stop record and metadata \-** e.g., stop name, latitude/longitude  
2) **Route records and metadata \-** e.g., name of one or more transit agencies serving the stop; name of one or more routes serving the stop; type of vehicle(s) serving the stop  
3) **Transit service –** quantitative summary of the frequency of arrivals/departures for route(s) serving the stop  
4) **Feed metadata** \- can be used to reference the feed dataset from which relevant records were sourced

## Stop record and metadata

**Columns about the stop:**

* `stop_onestop_id` \- Transitland's ID for the stop location. If multiple agencies provide separate records for the same stop location, they will be merged together into a single Onestop ID, assuming lat/lon and name are very similar. For more information open https://www.transit.land/stops/\<replace with stop\_onestop\_id​\>  
* `stop_id` \- transit operator's ID for the stop  
* `stop_name` \- name for the stop, provided by transit operator  
* `stop_desc` \- optional description for the stop, provided by the transit operator  
* `stop_lon` \- longitude coordinate for the stop location  
* `stop_lat` \- latitude coordinate for the stop location
* `stop_intid` \- internal ID for this stop _(debug field)_

## Route records and metadata

**Between 1 and 5 agency and route combinations will be defined in a single stop row. At least 1 agency and route combination will serve the stop:**

* `agency_id_1` \- ID for the transit operator/agency providing service to the stop  
* `agency_name_1` \- name of the transit operator/agency providing service to the stop  
* `route_id_1` \- ID for the route providing service to the stop  
* `route_short_name_1` \- short name for the route providing service to the stop  
* `route_long_name_1` \- long name for the route providing service to the stop  
* `route_type_1` \- vehicle type of the route \[\* see below for a list of the different route vehicle types\]
* `route_color_1` \- A hex RGB value for representing this route on a map
* `agency_intid_1` \- internal ID for the transit operator/agency providing service to the stop _(debug field)_
* `route_intid_1` \- internal ID for the route providing service to the stop _(debug field)_

**If additional agency and route combinations serve the same exact stop, additional columns will have values (using the same definitions as above):**

```agency_intid_1, agency_id_1, agency_name_1, route_intid_1, route_id_1, route_short_name_1, route_long_name_1, route_type_1, agency_intid_2, agency_id_2, agency_name_2, route_intid_2, route_id_2, route_short_name_2, route_long_name_2, route_type_2, agency_intid_3, agency_id_3, agency_name_3, route_intid_3, route_id_3, route_short_name_3, route_long_name_3, route_type_3, agency_intid_4, agency_id_4, agency_name_4, route_intid_4, route_id_4, route_short_name_4, route_long_name_4, route_type_4, agency_intid_5, agency_id_5, agency_name_5, route_intid_5, route_id_5, route_short_name_5, route_long_name_5, route_type_5```

## Transit service/schedule summary

**Columns about the frequency of transit service at the stop:**  
These columns summarize service by counting scheduled departures of one or more routes serving the stop. Interline's Transitland platform uses schedules sourced from transit agencies on a daily basis to inform these calculations. Each dataset delivery will be calculated based for a designated "target week" that is near in time to the delivery date of the dataset.

* `departure_count_dow1` \- Number of trips departing from stop on selected Monday (both directions)
* `departure_count_dow1_dir0` \- Number of trips departing from stop on selected Monday (inbound)
* `departure_count_dow1_dir1` \- Number of trips departing from stop on selected Monday (outbound)

These fields are repeated for all 7 days of the week, from Monday (dow1) to Sunday (dow7):

```departure_count_dow1, departure_count_dow1_dir0, departure_count_dow1_dir1, departure_count_dow2, departure_count_dow2_dir0, departure_count_dow2_dir1, departure_count_dow3, departure_count_dow3_dir0, departure_count_dow3_dir1, departure_count_dow4, departure_count_dow4_dir0, departure_count_dow4_dir1, departure_count_dow5, departure_count_dow5_dir0, departure_count_dow5_dir1, departure_count_dow6, departure_count_dow6_dir0, departure_count_dow6_dir1, departure_count_dow7, departure_count_dow7_dir0, departure_count_dow7_dir1```

## Feed metadata

**Columns about the feed from which the stop was sourced:**  
This information is primarily used to evaluate data freshness and for debugging purposes.

* `feed_id` \- Transitland's Onestop ID for the source feed. For more information open https://www.transit.land/feeds/\<replace with feed\_id\>  
* `feed_version_sha1` \- The date and time this feed version was fetched from the source
* `feed_intid` \- internal ID for the feed _(debug field)_
* `feed_version_intid` \- internal ID for the feed version _(debug field)_

## Route types

These are the definitions for the enum integers provided in the `route_type_1`, `route_type_2`, `route_type_3`, `route_type_4`, and `route_type_5` columns.

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