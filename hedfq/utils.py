
from base64 import b64encode, b64decode
from Pyfhel import Pyfhel, PyCtxt

ENCODING='utf-8' #'ISO-8859-1' "cp1252" #'latin-1'

def encrypt_serialise(he, df):

  for y in df.columns:
    df[y] = df[y].apply(he.encryptFrac)

  # print("encrypted, unmodified")
  # print(df.head())

  for y in df.columns:
    # base64 encoded
    df[y] = df[y].apply(lambda e: b64encode(e.to_bytes()).decode(ENCODING)) #.decode(encoding=ENCODING))
    # native encoding segfaults
    # df[y] = df[y].apply(lambda e: e.to_bytes().decode(encoding=ENCODING))

  return df

def deserialise(he, df):

  def deser(b):
    c = PyCtxt(pyfhel=he)
    # base64 encoding
    c.from_bytes(b64decode(b), float)
    # native encoding segfaults
    #c.from_bytes(b.encode(encoding=ENCODING), float)
    return c

  for y in df.columns:
    df[y] = df[y].apply(deser) #.decode(encoding=ENCODING))
  return df

