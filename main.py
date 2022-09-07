from fastapi import FastAPI
from api.core.config import settings
from backend.scrape import check_main_posts, check_under_posts, get_news, get_main_news, get_under_news

app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)


@app.get("/")
def hello_api():
    return {"Hello API"}


@app.get("/check_main_news")
def check_main_news():
    if check_main_posts():
        return {"Nueva noticia en main"}
    else:
        return {"No hay nueva noticia en main"}


@app.get("/check_under_news")
def check_under_news():
    if check_under_posts():
        return {"Nueva noticia en under"}
    else:
        return {"No hay nueva noticia en under"}


@app.get("/get_newest_main_news")
def get_newests_news():
    return get_main_news("newest_post")


@app.get("/get_last_main_news")
def get_newests_news():
    return get_main_news("last_post")


@app.get("/get_newest_under_news")
def get_newests_news():
    return get_under_news("newest_post")


@app.get("/get_last_under_news")
def get_newests_news():
    return get_under_news("last_post")






