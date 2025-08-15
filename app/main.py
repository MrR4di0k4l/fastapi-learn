from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader
from auth.apikey_auth import get_current_user
import uvicorn
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from tasks.routes import router as task_routes
from users.routes import router as user_routes
from users.models import UserModel


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Application startup")
    # Base.metadata.create_all(bind=engine)
    yield 

    print("Application shutdown")

app = FastAPI(
    lifespan=lifespan,
    title="Simple Todo App Api",
    description="this is a simple blog app with minimal usage of authentication and post managing",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Ali Bigdeli",
        "url": "https://thealibigdeli.ir/",
        "email": "bigdeli.ali3@gmail.com",
    },
    license_info={"name": "MIT"},
    docs_url="/swagger",
)

app.include_router(task_routes, prefix="/api/v1")
app.include_router(user_routes)

header_scheme = APIKeyHeader(name="x-key")

@app.get("/private")
def private_route(api_key : UserModel =  Depends(get_current_user)):
    print(api_key)
    return api_key

    
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="info", reload=True)