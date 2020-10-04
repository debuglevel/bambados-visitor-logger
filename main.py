import requests
import datetime

def main():
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

    j = response.json()
    count = j[0]["personCount"]
    max = j[0]["maxPersonCount"]
    free = max-count

    iso8601 =  datetime.datetime.now().replace(microsecond=0).isoformat()

    print(f"{iso8601};{count};{free};{max}")

if __name__ == "__main__":
    main()