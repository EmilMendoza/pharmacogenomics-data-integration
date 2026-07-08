"""
DGIdb API utilities.

This module retrieves drug-gene interaction data from DGIdb using
the DGIdb GraphQL API and converts the returned JSON into a structured
Pandas DataFrame.
"""

import json
import os

import pandas as pd
import requests


DGIDB_URL = "https://dgidb.org/api/graphql"


def download_dgidb_interactions(drug_name: str, output_file: str) -> dict:
    """
    Query DGIdb for drug-gene interactions and save the JSON response.
    """

    query = f"""
    {{
      drugs(names: ["{drug_name}"]) {{
        nodes {{
          interactions {{
            gene {{
              name
              conceptId
              longName
            }}
            interactionScore
            interactionTypes {{
              type
              directionality
            }}
            interactionAttributes {{
              name
              value
            }}
            publications {{
              pmid
            }}
            sources {{
              sourceDbName
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        DGIDB_URL,
        json={"query": query}
    )

    response.raise_for_status()

    data = response.json()

    output_dir = os.path.dirname(output_file)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_file, "w") as file:
        json.dump(data, file, indent=2)

    return data


def extract_interactions_to_dataframe(data: dict) -> pd.DataFrame:
    """
    Parse DGIdb drug-gene interaction JSON into a Pandas DataFrame.
    """

    drug_nodes = (
        data.get("data", {})
        .get("drugs", {})
        .get("nodes", [])
    )

    records = []

    for drug_index, drug in enumerate(drug_nodes):

        interactions = drug.get("interactions", [])

        for interaction in interactions:

            gene = interaction.get("gene", {})

            interaction_types = interaction.get(
                "interactionTypes", []
            )

            interaction_type_values = [
                item.get("type")
                for item in interaction_types
                if item.get("type")
            ]

            directionality_values = [
                item.get("directionality")
                for item in interaction_types
                if item.get("directionality")
            ]

            pmids = [
                publication.get("pmid")
                for publication in interaction.get("publications", [])
                if publication.get("pmid")
            ]

            sources = [
                source.get("sourceDbName")
                for source in interaction.get("sources", [])
                if source.get("sourceDbName")
            ]

            records.append({
                "drug_index": drug_index,
                "gene_name": gene.get("name"),
                "concept_id": gene.get("conceptId"),
                "gene_long_name": gene.get("longName"),
                "interaction_score": interaction.get("interactionScore"),
                "interaction_types": ", ".join(interaction_type_values),
                "directionality": ", ".join(directionality_values),
                "pmids": ", ".join(map(str, pmids)) if pmids else None,
                "sources": ", ".join(sources) if sources else None,
            })

    return pd.DataFrame(records)


def get_dgidb_interactions(
    drug_name: str,
    raw_output_file: str = "data/raw/dgidb_interactions.json"
) -> pd.DataFrame:
    """
    Complete DGIdb workflow:
    download drug-gene interactions and return a parsed DataFrame.
    """

    data = download_dgidb_interactions(
        drug_name=drug_name,
        output_file=raw_output_file
    )

    df = extract_interactions_to_dataframe(data)

    return df


if __name__ == "__main__":

    dgidb_df = get_dgidb_interactions(
        drug_name="ACE INHIBITOR"
    )

    print(dgidb_df.head())

    os.makedirs("output", exist_ok=True)

    dgidb_df.to_csv(
        "output/dgidb_interactions.csv",
        index=False
    )
