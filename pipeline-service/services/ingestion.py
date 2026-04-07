import requests

def fetch_all_customers():
    page = 1
    limit = 10
    all_data = []

    while True:
        res = requests.get(
            f"http://localhost:5000/api/customers?page={page}&limit={limit}"
        )
        data = res.json()

        all_data.extend(data["data"])

        if len(all_data) >= data["total"]:
            break

        page += 1

    return all_data