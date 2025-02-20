from fastapi import FastAPI
from api import endpoints

app = FastAPI()

# Include versioned APIs
app.include_router(endpoints.router)