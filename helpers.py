from datetime import datetime

def listing_helper(listing) -> dict:
    return {
        "id": str(listing["_id"]),
        "type": listing["type"],
        "availableNow": listing["availableNow"],
        # "ownerId": listing["ownerId"],
        "address": listing["address"],
        "createdAt": listing["createdAt"],
    }
 