import sys
sys.path.append("")

from ckgb.adapter import CKGAdapter
from biocypher import BioCypher

# start biocypher
bc = BioCypher(
    biocypher_config_path="config/biocypher_config_full.yaml",
)

# create CKG adapter
adapter = CKGAdapter(
    limit_import_count=100, # for testing; remove or set to 0 for full import
    biocypher_driver=bc,
    # dirname=output_directory,
) 

# perform import
# TODO find a way to pass nodes and edges to the driver instead of the driver to
# the adapter
adapter.write_nodes()
adapter.write_edges()

# convenience and import stats
bc.write_import_call()
bc.log_missing_bl_types()
bc.log_duplicates()
bc.show_ontology_structure()
