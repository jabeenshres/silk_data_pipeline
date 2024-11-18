from pymongo import MongoClient
import requests
from data_fetching.qualys_crowdstrike_client import BaseAPIClient

# from data_fetching.crowdstrike_client import CrowdstrikeClient
from data_normalization.normalize import normalize_qualys_host, normalize_crowdstrike_host
from data_deduping.dedupe import deduplicate_hosts
from visualizations.visualize import plot_os_distribution, plot_host_age, plot_open_ports_distribution
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("TOKEN")
QUALYS_API = os.getenv("QUALYS_API")
CROWD_STRIKE_API = os.getenv("CROWD_STRIKE_API")
MONGO_DB = os.getenv("MONGO_DB")


if not TOKEN:
    raise EnvironmentError("API tokens are not set in the .env file.")
    

if not CROWD_STRIKE_API or not QUALYS_API:
    raise EnvironmentError("API end-points are not set in the .env file.")

def get_mongo_collection():
    client = MongoClient(MONGO_DB)
    db = client["silk_pipeline"]
    return db["hosts"]

def save_hosts_to_db(hosts):
    collection = get_mongo_collection()
    for host in hosts:
        collection.update_one({"host_id": host["host_id"]}, {"$set": host}, upsert=True)



def main():
    # Fetch data
    qualys_client = BaseAPIClient(TOKEN, QUALYS_API)
    crowd_strike_client = BaseAPIClient(TOKEN, CROWD_STRIKE_API)

    try:
        qualys_hosts = qualys_client.fetch_hosts(skip=5, limit=2)
        print("Qualys Hosts:", qualys_hosts)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        sys.exit(1)  # Exit with code 1 to signal failure
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(2)  # Exit with a different code for unexpected errors

    try:
        crowd_hosts = crowd_strike_client.fetch_hosts(skip=5, limit=2)
        print("Crowd Strike Hosts:", crowd_hosts)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
        sys.exit(3)  
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(4)  

    # Normalize Hosts
    qualys_hosts = [normalize_qualys_host(h) for h in qualys_hosts]
    crowd_hosts = [normalize_crowdstrike_host(h) for h in crowd_hosts]
    # Combine and Deduplicate

    all_hosts = deduplicate_hosts(qualys_hosts + crowd_hosts)
    """
    Displaying Normalized all hosts
    """
    print(all_hosts)
    # Save to MongoDB
    save_hosts_to_db(all_hosts)

    # Visualize Data
    print("Generating visualizations for all hosts...")
    plot_os_distribution(qualys_hosts, "os_distribution.png", title="Distribution of Hosts by OS (All Sources)")
    plot_host_age(qualys_hosts, "host_age_bar.png", title="Old vs. New Hosts (All Sources)")
    plot_open_ports_distribution(qualys_hosts, "open_ports_distribution.png")

    print("Generating visualizations for CrowdStrike hosts...")
    plot_os_distribution(crowd_hosts, "os_distribution_crowdstrike.png", title="Distribution of Hosts by OS (CrowdStrike)")
    plot_host_age(crowd_hosts, "host_age_bar_crowdstrike.png", title="Old vs. New Hosts (CrowdStrike)")

if __name__ == "__main__":
    main()