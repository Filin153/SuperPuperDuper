import os
from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles
from config.config import tmp, settings
from fastapi.middleware.cors import CORSMiddleware
from transport.auth import auth_router
from transport.user import user_router
from transport.file import file_router



try:
    os.mkdir("./file")
except FileExistsError:
    pass

if settings.debug:
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(file_router)


@app.get("/")
async def reg(request: Request):
    return tmp.TemplateResponse("reg.html", {"request": request})


@app.get("/signin")
async def reg(request: Request):
    return tmp.TemplateResponse("signin.html", {"request": request})


@app.get("/add")
async def reg(request: Request):
    return tmp.TemplateResponse("add_file.html", {"request": request})
