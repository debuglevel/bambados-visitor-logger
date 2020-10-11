from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBServerError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential
import requests
import datetime
import argparse

def retrieve_visitors():
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'Abp-TenantId': '2115',
        'Abp.TenantId': '2115',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'DNT': '1',
        'Origin': 'https://www.stadtwerke-bamberg.de',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.stadtwerke-bamberg.de/baeder/bambados',
        'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    params = (
        ('organizationUnitIds', '30244'),
    )
    response = requests.get('https://api.ticos-systems.cloud/api/gates/counter', headers=headers, params=params)
    visitor_data = response.json()
    return visitor_data

def get_visitors():
    visitorData = retrieve_visitors()

    current_visitors = visitorData[0]["personCount"]
    maximum_seats = visitorData[0]["maxPersonCount"]
    free_seats = maximum_seats - current_visitors
    current_datetime = datetime.datetime.now()

    return current_visitors, maximum_seats, free_seats, current_datetime

def print_csv(visitor_data):
    current_visitors, maximum_seats, free_seats, current_datetime = visitor_data
    iso8601_timestamp = current_datetime.replace(microsecond=0).isoformat()

    print(f"{iso8601_timestamp};{current_visitors};{free_seats};{maximum_seats}")

def get_influxdblines(visitor_data):
    current_visitors, maximum_seats, free_seats, current_datetime = visitor_data
    nanoseconds_timestamp = int(current_datetime.timestamp() * 1000 * 1000 * 1000)

    influxdb_lines = []
    influxdb_lines.append(f"current value={current_visitors} {nanoseconds_timestamp}")
    influxdb_lines.append(f"maximum value={maximum_seats} {nanoseconds_timestamp}")
    influxdb_lines.append(f"free value={free_seats} {nanoseconds_timestamp}")

    return influxdb_lines

def print_influxdblines(influxdb_lines):
    for influxdb_line in influxdb_lines:
        print(influxdb_line)

@retry(retry=retry_if_exception_type(InfluxDBServerError), stop=stop_after_attempt(20), wait=wait_random_exponential(multiplier=1, max=300))
def write_influxdb(influxdb_connection_data, influxdb_lines):
    influxdb_host, influxdb_port, influxdb_database, influxdb_username, influxdb_password = influxdb_connection_data

    influxdb_client = InfluxDBClient(influxdb_host, influxdb_port, influxdb_username, influxdb_password, influxdb_database)
    influxdb_client.write_points(influxdb_lines, protocol='line')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--print-csv", help="write CSV to stdout", action="store_true")
    parser.add_argument("--print-influxdblines", help="write InfluxDB lines to stdout", action="store_true")
    parser.add_argument("--write-influxdb", help="write InfluxDB lines to InfluxDB", action="store_true")
    parser.add_argument("--influxdb-host", help="InfluxDB host", type=str, default="localhost")
    parser.add_argument("--influxdb-port", help="InfluxDB port", type=int, default=8086)
    parser.add_argument("--influxdb-database", help="InfluxDB database", type=str)
    parser.add_argument("--influxdb-username", help="InfluxDB username", type=str)
    parser.add_argument("--influxdb-password", help="InfluxDB password", type=str)
    args = parser.parse_args()
    
    (visitor_data) = get_visitors()

    if args.print_csv:
        print_csv(visitor_data)
    if args.print_influxdblines:
        print_influxdblines(get_influxdblines(visitor_data))
    if args.write_influxdb:
        (influxdb_connection_data) = args.influxdb_host, args.influxdb_port, args.influxdb_database, args.influxdb_username, args.influxdb_password
        write_influxdb(influxdb_connection_data, get_influxdblines(visitor_data))

if __name__ == "__main__":
    main()
