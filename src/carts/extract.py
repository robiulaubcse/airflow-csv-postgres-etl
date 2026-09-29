import json
import urllib.request


API_URL = "https://dummyjson.com/carts"


def fetch_carts(skip=0, limit=30):
    url = f"{API_URL}?skip={skip}&limit={limit}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode())

    return data


def fetch_all_carts():
    all_carts = []
    skip = 0
    limit = 30

    while True:
        data = fetch_carts(skip=skip, limit=limit)

        carts = data["carts"]
        all_carts.extend(carts)

        skip += limit

        if skip >= data["total"]:
            break

    return all_carts