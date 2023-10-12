import requests

DASHBOARD_API_URL = "http://host.docker.internal:80/flags"


def fetch_feature_flags():
    response = requests.get(DASHBOARD_API_URL)
    if response.status_code == 200:
        flags_data = response.json()
        return {flag["name"]: flag["enabled"] for flag in flags_data}
    return {}

