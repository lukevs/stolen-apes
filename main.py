import json
import os
from time import sleep

import requests

OPENSEA_API_KEY = os.environ["OPENSEA_API_KEY"]
BAYC_CONTRACT_ADDRESS = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"


def is_stolen(asset_contract_address: str, token_id: int) -> str:
    url = f"https://api.opensea.io/api/v1/asset/{asset_contract_address}/{token_id}/"
    response = requests.get(
        url, headers={"X-API-KEY": OPENSEA_API_KEY},
    )

    # supports_wyvern is false if stolen
    return not response.json()["supports_wyvern"]


def main():
    stolen_token_ids = []

    for token_id in range(1, 10001):
        message = "not stolen"

        if is_stolen(BAYC_CONTRACT_ADDRESS, token_id):
            message = "stolen"
            stolen_token_ids.append(token_id)
        
        print(f"{token_id} - {message}")

        # rate limit
        sleep(0.1)

    print(f"Total stolen: {len(stolen_token_ids)}")
    with open("stolen.txt", "w") as stolen_file:
        stolen_file.write("\n".join(map(str, stolen_token_ids)))


if __name__ == "__main__":
    main()
