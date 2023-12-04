from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session
from tmdb import get_json
import crud, schemas, models
from database import SessionLocal, engine
from typing import Optional

app = FastAPI()

# Habilita CORS (permite que o Svelte acesse o FastAPI)
origins = [
     "http://localhost",
     "http://localhost:5173",
     "http://127.0.0.1:5173"
    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    #allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    #allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

genres = [{'id': 28, 'name': 'Ação'}, 
    {'id': 12, 'name': 'Aventura'}, 
    {'id': 16, 'name': 'Animação'}, 
    {'id': 35, 'name': 'Comédia'}, 
    {'id': 80, 'name': 'Crime'}, 
    {'id': 99, 'name': 'Documentário'},
    {'id': 18, 'name': 'Drama'},
    {'id': 10751, 'name': 'Família'}, 
    {'id': 14, 'name': 'Fantasia'}, 
    {'id': 36, 'name': 'História'}, 
    {'id': 27, 'name': 'Terror'},
    {'id': 10402, 'name': 'Música'}, 
    {'id': 9648, 'name': 'Mistério'}, 
    {'id': 10749, 'name': 'Romance'},
    {'id': 878, 'name': 'Ficção Científica'},
    {'id': 10770, 'name': 'Filme de TV'},
    {'id': 53, 'name': 'Suspense'},
    {'id': 10752, 'name': 'Guerra'}, 
    {'id': 37, 'name': 'Faroeste'}
    ]

@app.get("/api/genres")
def read_genres():
    return genres

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

models.Base.metadata.create_all(bind=engine)


@app.get("/filme/{title}")
async def find_movie(title: str):
    return {"tmdb_id": title}

@app.get("/artista/filmes")
async def find_filmes_artista(personId: int):
    return {"id": personId}

# PESQUISA FILMES ------------------------------------------------------------------------------------------------

@app.get("/filmes")
async def filmes(search: Optional[str] = None):
    if search:
        # Realiza a busca de filmes pelo termo de pesquisa
        data_search = get_json("/search/movie", f"?query={search}&language=en-US")
        results_search = data_search['results']
        filmes_search = []
        for movie in results_search:
            filmes_search.append({
                "title": movie['original_title'],
                "image": f"https://image.tmdb.org/t/p/w185{movie['poster_path']}",
                "tmdb_id": movie['id']
            })
        return {"search": filmes_search}
    else:
        # Buscar filmes populares
        data_populares = get_json("/discover/movie", "?sort_by=vote_count.desc")
        results_populares = data_populares['results']
        populares = [{
            "title": movie['original_title'],
            "image": f"https://image.tmdb.org/t/p/w185{movie['poster_path']}",
            "tmdb_id": movie['id']
        } for movie in results_populares[:4]]

        # Buscar filmes em estreia
        data_estreias = get_json("/movie/now_playing", "?language=en-US")
        results_estreias = data_estreias['results']
        estreias = [{
            "title": movie['original_title'],
            "image": f"https://image.tmdb.org/t/p/w185{movie['poster_path']}",
            "tmdb_id": movie['id']
        } for movie in results_estreias[:4]]

        return {"populares": populares, "estreias": estreias}


#PESQUISA DE ARTISTAS ----------------------------------------------------------------------------------------------
@app.get("/artistas/{name}")
async def get_artista(name: str):
    artist_name = get_json("/search/person", f"?query={name}&language=en-US")
    results = artist_name['results']
    filtro = []
    for artist in results:
        artist_id = get_json("/person", f"/{artist['id']}?language=en-US")
        filtro.append({
            'id': artist_id['id'],
            "name": artist_id['name'],
            'rank': artist_id['popularity'],
            'biography': artist_id['biography'],
            "profile_path": artist_id['profile_path']
        })
    filtro.sort(reverse=True, key=lambda artist: artist['rank'])
    return filtro

# USUÁRIOS ------------------------------------------------------------------------------------------------
@app.get("/getUsers")
def read_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users

# ADICIONA USUARIO ----------------------------------------------------------------------------------------
@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# ATUALIZAÇÃO DE USUÁRIO ----------------------------------------------------------------------------------
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = crud.update_user(db, user_id=user_id, user=user)
    return db_user

# DELETAR USUÁRIO -----------------------------------------------------------------------------------------
@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id=user_id)
    return JSONResponse(content={"message": "User deleted successfully"}, status_code=200)

# BUSCAR USUÁRIO PELO ID ----------------------------------------------------------------------------------
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# FAVORITAR FILME ---------------------------------------------------------------------------------------
@app.post("/favorites/{user_id}/{tmdb_id}")
def favorite_movie(user_id: int, tmdb_id: int, db: Session = Depends(get_db)):
    # Fetch movie details from TMDB
    movie_details = get_json("/movie", f"/{tmdb_id}?language=en-US")
    movie_title = movie_details['original_title']
    movie_image = f"https://image.tmdb.org/t/p/w185{movie_details['poster_path']}"

    # Use the correct variable names
    return crud.favorite_movie(db=db, user_id=user_id, tmdb_id=tmdb_id, title=movie_title, image=movie_image)

# PEGAR TODOS OS FILMES FAVORITADOS ----------------------------------------------------------------------
@app.get("/favorites/{user_id}", response_model=list[schemas.Movie])
def get_favorites(user_id: int, db: Session = Depends(get_db)):
    favorites = crud.get_favorito(db, user_id=user_id)
    return favorites

# DELETA FILME FAVORITO/DESFAVORITA ----------------------------------------------------------------------
@app.delete("/deleteFavoritos/{user_id}/{tmdb_id}", response_model=schemas.Movie)
def delete_favorites(user_id: int, tmdb_id:int, db: Session = Depends(get_db)):
    delete = crud.delete_favorito(db, user_id=user_id, tmdb_id=tmdb_id)
    return delete
# FAVORITA ARTISTAS ----------------------------------------------------------------------------------------
@app.post("/favorites/artist/{user_id}/{artist_id}")
def favorite_artista(user_id: int, tmdb_id: int, db: Session = Depends(get_db)):
    return crud.favorite_artista(db=db, user_id=user_id, tmdb_id=tmdb_id)

# LISTA TODOS OS ARTISTAS FAVORITOS ------------------------------------------------------------------------
@app.get("/favoritesArtist/{user_id}", response_model=list[schemas.Movie]) 
def get_favorites_artista(user_id: int, db: Session = Depends(get_db)):
    return crud.get_favorites_artista(db, user_id=user_id)

# DELETA/ DESFAVORITA O ARTISTA ----------------------------------------------------------------------------
@app.delete("/deleteFavoritesArtista/{user_id}/{tmdb_id}", response_model=schemas.Movie)
def delete_favorites_artista(user_id: int, tmdb_id: int, db: Session = Depends(get_db)):
    delete = crud.favorite_artista(db, user_id=user_id, tmdb_id=tmdb_id)
    return delete


# source env/bin/activate
# uvicorn pycine:app --reload
# npm run dev
