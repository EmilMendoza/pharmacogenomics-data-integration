# Bioinformatics API Data Integration

Python toolkit for retrieving, parsing, and integrating pharmacogenomic data from multiple biomedical databases.

## Overview

This project demonstrates how to retrieve and integrate pharmacogenomic information from multiple public bioinformatics resources using Python.

Data are collected from:

- ClinVar
- PharmGKB
- DGIdb

The project retrieves API responses, parses JSON data, and converts the results into structured Pandas DataFrames for downstream analysis.

## Objectives

- Query multiple biomedical APIs
- Parse JSON responses
- Standardize heterogeneous biological data
- Integrate pharmacogenomic annotations
- Export analysis-ready datasets

## Technologies

### Programming

- Python

### Libraries

- requests
- pandas
- json
- Biopython

### Databases

- ClinVar
- PharmGKB
- DGIdb

## Repository Structure

```text
src/            Python source code
data/           Raw and processed data
notebooks/      Exploratory notebook
output/         Exported datasets
```

## Skills Demonstrated

- REST API development
- JSON parsing
- Biomedical data integration
- Pandas data manipulation
- Bioinformatics database querying
- Reproducible Python workflows
