import requests
import json
import argparse

# Base URL for AWS instance metadata
METADATA_URL = "http://169.254.169.254/latest/meta-data/"

def fetch_metadata(base_url, key=None):
    """
    Fetch metadata from AWS instance metadata service.

    :param base_url: The base URL for metadata.
    :param key: Specific key to retrieve (optional).
    :return: Metadata as JSON or specific key value.
    """
    if key:
        url = f"{base_url}{key}"
    else:
        url = base_url

    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()

        if response.text.endswith("/"):  # Indicates more nested keys
            keys = response.text.strip().split("\n")
            metadata = {}
            for k in keys:
                metadata[k] = fetch_metadata(base_url + k)
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

    print(json.dumps(metadata, indent=4))

if __name__ == "__main__":
    main()
