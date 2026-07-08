import os

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

os.makedirs("output", exist_ok=True)

if __name__ == "__main__":

    download_clinvar(
        query="NC_000003.11",
        output_file="data/raw/clinvar.json"
    )

    df = extract_clinvar_variants(
        "data/raw/clinvar.json"
    )

    print(df.head())

    os.makedirs("output", exist_ok=True)

    df.to_csv(
        "output/clinvar_variants.csv",
        index=False
    )
