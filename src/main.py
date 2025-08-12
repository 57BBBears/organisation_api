import uvicorn
from fastapi import APIRouter, FastAPI, Depends

from src.routers import activity, building, geo, organisation
from src.services.auth.security import check_auth


app = FastAPI(title="Organisation API", dependencies=[Depends(check_auth)])

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(activity.api)
v1_router.include_router(building.api)
v1_router.include_router(geo.api)
v1_router.include_router(organisation.api)

app.include_router(v1_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
