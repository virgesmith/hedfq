
import pandas as pd
from Pyfhel import Pyfhel, PyPtxt, PyCtxt
from base64 import b64encode, b64decode
from time import time

from hedfq.utils import encrypt, decrypt, serialise, deserialise, ENCODING

client_he = Pyfhel()           # Creating empty Pyfclient_hel object
client_he.contextGen(p=65537)  # Generating context. Tclient_he p defines tclient_he plaintext modulo.
client_he.keyGen()             # Key Generation: generates a pair of public/secret keys
print(client_he)

df = pd.read_csv("./client/snpp-2018-sample.csv").set_index(["AREA", "AGE GROUP", "SEX"])
print("unencrypted, unmodified")
print(len(df))
print(df.head())

print("unencrypted, aggregated")
print(df.groupby(level=["AREA", "SEX"]).sum())


start = time()
df = serialise(encrypt(client_he, df))
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
df2 = pd.read_csv("./client/snpp-2018-sample-encrypted.csv", encoding=ENCODING).set_index(["AREA", "AGE GROUP", "SEX"])
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
dfagg = df2.groupby(level=["AREA", "SEX"]).sum()
elapsed = time() - start
print("encrypted aggregation took %fs" % elapsed)


start = time()
# for y in dfagg.columns:
#   dfagg[y] = dfagg[y].apply(client_he.decryptFrac)
dfagg = decrypt(client_he, dfagg)
elapsed = time() - start
print("decrypting aggregation took %fs" % elapsed)
print("copied, decrypted, deserialised, aggregrated")
print(dfagg)


# print("copied, decrypted, deserialised, modified")
# for y in df2.columns:
#   df2[y] = df2[y].apply(client_he.decryptFrac)

# print(df2.head())
