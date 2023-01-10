import sys
sys.path.append("")  # vscode hack, may not be necessary

from ckgb.adapter import CKGAdapter
import biocypher

# optionally set output directory (e.g. for resuming)
# NOTE: resume functionality is a simple text based check; delete output folder
# to reset
output_directory = "biocypher-out/subset"

# start biocypher
driver = biocypher.Driver(
    db_name="subset",
    clear_cache=False,
    user_schema_config_path="config/subset_schema_config.yaml",
    delimiter="¦",
    output_directory=output_directory,
)
driver.start_ontology_adapter() # for resume functionality

# create CKG adapter
adapter = CKGAdapter(
    limit_import_count=100, # for testing; remove or set to 0 for full import
    biocypher_driver=driver,
    dirname=output_directory,
    resume=True,
    node_file="data/subset_nodes.csv",
    edge_file="data/subset_relationships.csv",
) 

# perform import
adapter.write_nodes()
adapter.write_edges()

# convenience and import stats
driver.write_import_call()
driver.log_missing_bl_types()
driver.log_duplicates()
driver.show_ontology_structure()
