"""
Script to create a dataset to be used in the Bioteque embedding pipeline. 
Author: Elena Pareja-Lorente
"""
import biocypher
import pandas as pd

def get_labels():
    with open("data/embedding_relationships.txt", "r") as f:
        node_labels = f.read().splitlines()

    node_labels = node_labels[1:]
    node_labels = [label.split(",") for label in node_labels]
    return node_labels

d = biocypher.Driver(
    db_name = "subset", 
    db_user = "neo4j", 
    db_passwd = "neo4j", 
    offline = False)

node_labels = get_labels()

for src, rel, tar in node_labels: 
    print(src, rel, tar)
    ids = d.query(f"MATCH p=(n:{src})-[r:{rel}]->(m:{tar}) RETURN n.id, m.id")
    pd.DataFrame(ids[0]).to_csv(f"{src}_{rel}_{tar}.tsv", sep = "\t", index=False)