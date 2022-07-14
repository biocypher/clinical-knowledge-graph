from adapter import BioCypherAdapter

adapter = BioCypherAdapter(db_name="small")

# adapter.write_nodes()
# adapter.write_edges()
# adapter.bcy.write_import_call()

adapter.write_to_csv_for_admin_import()
