from google.cloud import bigquery
import csv


service_request_columns = 19
bikeshare_stations_columns = 7
bikeshare_status_columns = 4
bikeshare_trips_columns = 11
film_locations_columns = 11
sffd_service_calls_columns = 36
sfpd_incidents_columns = 12
street_trees_columns = 18



client = bigquery.Client()

QUERY = (
    'SELECT * FROM `bigquery-public-data.san_francisco.sffd_service_calls` '
    )

query_job = client.query(QUERY)
rows = query_job.result()


selected_table_columns = sffd_service_calls_columns

with open('data_sffd_service_calls.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    fieldnames = []
    for i in range(selected_table_columns):
        fieldnames.append(query_job._query_results._properties['schema']['fields'][i]['name'])

    writer.writerow(fieldnames)

    for row in rows:
        data = []
        for j in range(selected_table_columns):
            data.append(row[j])
            
        writer.writerow(data)

print("all done")

