import json
import random
import time

from fastapi import FastAPI, Form
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, Response, RedirectResponse
from starlette.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
powered_by = [
    "RCE as a feature.",
    "Unicorns & fairy dust.",
    "Three pi's in a trench-coat.",
    "An overworked, underpaid hamster.",
    "Pretty graphs for someone who dropped a stats minor.",
    "You seeing this proves I can make software which doesn't only break.",
]
with open("creds.json", "r") as f:
    data: dict[str, str] = json.loads(f.read())

origins = ["http://127.0.0.1:8000", "https://tbue.skelmis.co.nz"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    message: str


class Success(Message):
    class Config:
        schema_extra = {
            "example": {
                "message": "Successful login.",
            }
        }


class Failure(Message):
    class Config:
        schema_extra = {
            "example": {
                "message": "Login failed.",
            }
        }


@app.middleware("http")
async def timer_injection(request: Request, call_next):
    start = time.time()
    response: Response = await call_next(request)
    finish = time.time()
    response.headers["X-TIME-SECONDS"] = str(finish - start)
    return response


@app.middleware("http")
async def header_injection(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-POWERED-BY"] = random.choice(powered_by)
    return response


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/login/{number}", response_class=HTMLResponse)
async def login_form(request: Request, number: int):
    return templates.TemplateResponse(
        "login_form.html", {"request": request, "number": number}
    )


@app.post(
    "/login/1",
    responses={
        200: {"model": Success},
        401: {"model": Failure},
    },
    description="Your typical login form, enumeration based on status codes or response body.",
)
async def login_one(username: str = Form(), password: str = Form()):
    pw = data.get(username, False)
    if pw and pw == password:
        return JSONResponse(content={"message": "Success"}, status_code=200)
    return JSONResponse(content={"message": "Invalid authentication"}, status_code=401)


@app.post(
    "/login/2",
    responses={
        200: {"model": Message},
        400: {"model": Message},
    },
    description="A login form with no (visible) information leakage.",
)
async def login_two(username: str = Form(), password: str = Form()):
    # Example real world flows are more like
    # if user doesnt exist:
    #     return failed
    #
    # # Expensive check here only applies
    # # to valid users for the site
    # if password is not correct:
    #    return failed
    #
    # return logged in
    pw = data.get(username, False)
    if pw:
        # Mimic an expensive password comparison
        time.sleep(random.randint(15, 40) / 100)
        if pw == password:
            return JSONResponse(content={"message": "Success"}, status_code=200)

    return JSONResponse(content={"message": "Invalid authentication"}, status_code=400)


@app.post(
    "/login/3",
    responses={
        200: {"model": Message},
        400: {"model": Message},
    },
    description="A login form with no information leakage.<br>"
    "TBUE is mitigated by constant response times regardless of auth state.",
)
async def login_three(username: str = Form(), password: str = Form()):
    # Example real world flows are more like
    # if user doesnt exist:
    #     return failed
    #
    # # Expensive check here only applies
    # # to valid users for the site
    # if password is not correct:
    #    return failed
    #
    # return logged in
    pw = data.get(username, False)

    # All requests get roughly the same
    # response times, enough to mitigate TBUE
    time.sleep(random.randint(15, 40) / 100)
    if pw and pw == password:
        return JSONResponse(content={"message": "Success"}, status_code=200)

    return JSONResponse(content={"message": "Invalid authentication"}, status_code=400)
