import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient
import requests

# Custom modules
from data_fetching.api_client import BaseAPIClient
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

# Validate required environment variables
if not TOKEN:
    raise EnvironmentError("API token is not set in the .env file.")
if not QUALYS_API or not CROWD_STRIKE_API:
    raise EnvironmentError("API endpoints are not set in the .env file.")
if not MONGO_DB:
    raise EnvironmentError("MongoDB connection string is not set in the .env file.")


def get_user_input():
    """
    Prompt the user for `skip` and `limit` parameters.
    Ensures the values meet API constraints:
    - skip: Must be between 0 and 5 (inclusive).
    - limit: Must be either 1 or 2.
    :return: Tuple of (skip, limit).
    """
    print("Provide API parameters for fetching data:")
    
    # Get valid input for `skip`
    while True:
        try:
            skip = int(input("Enter skip (0-5): "))
            if 0 <= skip <= 5:
                break
            else:
                print("Invalid value. Skip must be between 0 and 5.")
        except ValueError:
            print("Please enter a valid integer for skip.")

    # Get valid input for `limit`
    while True:
        try:
            limit = int(input("Enter limit (1 or 2): "))
            if 1 <= limit <= 2:
                break
            else:
                print("Invalid value. Limit must be either 1 or 2.")
        except ValueError:
            print("Please enter a valid integer for limit.")

    return skip, limit


def get_mongo_collection():
    """
    Establish a connection to MongoDB and return the 'hosts' collection.

    :return: MongoDB collection object.
    """
    client = MongoClient(MONGO_DB)
    db = client["silk_pipeline"]
    return db["hosts"]


def save_hosts_to_db(hosts):
    """
    Save or update normalized and deduplicated hosts in MongoDB.

    :param hosts: List of dictionaries containing host data.
    """
    collection = get_mongo_collection()
    for host in hosts:
        collection.update_one({"host_id": host["host_id"]}, {"$set": host}, upsert=True)


def main():
    """
    Main pipeline function:
    1. Fetch data from Qualys and CrowdStrike APIs.
    2. Normalize and deduplicate the data.
    3. Save the processed data to MongoDB.
    4. Generate visualizations.
    """
    # Initialize API clients
    qualys_client = BaseAPIClient(TOKEN, QUALYS_API)
    crowd_strike_client = BaseAPIClient(TOKEN, CROWD_STRIKE_API)

    # Get user input for skip and limit parameters
    skip, limit = get_user_input()

    # Fetch hosts from Qualys API
    try:
        print(f"Fetching Qualys hosts with skip={skip} and limit={limit}...")
        qualys_hosts = qualys_client.fetch_hosts(skip=skip, limit=limit)
        print("Fetched Qualys Hosts:", qualys_hosts)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred while fetching Qualys hosts: {http_err}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while fetching Qualys hosts: {e}")
        sys.exit(2)

    # Fetch hosts from CrowdStrike API
    try:
        print(f"Fetching CrowdStrike hosts with skip={skip} and limit={limit}...")
        crowd_hosts = crowd_strike_client.fetch_hosts(skip=skip, limit=limit)
        print("Fetched CrowdStrike Hosts:", crowd_hosts)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred while fetching CrowdStrike hosts: {http_err}")
        sys.exit(3)
    except Exception as e:
        print(f"Unexpected error while fetching CrowdStrike hosts: {e}")
        sys.exit(4)

    # Normalize the data
    qualys_hosts = [normalize_qualys_host(h) for h in qualys_hosts]
    crowd_hosts = [normalize_crowdstrike_host(h) for h in crowd_hosts]

    # Deduplicate and combine data
    all_hosts = deduplicate_hosts(qualys_hosts + crowd_hosts)
    print("Normalized and Deduplicated Hosts:", all_hosts)

    # Save the deduplicated data to MongoDB
    save_hosts_to_db(all_hosts)

    # Fetch all combined hosts from MongoDB
    print("Fetching combined data from MongoDB for visualizations...")
    combined_hosts = list(get_mongo_collection().find({}))

    # Generate visualizations for combined data
    print("Generating visualizations for combined data...")
    plot_os_distribution(combined_hosts, "os_distribution_combined.png", title="Distribution of Hosts by OS (Combined)")
    plot_host_age(combined_hosts, "host_age_combined.png", title="Old vs. New Hosts (Combined)")
    plot_open_ports_distribution(combined_hosts, "open_ports_distribution_combined.png")

    print("Pipeline execution completed successfully!")


if __name__ == "__main__":
    main()
