# client.py

import requests
import pandas as pd
import pickle
from Pyfhel import Pyfhel

from hedfq.utils import encrypt_serialise, deserialise, ENCODING

server = "http://localhost:5000/"

# check
r = requests.get(server+"get")
assert r.status_code == 400
print(r.status_code, r.content)

dataset = pd.read_csv("./client/snpp-2018-sample.csv").set_index(["CODE", "AREA", "AGE GROUP", "SEX"])

# encryption
client_he = Pyfhel()
client_he.contextGen(p=65537)
client_he.keyGen()

pk_file = "client-pubkey.pk"
ctx_file = "client-context.ctx"
client_he.savepublicKey(pk_file)
client_he.saveContext(ctx_file)

# encrypt and serialise
dataset = encrypt_serialise(client_he, dataset)

# register with server
data = {'pubkey': open(pk_file, 'rb'), 'context': open('client-context.ctx', 'rb'), "dataset": pickle.dumps(dataset)}
r = requests.post(server+'upload', files=data)
print(r.status_code, r.content)

# get back from server
r = requests.get(server+"get")
assert(r.status_code == 200)
dataset = pickle.loads(r.content)

print(dataset.head())
