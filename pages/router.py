from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from hotels.router import get_hotels_by_location_and_time
from fastapi_cache.decorator import cache
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/search", response_class=HTMLResponse)
# @cache(expire=30)
async def get_hotels_page(
        request: Request,
        hotels=Depends(get_hotels_by_location_and_time)
):
    return templates.TemplateResponse(name="hotels.html",
                                      context={"request": request,
                                               "hotels": hotels})
