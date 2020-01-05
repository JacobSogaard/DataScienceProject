from google.cloud import bigquery
import csv


client = bigquery.Client()

QUERY = (
    'SELECT * FROM `bigquery-public-data.san_francisco.sffd_service_calls` '
    
    'LIMIT 5000')

query_job = client.query(QUERY)
rows = query_job.result()


with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['timestamp', 'gt_long', 'gt_lat'])
    for row in rows:
        writer.writerow([row.timestamp, row.longitude, row.latitude])


