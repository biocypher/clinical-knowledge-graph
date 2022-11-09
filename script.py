from adapter import BioCypherAdapter

adapter = BioCypherAdapter(
    db_name="large", 
    limit_import_count=100,  # limit_import_count is for testing; remove or set to 0 for full import
    clear_cache=False,
) 

adapter.write_to_csv_for_admin_import()
