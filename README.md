# Device Change Event Metadata

`run_event_analytics.py` is a python script that reads CSV datafiles in the `data-dump` directory, and loads all data into a Pandas dataframe, and outputs some interesting metadata and data visualizations.

Before rendering the metadata and data visualizations, data cleansing is performed on some **key fields** found in the data: `timestamp`, `device_id`, and `event_type`.

Examples of data quality issues found:
- Rows found containing data that did not match the schema. For instance, there were rows that had the `timestamp` missing, which is the first ordinal field in the schema. When timestamp value was missing, the next ordinal field `device_id` took its place instead.
- NULL values for key fields
- Invalid values for key fields

Any rows containing invalid `timestamp`, `device_id`, and `event_type` values were ignored from the statistical outputs of this script.


## Assumptions 

Assumptions regarding the data and task at-hand include the following:

- The files in `data-dump` represent a complete data for a timeframe, and there are no files are missing.

- The removal of rows with malformed data or NULL will not have statistical significance on the resulting metadata and outputs generated.

- For `device_id` and `event_type` fields, the `casefold()` method was used over `lower()` to handle possible non-ascii characters.

- The metadata required for output is limited to saving to the min, max, and mean of the count of each event type per device_id. Therefore,a complete run of the script `device_change_event_metadata.py` results in the following outputs:
	* Intermediate and final aggregations printed to console
	* A file generated in the path `data-dump/metadata` in CSV format containing the Min, Max, and Mean of the Frequency of Events Sent by Devices per Event Type.

## Testing

Testing is rather limited to evaluation of runtime errors. In the future, Unit Testing /mocks should created to ensure proper data types and schemas are found prior to processing. In addition, testing around thresholds of metrics may prove to be useful.

### Language

python3


### Dependencies

matplotlib

pandas

numpy




## How to Run

1) Ensure all folder paths are unzipped. 
2) Ensure python3 runtime environment.
3) Confirm package dependencies are installed. i.e., `pip install matplotlib`
4) Run the following commands in a command-line terminal.

`cd censys`		

`python3 device_change_event_metadata.py`

There will be metadata output to the terminal/console, as well as summary metadata written to data-dump/metadata in CSV format.

The Python script will leverage matplotlib library to render graphics for Histograms.



## Future Extensions

Some possibilities for extending the functionality of this program include the following, in no specified order:

* Log counts of rows ignored, reason for ignoring that row, including the filename and row number of ignored / errored row. 
	* Output to console summary aggregate information on the reason the ignored row.
	* Create data files for ignored rows; intermediate and aggregate
* Output aggregate metadata per `date` to understand when new errors are introduced, and any skew in the data over time.
	* Log which devices emit over a normal threshold of events.
	* Normalize frequency of events by percentile to understand threshold bounds.
	* Create data file for devices with abnormal activity.

