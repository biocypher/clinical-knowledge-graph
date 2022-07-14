import neo4j_utils as nu

driver = nu.Driver(
    db_name="neo4j",
    db_uri="bolt://localhost:7687",
    db_user="neo4j",
    db_passwd="your_password_here",
    multi_db=False,
)

# remove Experiment nodes with UO ids (likely bug)
# cross-reference with unit nodes 0 and 2
# 2 has no rels, 0 has 4 HAS_PARENT rels
driver.query("MATCH (n:Experiment) WHERE n.id = 'UO:0000002' DELETE n")

driver.query(
    "MATCH (n:Experiment)--(m) WHERE n.id = 'UO:0000000' "
    "WITH n, m "
    "MATCH (u:Units {id: 'UO:0000000'}) "
    "CREATE (m)-[:HAS_PARENT]->(u) "
    "DETACH DELETE n "
)
