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

    data = response.json()

    return not (data.get("success", True) and data.get("supports_wyvern", True))


def main():
    total_stolen = 0

    with open("stolen.txt", "a") as stolen_file:
        for token_id in range(1, 10001):
            message = "not stolen"

            if is_stolen(BAYC_CONTRACT_ADDRESS, token_id):
                message = "stolen"
                stolen_file.write(f"{token_id}\n")
                total_stolen += 1
            
            print(f"{token_id} - {message}")

            # rate limit
            sleep(0.1)

    print(f"Total stolen: {total_stolen}")


if __name__ == "__main__":
    main()
