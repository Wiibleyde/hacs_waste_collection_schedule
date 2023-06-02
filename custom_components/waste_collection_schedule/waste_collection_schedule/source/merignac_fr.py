import logging
from datetime import datetime

import requests
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Mérignac"
DESCRIPTION = "Source for Mérignac rubbish collection."
URL = "https://opendata.bordeaux-metropole.fr/api/explore/v2.1/catalog/datasets/en_frcol_s/exports/json?lang=fr&facet=facet(name%3D%22jour_col%22%2C%20disjunctive%3Dtrue)&refine=commune%3A%22M%C3%A9rignac%22&timezone=Europe%2FBerlin"

_LOGGER = logging.getLogger(__name__)

ICON_MAP = {
    "Food and Green Waste": "mdi:leaf",
    "Hard Waste": "mdi:sofa",
    "Recycling": "mdi:recycle",
}


class Source:
    def __init__(self):
        pass

    def fetch(self):
        session = requests.Session()
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        }
        session.headers.update(headers)

        response = session.get(URL)
        response.raise_for_status()

        wasteApiResult = response.json()
        _LOGGER.debug("Waste API result: %s", wasteApiResult)

        entries = []
        for record in wasteApiResult["records"]:
            waste_type = record["fields"]["type_col"]
            icon = ICON_MAP.get(waste_type)
            next_pickup_date = datetime.strptime(
                record["fields"]["jour_col"], "%Y-%m-%d"
            ).date()
            entries.append(
                Collection(date=next_pickup_date, t=waste_type, icon=icon)
            )

        return entries