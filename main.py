from data_fetching.qualys_crowdstrike_client import QualysClient
from data_normalization.normalize import normalize_qualys_host

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

TOKEN = os.getenv("TOKEN")
QUALYS_API = os.getenv("QUALYS_API")
CROWD_STRIKE_API = os.getenv("CROWD_STRIKE_API")

if not TOKEN:
    raise EnvironmentError("API tokens are not set in the .env file.")
    

if not CROWD_STRIKE_API or not QUALYS_API:
    raise EnvironmentError("API end-points are not set in the .env file.")



def main():
    # Fetch data
    qualys_client = QualysClient(TOKEN, QUALYS_API)
    qualys_client.fetch_hosts()
    qualys_hosts = [normalize_qualys_host(h) for h in qualys_client.fetch_hosts()]
    print(qualys_hosts)

if __name__ == "__main__":
    main()