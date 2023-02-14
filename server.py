from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get('/')
@app.get('/home/', response_class=HTMLResponse)
def home_page(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('home_page.html', context=context)


@app.post('/login')
def login(username=Form(), password=Form()):
    return {"name": username, "password": password}

