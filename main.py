import requests
import datetime

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

def print_csv():
    current_visitors, maximum_seats, free_seats, timestamp = get_visitors()
    iso8601_timestamp = timestamp.replace(microsecond=0).isoformat()
    print(f"{iso8601_timestamp};{current_visitors};{free_seats};{maximum_seats}")

def main():
    print_csv()

if __name__ == "__main__":
    main()