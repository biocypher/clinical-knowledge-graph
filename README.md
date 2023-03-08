# CKG-BioCypher migration repository

This code serves as an adapter to the [Clinical Knowledge
Graph](https://doi.org/10.1038/s41587-021-01145-6). Data is processed from the
CKG Neo4j database dump (available
[here](https://data.mendeley.com/datasets/mrcf7f4tc2/3)) into
BioCypher-compatible format using the adapter class and the configuration files
in `config/`. For more information on BioCypher, please visit 
https://biocypher.org.

## Installation
The project uses [Poetry](https://python-poetry.org). You can install it like this:

``` 
git clone https://github.com/saezlab/CKG-BioCypher.git 
cd CKG-BioCypher
poetry install 
```

Poetry will create a virtual environment according to your configuration (either
centrally or in the project folder). You can activate it by running `poetry
shell` inside the project directory.

## Projects
Three concepts are represented in this repository:
- a full import of the CKG Neo4j dump file into BioCypher-compatible format
- a subsetting procedure to demonstrate the simplicity of subsetting a KG
- a subset used in the input of the Bioteque embedding pipeline to demonstrate
    a use case for the flexible subsetting of existing BioCypher adapters

### Full import
The full import database schema is configured in
`config/full_schema_config.yaml`. The adapter (`ckgb/adapter.py`) uses this
schema to stream data from the CKG dump in a running Neo4j instance into the
BioCypher driver. This is orchestrated by the import script at
`scripts/full_ckg_script.py`. The script can be run like this:

``` poetry run python scripts/full_ckg_script.py ```

The script will create a new database in BioCypher format in the `biocypher-out`
directory, including a shell script to generate a Neo4j instance from the files
using the neo4j-admin tool.

### Subsetting
The subsetting procedure is configured in `config/subset_schema_config.yaml`. It
is a simplified version of the full import schema, with only a subset of the
nodes and edges. The adapter (`ckgb/adapter.py`) uses this schema to stream data
from the CKG dump in a running Neo4j instance into the BioCypher driver. This is
orchestrated by the import script at `scripts/subset_ckg_script.py`. The script
can be run like this:

``` poetry run python scripts/subset_ckg_script.py ```

The script will create a new database in BioCypher format in the `biocypher-out`
directory, including a shell script to generate a Neo4j instance from the files
using the neo4j-admin tool.

### Bioteque embeddings
The Bioteque subsetting procedure is configured in
`config/embedding_schema_config.yaml`. It is, like the subsetting procedure, a
simplified version of the full import schema, orchestrated by the import script
at `scripts/embedding_ckg_script.py`. The script can be run like this:

``` poetry run python scripts/embedding_ckg_script.py ```

In addition, after the instance has been created from the generated files, the
script at `other/create_list_bqe.py` can be used to create input files for the
Bioteque pipeline (https://bioteque.irbbarcelona.org). In this way, flexible
embeddings can be generated from BioCypher adapters with minimal effort. For
another example, check out the adapter for the Open Targets dataset at
https://github.com/saezlab/OTAR-BioCypher.
