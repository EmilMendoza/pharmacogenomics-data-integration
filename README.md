# Bioinformatics API Data Integration

A Python toolkit for retrieving, parsing, and integrating pharmacogenomic data from multiple biomedical databases using public APIs.

This project demonstrates how bioinformatics data from **ClinVar**, **PharmGKB**, and **DGIdb** can be collected, standardized, and exported into analysis-ready datasets for downstream analysis.

## Overview

Pharmacogenomic information is distributed across multiple databases, each using different data structures and formats. This project automates the retrieval and processing of these data sources by:

- Querying multiple public bioinformatics APIs
- Parsing JSON responses
- Converting API responses into structured Pandas DataFrames
- Exporting analysis-ready CSV files

The project demonstrates practical applications of Python for bioinformatics data integration and reproducible workflow development.

## Objectives

- Retrieve pharmacogenomic data from public APIs
- Parse JSON responses into structured tables
- Integrate drug, gene, and variant information
- Generate analysis-ready datasets
- Demonstrate modular Python programming for bioinformatics

## Data Sources

The project integrates data from:

- **ClinVar**
- **PharmGKB**
- **DGIdb**

## Technologies

### Programming

- Python

### Libraries

- requests
- pandas
- Biopython
- json

### Bioinformatics Resources

- ClinVar (NCBI Entrez)
- PharmGKB API
- DGIdb GraphQL API

## Repository Structure

```text
bioinformatics-api-data-integration/
│
├── README.md
├── LICENSE
├── requirements.txt
│
├── src/
│   ├── clinvar.py
│   ├── pharmgkb.py
│   ├── dgidb.py
│   └── main.py
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── data/
│   ├── raw/
│   └── processed/
│
└── output/
```


## Installation

Clone the repository

```bash
git clone https://github.com/EmilMendoza/bioinformatics-api-data-integration.git
cd bioinformatics-api-data-integration
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Usage

Run the complete workflow

```bash
python src/main.py
```

The workflow retrieves data from:

- ClinVar
- PharmGKB
- DGIdb

and exports CSV files to the `output/` directory.

---

## Output

The workflow generates:

- `clinvar_variants.csv`
- `pharmgkb_annotations.csv`
- `dgidb_interactions.csv`

---

## Skills Demonstrated

- Python programming
- REST API integration
- GraphQL API querying
- JSON parsing
- Pandas data manipulation
- Biomedical data integration
- Bioinformatics database querying
- Reproducible workflow development
- Modular software design

---

## Future Improvements

Potential extensions include:

- Additional pharmacogenomic databases
- Command-line interface (CLI)
- Automated data integration across APIs
- Variant annotation filtering
- Visualization dashboards
- Unit testing

---

## Repository Status

This repository was developed as part of graduate bioinformatics coursework and has been refactored into a modular Python project for portfolio purposes.

The original exploratory notebook is included in the `notebooks/` directory, while the reusable Python implementation is located in the `src/` directory.
