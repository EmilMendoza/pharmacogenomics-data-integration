
"""
Main workflow for bioinformatics API data integration.

This script retrieves pharmacogenomic and drug-gene interaction data
from ClinVar, PharmGKB, and DGIdb, then exports the results as CSV files.
"""

import os

from clinvar import download_clinvar, extract_clinvar_variants
from pharmgkb import get_pharmgkb_annotations
from dgidb import get_dgidb_interactions


def main():
    """
    Run the full API data integration workflow.
    """

    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    print("Retrieving ClinVar data...")
    download_clinvar(
        query="NC_000003.11",
        output_file="data/raw/clinvar.json"
    )

    clinvar_df = extract_clinvar_variants(
        "data/raw/clinvar.json"
    )

    clinvar_df.to_csv(
        "output/clinvar_variants.csv",
        index=False
    )

    print("Retrieving PharmGKB data...")
    pharmgkb_df = get_pharmgkb_annotations(
        pharmgkb_id="PA164712308"
    )

    pharmgkb_df.to_csv(
        "output/pharmgkb_annotations.csv",
        index=False
    )

    print("Retrieving DGIdb data...")
    dgidb_df = get_dgidb_interactions(
        drug_name="ACE INHIBITOR"
    )

    dgidb_df.to_csv(
        "output/dgidb_interactions.csv",
        index=False
    )

    print("Workflow complete.")
    print("Output files saved to the output/ directory.")


if __name__ == "__main__":
    main()
