import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)

class HallenbadData:
    def __init__(self):
        self.name: Optional[str] = None
        self.water_temp: Optional[str] = None
        self.status: Optional[str] = None
        self.last_updated: Optional[str] = None

    def get_temperature(self) -> int:
        match = re.match(r'^(\d+)', self.water_temp)
        if match is not None:
            return int(match.group(1))

    def as_csv(self) -> str:
        return f"{self.name};{self.get_temperature()};{self.status};{self.last_updated}"

    def __repr__(self):
        return f"{{ {self.name}, {self.water_temp}, {self.status}, {self.last_updated} }}"


def extract_hallenbad_data(html: str) -> List[HallenbadData]:
    soup = BeautifulSoup(html, 'html.parser')
    hallenbad_table = soup.find(id="baederinfossummary")

    data = []

    table_body = hallenbad_table.find("tbody")
    for row in table_body.find_all("tr"):
        # Extract the data
        columns = row.find_all("td")

        hallenbad_data = HallenbadData()
        hallenbad_data.name = columns[0].a.string
        hallenbad_data.water_temp = columns[1].string
        hallenbad_data.status = columns[2].string
        hallenbad_data.last_updated = columns[3].string

        data.append(hallenbad_data)

    return data


def store_hallenbad_data(data: List[HallenbadData], folder: Path) -> None:
    """
    Stores the Hallenbad data to a file per hallenbad
    """

    for hallenbad_data in data:
        file_path = folder / (hallenbad_data.name + ".csv")

        with open(file_path, 'a') as f:
            f.write(datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + ";" + hallenbad_data.as_csv() + "\n")
