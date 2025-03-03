from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import endpoints

app = FastAPI()

# Include versioned APIs
app.include_router(endpoints.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)