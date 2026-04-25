import json, msgpack, os
with open("helpers/bank.json", "r") as f:
    data = json.load(f)
with open("helpers/bank.msgpack", "wb") as f:
    msgpack.pack(data, f, use_bin_type=True)
print("done")