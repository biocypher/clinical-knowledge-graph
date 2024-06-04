# CKG-BioCypher migration repository

This code serves as an adapter to the [Clinical Knowledge
Graph](https://doi.org/10.1038/s41587-021-01145-6). Data is processed from the
CKG Neo4j database dump (available
[here](https://data.mendeley.com/datasets/mrcf7f4tc2/3)) into
BioCypher-compatible format using the adapter class and the configuration files
in `config/`. For more information on BioCypher, please visit 
https://biocypher.org.

## Setup and Installation

### Clone and setup the project

The project uses [Poetry](https://python-poetry.org). You can install it like 
this:

``` 
git clone https://github.com/saezlab/CKG-BioCypher.git 
cd CKG-BioCypher
poetry install 
```

Poetry will create a virtual environment according to your configuration (either
centrally or in the project folder). You can activate it by running `poetry
shell` inside the project directory.

### Run the CKG

For getting the data from the CKG, an instance of the CKG needs to be running in
Neo4j. For setting this up, please refer to the [CKG
docs](https://ckg.readthedocs.io/en/latest/ckg_builder/graphdb-builder.html#building-ckg-s-graph-database-from-a-dump-file).

Alternatively, you can use the pre-made CKG Neo4j database dump instance setup
configuration provided in the `ckg_dump` directory by following the README in
it.

### Configuration

Now the credentials for the CKG Neo4j instance need to be configured within the
`ckgb/adapter.py`.


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
orchestrated by the import script at `scripts/subset_ckg_script.py`.

To create a subset, configure the subset schema in
`config/subset_schema_config.yaml`, and insert the used node and relationship
names of the subset in the `data/subset_nodes.csv` and
`data/subset_relationships.csv`. To check which nodes and relationships exist
in the CKG you can have a look at `data/all_nodes.csv` and
`data/all_granular_relationships.csv`.

If you would like to insert relationship properties, adapt the `_write_edges`
method in the adapter and specify how the properties of each relationship type
should be handeled.

Finally the subsetting procedure can be run with `poetry run python
scripts/subset_ckg_script.py`. The script will create a new database in
BioCypher format in the `biocypher-out` directory, including a shell script to
generate a Neo4j instance from the files using the neo4j-admin tool.

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
https://github.com/biocypher/open-targets.
