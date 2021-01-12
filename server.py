# encrypted server - stores, and operates on, encrypted data
# despite not being able to decrypt it


from flask import Flask, request
import pandas as pd
from Pyfhel import Pyfhel, PyCtxt
from base64 import b64encode, b64decode
import pickle

from hedfq.utils import serialise, deserialise #, ENCODING


app = Flask(__name__)

server_he = None
dataset = None

@app.route("/upload", methods=["POST"])
def upload():

  files = request.files#.getlist()
  if "pubkey" not in request.files.keys():
    return "no pubkey", 400
  if "context" not in request.files.keys():
    return "no context", 400
  if "dataset" not in request.files.keys():
    return "no dataset", 400

  global dataset
  global server_he

  # clunky but pyfhel doesnt support loading from anything but a file
  request.files["pubkey"].save("server/client-pubkey.pk")
  request.files["context"].save("server/client-context.pk")

  server_he = Pyfhel()
  # NOTE: these functions segfault if given the wrong data or not done in this order
  server_he.restoreContext("server/client-context.pk")
  server_he.restorepublicKey("server/client-pubkey.pk")
  dataset = pickle.load(request.files["dataset"])

  return "%d rows" % len(dataset), 200

@app.route("/delete")
def delete():
  global server_he, dataset
  server_he = None
  dataset = None
  return "", 200


@app.route("/get", methods=["GET"])
def download():
  if server_he is None:
    return "no encrypted data registered", 400
  return pickle.dumps(dataset), 200

@app.route("/aggregate", methods=["GET"])
def aggregate():

  agg_param = request.args.get("on")

  cols = ["AREA", "AGE GROUP", "SEX"]

  if agg_param not in cols:
    return "invalid or missing aggregation parameter: %s. must be one of %s" % (agg_param, cols), 400

  if server_he is None or dataset is None:
    return "no encrypted data registered", 400

  # Note NO decryption!
  result = deserialise(server_he, dataset)
  cols = [c for c in cols if c != agg_param]
  result = result.groupby(level=cols).sum()
  result = serialise(result)

  return pickle.dumps(result), 200

if __name__ == "__main__":
  app.run()