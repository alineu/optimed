import requests
import requests_cache

FLUSH_PERIOD = 10 * 60  # 10 minutes in seconds
requests_cache.install_cache(expire_after=FLUSH_PERIOD)

def get_local_IP_address():
    return requests.get('https://api.ipify.org').text


def get_location(ip_address):
    """Return city, country, latitude, and longitude for a given IP address."""

    response = requests.get(f'http://ip-api.com/json/{ip_address}',
                            headers={'User-Agent': 'wqu_weather_app'})
    data = response.json()
    keys = ('city', 'country', 'lat', 'lon', 'timezone')

    return {key: data[key] for key in keys}

