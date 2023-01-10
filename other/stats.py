import pandas as pd
import json

# read in the data
with open("apoc.meta.stats.csv") as f:
    stats = pd.read_csv(f)

stats.columns

# extract labels
labels = stats["labels"]

# parse json from labels object
labels_json = json.loads(labels[0])

# pandas dataframe from json
labels_df = pd.DataFrame.from_dict(labels_json, orient="index")

# write to csv
labels_df.to_csv("ckg_labels.csv")

# extract rel types
rel_types = stats["relTypes"]

# parse json from rel types object
rel_types_json = json.loads(rel_types[0])

# pandas dataframe from json
rel_types_df = pd.DataFrame.from_dict(rel_types_json, orient="index")

# write to csv
rel_types_df.to_csv("ckg_rel_types.csv")
