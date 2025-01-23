import requests
import json
import argparse

# Base URL for the metadata service
METADATA_URL = "http://localhost:8080/latest/meta-data/"

def fetch_metadata(base_url, key=None):
    """Fetch metadata from AWS instance metadata service."""
    url = f"{base_url}{key}" if key else base_url

    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()

        # Check if the response contains subkeys (ends with "/")
        if response.text.endswith("/"):
            keys = response.text.strip().split("\n")
            metadata = {}
            for k in keys:
                metadata[k] = fetch_metadata(base_url, key=(key + "/" if key else "") + k)
            return metadata
        else:
            return response.text
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="AWS Instance Metadata Query Tool")
    parser.add_argument(
        "--key", type=str, help="Specific metadata key to retrieve (e.g., 'ami-id')"
    )
    args = parser.parse_args()

    if args.key:
        metadata = fetch_metadata(METADATA_URL, key=args.key)
    else:
        metadata = fetch_metadata(METADATA_URL)

    # Print the metadata in JSON format
    print(json.dumps(metadata, indent=4))

if __name__ == "__main__":
    main()
