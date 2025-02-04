import uvicorn
from fastapi import FastAPI
from v1.app import app as app_v1
from v2.app import app as app_v2

app = FastAPI()

app.mount("/v1", app_v1)
app.mount("/v2", app_v2)

@app.get("/")
async def read_root():
    return {
        "message": "ASCOR API",
        "versions": ["v1", "v2"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", log_level="info")