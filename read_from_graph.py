import neo4j_utils as nu
import pandas as pd
import json


# driver = nu.Driver(
#     db_name="neo4j",
#     db_uri="bolt://localhost:7687",
#     db_user="neo4j",
#     db_passwd="your_password_here",
#     multi_db=False,
# )

# res, sum = driver.query(
#     "MATCH (n:Known_variant)-[:VARIANT_IS_CLINICALLY_RELEVANT]-(m) RETURN n, m LIMIT 1"
# )

# res, sum = driver.query("MATCH (n:Pathway) RETURN n.id")

# print(res)

# ### get all node labels
# res, sum = driver.query("MATCH (n) RETURN DISTINCT labels(n)")

# # write res to csv
# with open("node_labels.csv", "w") as f:
#     for r in res:
#         name = r["labels(n)"][0]
#         f.write(str(name) + "\n")

# ### get all relationship combinations
# res, sum = driver.query(
#     "MATCH (n)-[r]->(m) RETURN DISTINCT labels(n), type(r), labels(m)"
# )

# # write res to file
# with open("granular_relationships.txt", "w") as f:
#     f.write("Source,Relationship,Target\n")
#     for r in res:
#         src = r["labels(n)"]
#         # concatenate src labels if more than 1
#         if len(src) > 1:
#             src = ";".join(src)
#         else:
#             src = src[0]
#         tar = r["labels(m)"]
#         # concatenate tar labels if more than 1
#         if len(tar) > 1:
#             tar = ";".join(tar)
#         else:
#             tar = tar[0]
#         typ = r["type(r)"]
#         f.write(f"{src},{typ},{tar}\n")


# ### get relationship type summary
# res, sum = driver.query(
#     "MATCH ()-[relationship]->() "
#     "RETURN TYPE(relationship) AS type, COUNT(relationship) AS amount "
#     "ORDER BY amount DESC"
# )

# # write res to file
# with open("relationship_types.txt", "w") as f:
#     for r in res:
#         f.write(str(r) + "\n")

# # read file back to dict
# d = {}
# with open("relationship_types.txt", "r") as f:
#     # read csv file
#     for line in f:
#         line = line.strip('\n')
#         line = line.replace("'", '"')
#         l = json.loads(line)
#         typ = l["type"]
#         amount = l["amount"]
#         # add typ and amount to d
#         d[typ] = amount

# # convert dict to pandas dataframe
# df = pd.DataFrame.from_dict(d, orient='index')
# df.columns = ['amount']

# # write df to csv file
# df.to_csv("relationship_types.csv")

# ### prepend in file
# # prepend "somatic:" to each line in file "/Users/slobentanzer/GitHub/CKG/biocypher-out/202207112047/Somatic.SequenceVariant-part000.csv"
# with open(
#     "/Users/slobentanzer/GitHub/CKG/biocypher-out/202207112047/Somatic.SequenceVariant-part000 copy.csv",
#     "r",
# ) as f:
#     with open(
#         "/Users/slobentanzer/GitHub/CKG/biocypher-out/202207112047/Somatic.SequenceVariant-part000.csv",
#         "w",
#     ) as f2:
#         for line in f:
#             f2.write("somatic:" + line)
