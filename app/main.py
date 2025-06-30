import asyncio,os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from app.routes.api.v1 import user
from app.middleware.Ratelimiter import RateLimiterMiddleware


# Define the list of exempt routes
EXEMPT_ROUTES = [
    "/docs",            # OpenAPI documentation
    "/redoc",           # ReDoc documentation
    "/openapi.json",    # OpenAPI schema
    "/user/search"
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    for route in app.routes:
        print(route.path,route.name)
    # Perform startup tasks (e.g., connect to a database)
    yield
    print("Shutting down...")
    # Perform cleanup tasks (e.g., close database connections)
    await asyncio.sleep(1)
    print("Graceful shutdown complete.")

app = FastAPI(title="SökerData", lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(RateLimiterMiddleware)
# Include routers
app.include_router(user.router, prefix="/user", tags=["user"])

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload= os.getenv("ENVIRONMENT")=='Developement')
