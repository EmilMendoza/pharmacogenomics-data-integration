
"""
PharmGKB API utilities.

This module retrieves variant annotation data from PharmGKB and converts
the returned JSON into a structured Pandas DataFrame.
"""

import json
import os
from typing import Optional

import pandas as pd
import requests


BASE_URL = (
    "https://api.pharmgkb.org/v1/data/variantAnnotation"
)


def download_pharmgkb_annotations(
    pharmgkb_id: str,
    output_file: str,
) -> dict:
    """
    Retrieve PharmGKB variant annotations for a drug or chemical ID.

    Parameters
    ----------
    pharmgkb_id : str
        PharmGKB accession ID for a drug or chemical.
        Example: PA164712308 for ACE inhibitors, plain.

    output_file : str
        Path where the raw JSON response should be saved.

    Returns
    -------
    dict
        JSON response from the PharmGKB API.
    """

    params = {
        "relatedChemicals.accessionId": pharmgkb_id
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    output_dir = os.path.dirname(output_file)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w") as file:
        json.dump(data, file, indent=2)

    return data


def parse_pharmgkb_annotations(
    json_file: str,
    selected_columns: Optional[list] = None,
) -> pd.DataFrame:
    """
    Parse PharmGKB variant annotation JSON into a DataFrame.

    Parameters
    ----------
    json_file : str
        Path to the PharmGKB JSON file.

    selected_columns : list, optional
        Columns to retain from the PharmGKB API response.

    Returns
    -------
    pandas.DataFrame
        Parsed PharmGKB variant annotation table.
    """

    with open(json_file, "r") as file:
        data = json.load(file)

    records = data.get("data", [])

    df = pd.DataFrame.from_records(records)

    if selected_columns is None:
        selected_columns = [
            "description",
            "isAssociated",
            "score",
            "sentence",
            "sequenceLocation",
        ]

    available_columns = [
        column for column in selected_columns
        if column in df.columns
    ]

    return df[available_columns]


def get_pharmgkb_annotations(
    pharmgkb_id: str,
    raw_output_file: str = "data/raw/pharmgkb_annotations.json",
) -> pd.DataFrame:
    """
    Complete PharmGKB workflow:
    download variant annotations and return a parsed DataFrame.
    """

    download_pharmgkb_annotations(
        pharmgkb_id=pharmgkb_id,
        output_file=raw_output_file,
    )

    df = parse_pharmgkb_annotations(raw_output_file)

    return df


if __name__ == "__main__":

    pharmgkb_df = get_pharmgkb_annotations(
        pharmgkb_id="PA164712308"
    )

    print(pharmgkb_df.head())

    os.makedirs("output", exist_ok=True)

    pharmgkb_df.to_csv(
        "output/pharmgkb_annotations.csv",
        index=False
    )
