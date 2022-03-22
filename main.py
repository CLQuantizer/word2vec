import pandas as pd
import gensim.downloader
import pickle
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing import List
from fastapi import Depends,Request, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#glove_vectors = gensim.downloader.load('glove-wiki-gigaword-50')
app = FastAPI()
app.mount('/static',StaticFiles(directory='static'),name='static')
templates = Jinja2Templates(directory="templates")

#f=open('glove50','wb')
#pickle.dump(glove_vectors,f)
f = open('glove50','rb')
glove_vectors = pickle.load(f)

@app.post("/related/{word}")
async def related(word):
	word = word.lower()
	df = pd.DataFrame(glove_vectors.most_similar(word,topn=15),columns = ['words','sim'])
	words = list(df['words'])
	probs = [round(x,2) for x in list(df['sim'])]
	return {'words':words, 'probs':probs}

@app.get('/',response_class = HTMLResponse)
async def home(request: Request):
    sent = 'Key in a lower case word for its 15 most related words in Glove50'
    return templates.TemplateResponse('home.html',{"request": request, 'sent':sent})

@app.get("/writing_interface/",response_class = HTMLResponse)
async def writing_interface(request:Request):
    return templates.TemplateResponse('writing_interface.html',{"request":request})

@app.get("/all_writings/", response_model=List[schemas.Writing],response_class= HTMLResponse)
async def read_writings(request:Request, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    writings = crud.get_writings(db, skip=skip, limit=limit)
    return templates.TemplateResponse('all_writings.html',{"request":request,"writings":writings})

@app.post("/writings/{writing_id}", response_model=schemas.Writing)
async def create_writing(writing: schemas.WritingCreate, db: Session = Depends(get_db)):
    return crud.create_writing(db=db, writing=writing)
