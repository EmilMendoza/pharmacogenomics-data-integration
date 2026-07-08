"""
ClinVar API utilities.
"""

import json
import os

import pandas as pd
from Bio import Entrez


Entrez.email = "ian@gimik.com"


def download_clinvar(query, output_file, max_results=10):
    """
    Search ClinVar and save the returned JSON summary.
    """

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    handle = Entrez.esearch(
        db="clinvar",
        term=query,
        sort="relevance",
        retmax=max_results,
        retmode="xml"
    )

    results = Entrez.read(handle)
    handle.close()

    id_list = results["IdList"]

    handle = Entrez.esummary(
        db="clinvar",
        id=id_list,
        retmode="json"
    )

    with open(output_file, "wb") as output:
        output.write(handle.read())

    handle.close()


def extract_clinvar_variants(json_path):
    """
    Convert ClinVar JSON results into a Pandas DataFrame.
    """

    with open(json_path, "r") as file:
        data = json.load(file)

    variants = data["result"]
    uids = variants["uids"]

    records = []

    for uid in uids:
        variant = variants[uid]

        gene_symbol = (
            variant["genes"][0]["symbol"]
            if variant.get("genes")
            else ""
        )

        trait_set = (
            variant.get("germline_classification", {})
            .get("trait_set", [])
        )

        trait_name = (
            trait_set[0].get("trait_name", "")
            if trait_set
            else ""
        )

        records.append({
            "uid": uid,
            "accession": variant.get("accession"),
            "title": variant.get("title"),
            "gene": gene_symbol,
            "protein_change": variant.get("protein_change"),
            "variant_type": variant.get("obj_type"),
            "molecular_consequence": ", ".join(
                variant.get("molecular_consequence_list", [])
            ),
            "classification": variant.get(
                "germline_classification", {}
            ).get("description", ""),
            "trait": trait_name
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    download_clinvar(
        query="NC_000003.11",
        output_file="data/raw/clinvar.json"
    )

    df = extract_clinvar_variants("data/raw/clinvar.json")
    print(df.head())

    os.makedirs("output", exist_ok=True)

    df.to_csv(
        "output/clinvar_variants.csv",
        index=False
    )
