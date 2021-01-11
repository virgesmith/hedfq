# encrypted server - stores, and operates on, encrypted data
# despite not being able to decrypt it


from flask import Flask, request
import pandas as pd
from Pyfhel import Pyfhel, PyCtxt
from base64 import b64encode, b64decode
import pickle

from hedfq.utils import deserialise #, ENCODING


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

  request.files["pubkey"].save("server/client-pubkey.pk")
  request.files["context"].save("server/client-context.pk")

  server_he = Pyfhel()
  # NOTE: these functions segfault if given the wrong data or not done in this order
  server_he.restoreContext("server/client-context.pk")
  server_he.restorepublicKey("server/client-pubkey.pk")
  dataset = pickle.load(request.files["dataset"])

  return "%d rows" % len(dataset), 200

@app.route("/get", methods=["GET"])
def download():
  if server_he is None:
    return "no encrypted data registered", 400
  return pickle.dumps(dataset), 200

@app.route("/query", methods=["GET"])
def query():
  if server_he is None:
    return "no encrypted data registered", 400

  df = deserialise(server_he, dataset)

  # TODO

  return "", 200

if __name__ == "__main__":
  app.run()