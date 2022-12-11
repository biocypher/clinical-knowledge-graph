from adapter import CKGAdapter
import biocypher

# output_directory = "biocypher-out/strict_complete"

# start biocypher
driver = biocypher.Driver(
    db_name="strict",
    clear_cache=False,
    user_schema_config_path="config/schema_config.yaml",
    delimiter="¦",
    # output_directory=output_directory,
)
driver.start_ontology_adapter() # for resume functionality

# create CKG adapter
adapter = CKGAdapter(
    limit_import_count=100, # for testing; remove or set to 0 for full import
    biocypher_driver=driver,
    # dirname=output_directory,
    # resume=True,
) 

# perform import
# TODO find a way to pass nodes and edges to the driver instead of the driver to
# the adapter
adapter.write_nodes()
adapter.write_edges()

# convenience and import stats
driver.write_import_call()
driver.log_missing_bl_types()
driver.log_duplicates()
driver.show_ontology_structure()
