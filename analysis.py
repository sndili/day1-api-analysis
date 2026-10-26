"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error fetching customer data: {error}")
        return[]


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    for key, value in record.items():
        print(" " * indent + f"{key}: {type(value).__name__}")
        if isinstance(value, dict):
            explore(value, indent + 2)


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = []

    for customer in customers:
        rows.append({
            "customer_id": customer["id"],
            "name": customer["name"],
            "username": customer["username"],
            "email": customer["email"],
            "email_domain": customer["email"].split("@")[1],
            "phone": customer["phone"],
            "city": customer["address"]["city"],
            "zipcode": customer["address"]["zipcode"],
            "latitude": float(customer["address"]["geo"]["lat"]),
            "longitude": float(customer["address"]["geo"]["lng"]),
            "company": customer["company"]["name"],
            "website": customer["website"],
        })
    return rows
    

def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {customer["address"]["city"] for customer in customers}


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
    counts = {}

    for customer in customers:
        city = customer["address"]["city"]
        counts[city] = counts.get(city, 0) + 1

    return counts    


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    counts = {}

    for customer in customers:
        domain = customer["email"].split("@")[1]
        top_level_domain = domain.split(".")[-1]
        counts[top_level_domain] = counts.get(top_level_domain, 0) + 1

    return counts       


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def plot_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of the distribution to path."""
    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values)
    plt.title("Customer Distribution by Email Domain")
    plt.xlabel("Email Domain Suffix")
    plt.ylabel("Number of Customers")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()



if __name__ == "__main__":
    # TODO: run each step and print a short findings summary

    customers = get_customers()

    if not customers:
        print("No customer data available. Analysis stopped.")
        raise SystemExit(1)

    print(f"Total customers fetched: {len(customers)}")

    print("\nExploring the first customer record:")
    explore(customers[0])

    rows = extract_attributes(customers)

    cities = unique_cities(customers)
    print(f"\nNumber of unique cities: {len(cities)}")
    print(f"Number of customers: {len(customers)}")

    city_data = city_counts(customers)
    sorted_city_counts = dict(
        sorted(city_data.items(), key=lambda item: (-item[1], item[0]))
    )
    print("\nCustomer counts by city:")
    print(sorted_city_counts)

    domain_data = email_domain_counts(customers)
    sorted_domain_counts = dict(
        sorted(domain_data.items(), key=lambda item: (-item[1], item[0]))
    )
    print("\nCustomer counts by email domain suffix:")
    print(sorted_domain_counts)

    df = to_dataframe(rows)
    print(f"\nDataFrame shape: {df.shape}")
    print("\nDataFrame data types:")
    print(df.dtypes)

    pandas_city_counts = df["city"].value_counts().to_dict()
    print(
        "\nManual city counts match pandas:",
        city_data == pandas_city_counts
    )

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    df.to_csv(output_dir / "customers.csv", index=False)

    city_df = pd.DataFrame(
        [
            {"city": city, "customer_count": count}
            for city, count in sorted_city_counts.items()
        ]
    )
    city_df.to_csv(output_dir / "city_counts.csv", index=False)

    plot_distribution(
        sorted_domain_counts,
        output_dir / "customer_distribution.png"
    )

    print("\nFindings summary:")
    print(f"- Analysed {len(customers)} customers.")
    print(f"- The customers represent {len(cities)} unique cities.")
    print(f"- The data contains {len(sorted_domain_counts)} email domain suffixes.")
    print("\nOutput files saved in the output folder.")