from adapter import CKGAdapter
import biocypher

# start biocypher
driver = biocypher.Driver(
    offline=True,  
    strict_mode=True,
    db_name="large",
    clear_cache=False,
    user_schema_config_path="config/schema_config.yaml",
    delimiter="¦",
)

# create CKG adapter
adapter = CKGAdapter(
    limit_import_count=100, # limit_import_count is for testing; remove or set to 0 for full import
    biocypher_driver=driver
) 

# perform import
# TODO find a way to pass nodes and edges to the driver instead of the driver to the adapter
adapter.write_nodes()
adapter.write_edges()

# convenience and import stats
driver.write_import_call()
driver.log_missing_bl_types()
driver.log_duplicates()
driver.show_ontology_structure()
