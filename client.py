# client.py

import requests
import pandas as pd
import pickle
from Pyfhel import Pyfhel

from hedfq.utils import encrypt, decrypt, serialise, deserialise, ENCODING

server = "http://localhost:5000/"

# check
print("get before dataset has been uploaded:")
r = requests.get(server+"get")
assert r.status_code == 400
print(r.status_code, r.content)

dataset = pd.read_csv("./client/snpp-2018-sample.csv").set_index(["AREA", "AGE GROUP", "SEX"])
records = len(dataset)

# encryption
client_he = Pyfhel()
client_he.contextGen(p=65537)
client_he.keyGen()

pk_file = "client-pubkey.pk"
ctx_file = "client-context.ctx"
client_he.savepublicKey(pk_file)
client_he.saveContext(ctx_file)

# encrypt and serialise
dataset = serialise(encrypt(client_he, dataset))

# register with server
print("upload encrypted dataset:")
data = {'pubkey': open(pk_file, 'rb'), 'context': open('client-context.ctx', 'rb'), "dataset": pickle.dumps(dataset)}
r = requests.post(server+'upload', files=data)
print(r.status_code, r.content)

# get back from server
print("check dataset ok:")
r = requests.get(server+"get")
assert r.status_code == 200
dataset = pickle.loads(r.content)
assert len(dataset) == records

# query
print("aggregate by area and decrypt:")
r = requests.get(server+"aggregate?on=AREA")
assert r.status_code == 200
agg_dataset = pickle.loads(r.content)
agg_dataset = decrypt(client_he, deserialise(client_he, agg_dataset))
print(agg_dataset)

print("aggregate by age and decrypt:")
r = requests.get(server+"aggregate?on=AGE GROUP")
assert r.status_code == 200
agg_dataset = pickle.loads(r.content)
agg_dataset = decrypt(client_he, deserialise(client_he, agg_dataset))
print(agg_dataset)

print("aggregate by sex and decrypt:")
r = requests.get(server+"aggregate?on=SEX")
assert r.status_code == 200
agg_dataset = pickle.loads(r.content)
agg_dataset = decrypt(client_he, deserialise(client_he, agg_dataset))
print(agg_dataset)

print("aggregate with invalid param:")
r = requests.get(server+"aggregate?on=INVALID")
assert r.status_code == 400
print(r.content)

# delete from server
print("delete encrypted data on server:")
r = requests.get(server+"delete")
assert r.status_code == 200

# check its gone
print("check encrypted data no longer on server:")
r = requests.get(server+"get")
assert r.status_code == 400
