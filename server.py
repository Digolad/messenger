from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from project.home_page import HomePage

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/')
@app.get('/home/', response_class=HTMLResponse)
def home_page(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('home_page.html', context=context)


@app.post('/login', response_class=HTMLResponse)
def login(email=Form(), password=Form(), request=Request):
    hp = HomePage()
    user_data = hp.get_user_by_mail(mail=email)
    if user_data is None:
        war_mail = 'The mail not registered yet.'
        context = {'request': request, 'war_mail': war_mail}
        return templates.TemplateResponse('home_page.html', context=context)

    print(user_data)
    if user_data['mail'] == email:
        if user_data['password'] == password:
            return RedirectResponse('/chat')
        return 'wrong password'


@app.post('/chat')
def chat(request: Request):
    context = {'request': request}
    return templates.TemplateResponse('chat.html', context=context)
