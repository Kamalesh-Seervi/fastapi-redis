from fastapi import FastAPI
import redis
import requests
app=FastAPI()

rd = redis.Redis(host='redis', port=6379, db=0)

@app.get("/")
def home():
    return "hello worlds"


@app.get("/fish/{species}")
def fetch_fish(species:str):
    cache= rd.get(species)
    if cache:
        print("cache hit")
    else:
        print("cache is not there in redis")
        data=requests.get(f"https://www.fishwatch.gov/api/species/{species}").json()
        rd.set(species,data.text)
        return data.json()
        
        

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)