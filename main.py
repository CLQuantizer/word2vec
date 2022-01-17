import pandas as pd
import gensim.downloader
import pickle
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# glove_vectors = gensim.downloader.load('glove-wiki-gigaword-50')
app = FastAPI()
templates = Jinja2Templates(directory="templates")
# f=open('glove50','wb')
# pickle.dump(glove_vectors,f)
f = open('glove50','rb')
glove_vectors = pickle.load(f)

@app.post("/related/{word}")
async def related(word):
	df = pd.DataFrame(glove_vectors.most_similar(word,topn=15),columns = ['words','sim'])
	words = list(df['words'])
	probs = [round(x,2) for x in list(df['sim'])]
	return {'words':words, 'probs':probs}

@app.get('/',response_class = HTMLResponse)
async def home(request: Request):
    sent = 'Key in a lower case word for its 15 most related words in Glove50'
    return templates.TemplateResponse('home.html',{"request": request, 'sent':sent})