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
    for token_id in range(1, 11):
        stolen_message = (
            "stolen" if is_stolen(BAYC_CONTRACT_ADDRESS, token_id)
            else "not stolen"
        )

        print(f"{token_id} is {stolen_message}")
        sleep(1)


if __name__ == "__main__":
    main()
