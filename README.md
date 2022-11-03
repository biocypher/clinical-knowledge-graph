# CKG-BioCypher migration repository

This code serves as an adapter to the [Clinical Knowledge Graph](https://doi.org/10.1038/s41587-021-01145-6). Data is processed from the CKG Neo4j database dump (available [here](https://data.mendeley.com/datasets/mrcf7f4tc2/3)) into BioCypher-compatible format using the adapter class and the configuration in `config/schema_config.yaml`.

`adapter.py` represents the adapter class, the import is performed using `script.py`. More information on BioCypher and its use can be found here: https://saezlab.github.io/BioCypher/
