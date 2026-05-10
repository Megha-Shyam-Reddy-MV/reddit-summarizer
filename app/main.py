from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from fastapi.responses import JSONResponse

from app.reddit_client import fetch_post_and_comments
from app.summarizer import summarize_reddit_thread

app = FastAPI()
limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):

    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded"
        }
    )

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "summary": None
        }
    )


@app.get("/summarize", response_class=HTMLResponse)
def summarize(request: Request, url: str):

    reddit_data = fetch_post_and_comments(url)

    summary = summarize_reddit_thread(reddit_data)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "summary": summary,
            "title": reddit_data["title"]
        }
    )

@app.get("/api/summarize")
@limiter.limit("5/minute")
def summarize_api(request: Request, url: str):

    reddit_data = fetch_post_and_comments(url)

    summary = summarize_reddit_thread(reddit_data)

    return {
        "title": reddit_data["title"],
        "summary": summary
    }