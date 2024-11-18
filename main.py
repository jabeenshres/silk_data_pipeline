import os
import sys
from pymongo import MongoClient
import requests
from dotenv import load_dotenv

# Custom module imports
from data_fetching.qualys_crowdstrike_client import BaseAPIClient
from data_normalization.normalize import normalize_qualys_host, normalize_crowdstrike_host
from data_deduping.dedupe import deduplicate_hosts
from visualizations.visualize import plot_os_distribution, plot_host_age, plot_open_ports_distribution

# Load environment variables from .env file
load_dotenv()

# Read environment variables
TOKEN = os.getenv("TOKEN")
QUALYS_API = os.getenv("QUALYS_API")
CROWD_STRIKE_API = os.getenv("CROWD_STRIKE_API")
MONGO_DB = os.getenv("MONGO_DB")

# Validate critical environment variables
if not TOKEN:
    raise EnvironmentError("API token is not set in the .env file.")
if not QUALYS_API or not CROWD_STRIKE_API:
    raise EnvironmentError("API endpoints are not set in the .env file.")
if not MONGO_DB:
    raise EnvironmentError("MongoDB connection string is not set in the .env file.")


def get_mongo_collection():
    """
    Establish a connection to MongoDB and return the 'hosts' collection.
    """
    client = MongoClient(MONGO_DB)
    db = client["silk_pipeline"]
    return db["hosts"]


def save_hosts_to_db(hosts):
    """
    Save or update hosts in the MongoDB 'hosts' collection.

    :param hosts: List of normalized host dictionaries.
    """
    collection = get_mongo_collection()
    for host in hosts:
        collection.update_one({"host_id": host["host_id"]}, {"$set": host}, upsert=True)


def main():
    """
    Main pipeline execution:
    - Fetch data from APIs.
    - Normalize and deduplicate the data.
    - Save data to MongoDB.
    - Generate visualizations.
    """
    # Initialize API clients
    qualys_client = BaseAPIClient(TOKEN, QUALYS_API)
    crowd_strike_client = BaseAPIClient(TOKEN, CROWD_STRIKE_API)

    # Fetch data from APIs
    try:
        qualys_hosts = qualys_client.fetch_hosts(skip=5, limit=2)
        print("Fetched Qualys Hosts:", qualys_hosts)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred while fetching Qualys hosts: {http_err}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while fetching Qualys hosts: {e}")
        sys.exit(2)

    try:
        crowd_hosts = crowd_strike_client.fetch_hosts(skip=5, limit=2)
        print("Fetched CrowdStrike Hosts:", crowd_hosts)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred while fetching CrowdStrike hosts: {http_err}")
        sys.exit(3)
    except Exception as e:
        print(f"Unexpected error while fetching CrowdStrike hosts: {e}")
        sys.exit(4)

    # Normalize the fetched hosts
    qualys_hosts = [normalize_qualys_host(h) for h in qualys_hosts]
    crowd_hosts = [normalize_crowdstrike_host(h) for h in crowd_hosts]

    # Combine and deduplicate the hosts
    all_hosts = deduplicate_hosts(qualys_hosts + crowd_hosts)
    print("Normalized and Deduplicated Hosts:", all_hosts)

    # Save deduplicated data to MongoDB
    save_hosts_to_db(all_hosts)

    # Generate visualizations
    print("Generating visualizations for all hosts...")
    plot_os_distribution(qualys_hosts, "os_distribution.png", title="Distribution of Hosts by OS (All Sources)")
    plot_host_age(qualys_hosts, "host_age_bar.png", title="Old vs. New Hosts (All Sources)")
    plot_open_ports_distribution(qualys_hosts, "open_ports_distribution.png")

    print("Generating visualizations for CrowdStrike hosts...")
    plot_os_distribution(crowd_hosts, "os_distribution_crowdstrike.png", title="Distribution of Hosts by OS (CrowdStrike)")
    plot_host_age(crowd_hosts, "host_age_bar_crowdstrike.png", title="Old vs. New Hosts (CrowdStrike)")

    print("Pipeline execution completed successfully!")


if __name__ == "__main__":
    main()