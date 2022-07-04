from pymongo import MongoClient
from fastapi import FastAPI
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware

client = MongoClient("MONGO_URI")
collection = client['test']['test-db']


app = FastAPI()
origins = ["*"]

app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],)

@app.get("/attendance")
def attendance(roll:Optional[int]=None):
    if (roll == None):
        json = {"data":[]}
        for i in collection.find():
            json["data"].append(i)
        return json
    else:
        att = collection.find({"_id":roll})
        for i in att:
            return i
