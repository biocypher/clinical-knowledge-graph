import sys
sys.path.append("")  # vscode hack, may not be necessary

from ckgb.adapter import CKGAdapter
from biocypher import BioCypher

output_directory = "biocypher-out/embedding"

# start biocypher
bc = BioCypher(
    biocypher_config_path="config/biocypher_config_embedding.yaml",
    output_directory=output_directory,
)

# create CKG adapter
adapter = CKGAdapter(
    limit_import_count=100, # for testing; remove or set to 0 for full import
    biocypher_driver=bc,
    dirname=output_directory,
    node_file="data/embedding_nodes.csv",
    edge_file="data/embedding_relationships.csv",
) 

# perform import
adapter.write_nodes()
adapter.write_edges()

# convenience and import stats
bc.write_import_call()
bc.summary()
