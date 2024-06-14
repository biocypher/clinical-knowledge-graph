# Building CKG’s Graph Database from a Dump File

## Step 1: Download CKG Neo4j database dump 

For additional info about the dump, please read the [CKG
docs](https://ckg.readthedocs.io/en/latest/ckg_builder/graphdb-builder.html?highlight=dump#more-on-the-dump-file).
The dump of the CKG neo4j database v4.2.3 is available
[here](https://data.mendeley.com/datasets/mrcf7f4tc2/3); another set of links is
provided in [the
docs](https://ckg.readthedocs.io/en/latest/ckg_builder/graphdb-builder.html?highlight=dump#more-on-the-dump-file)

*Option A*: download using Python (in this directory):

```
poetry run python download.py
```

*Option B*: download manually and verify with md5sum:

```
wget -P ./neo4j/backups/graph.db/ "https://datashare.biochem.mpg.de/s/kCW7uKZYTfN8mwg/download" -O ./ckg_latest_4.2.3.dump
wget -P ./neo4j/backups/graph.db/ "https://datashare.biochem.mpg.de/s/fP6MKhLRfceWwxC/download" -O ./data.zip
wget -P ./neo4j/plugins/ https://github.com/neo4j/graph-data-science/releases/download/1.5.1/neo4j-graph-data-science-1.5.1.jar
wget -P ./neo4j/plugins/ https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.2.0.4/apoc-4.2.0.4-all.jar
md5sum -c ./ckg_latest.md5
```

## Step 2: Initilize Neo4j with the dump:

Initialization is automated and depends on presence of the above mentioned files
in `./neo4j/backups/graph.db/`. To start the service, run in this directory
(`ckg_dump`):

```
docker compose up -d
```

After initialization, the file `./neo4j/data/neo4j-import-done.flag` will be
created, denoting successful import. To reset the state of the graph to the
dumped state, remove the contents of the `./neo4j/data/` folder:

``` 
docker compose down 
rm -rf ./neo4j/data/*
```
