
import pandas as pd
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
from base64 import b64encode, b64decode
from time import time

from hedfq.utils import encrypt_serialise, deserialise, ENCODING


# def read_unencrypted():

#   # df = pd.read_csv("../client/england_snpp_2018.csv").set_index(["CODE", "AREA", "AGE GROUP", "SEX"])
#   # # take a subset otherwise encryption will take forever and encrypted dataset will be enormous
#   # df = df.loc[["E06000001", "E06000002", "E06000003", "E06000005"]][["2018", "2019", "2020", "2021", "2022"]]
#   # # ensure consistent types
#   # #df["2018"] = df["2018"].astype(float)
#   # df.to_csv("snpp_2018_sample.csv")

#   df = pd.read_csv("./client/snpp-2018-sample.csv").set_index(["CODE", "AREA", "AGE GROUP", "SEX"])
#   return df

client_he = Pyfhel()           # Creating empty Pyfclient_hel object
client_he.contextGen(p=65537)  # Generating context. Tclient_he p defines tclient_he plaintext modulo.
client_he.keyGen()             # Key Generation: generates a pair of public/secret keys
print(client_he)

df = pd.read_csv("./client/snpp-2018-sample.csv").set_index(["CODE", "AREA", "AGE GROUP", "SEX"])
print("unencrypted, unmodified")
print(len(df))
print(df.head())

print("unencrypted, aggregated")
print(df.groupby(level=["CODE", "AREA", "SEX"]).sum())


start = time()
df = encrypt_serialise(client_he, df)
elapsed = time() - start
print("encryption took %fs" % elapsed)
print("encrypted, serialised, unmodified")
print(df.head())

pk_file = "client-pubkey.pk"
ctx_file = "client-context.ctx"
client_he.savepublicKey(pk_file)
client_he.saveContext(ctx_file)

# serialise to file
df.to_csv("./client/snpp-2018-sample-encrypted.csv", encoding=ENCODING)

# delete original data
df = None

# server only has public key
server_he = Pyfhel()
server_he.restoreContext(ctx_file)
server_he.restorepublicKey(pk_file)

# load from file
df2 = pd.read_csv("./client/snpp-2018-sample-encrypted.csv", encoding=ENCODING).set_index(["CODE", "AREA", "AGE GROUP", "SEX"])
#df2 = df
#assert df2.equals(df)
print("copied, encrypted, serialised, unmodified")
print(len(df2))
print(df2.head())

df2 = deserialise(server_he, df2)
print("copied, encrypted, deserialised, unmodified")
print(df2.head())

#x = df2["2018"][0]
#df2["2018"][0] = x + delta # + x

start = time()
dfagg = df2.groupby(level=["CODE", "AREA", "SEX"]).sum()
elapsed = time() - start
print("encrypted aggregation took %fs" % elapsed)


start = time()
for y in dfagg.columns:
  dfagg[y] = dfagg[y].apply(client_he.decryptFrac)
elapsed = time() - start
print("decrypting aggregation took %fs" % elapsed)
print("copied, decrypted, deserialised, aggregrated")
print(dfagg)


# print("copied, decrypted, deserialised, modified")
# for y in df2.columns:
#   df2[y] = df2[y].apply(client_he.decryptFrac)

# print(df2.head())
