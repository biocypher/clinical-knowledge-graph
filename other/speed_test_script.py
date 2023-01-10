import os
import time
import itertools
from ckgb.speed_test import SpeedTest

st = SpeedTest()

"""
The clear winner appears to be a batch size of 100000 (1e5).
"""

# time write_edges function across a range of id_batch_sizes
batch_sizes = itertools.chain(
    range(int(1e4), int(9e4), int(1e4)), range(int(1e5), int(2e6), int(1e5))
)

path = "data/times.csv"
if not os.path.exists(path):
    with open(path, "w") as f:
        f.write("id_batch_size,time\n")
    done_batches = []
else:
    # read first column of times.csv
    with open(path, "r") as f:
        # skip header
        next(f)
        done_batches = [float(line.split(",")[0]) for line in f.readlines()]

for id_batch_size in batch_sizes:
    if id_batch_size in done_batches:
        continue

    # record start time
    start = time.time()

    # run write_edges function 3 times
    st.write_edges(id_batch_size)

    # calculate time and add to dict
    time_ = time.time() - start

    # delete files in speed_test directory
    for file in os.listdir("speed_test"):
        os.remove(os.path.join("speed_test", file))

    # append single time to csv
    with open("data/times.csv", "a") as f:
        f.write(f"{id_batch_size},{time_}\n")
