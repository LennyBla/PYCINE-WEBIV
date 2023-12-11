from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from tmdb import get_json
import models, schemas

# Recupera um usuário pelo seu ID---------------------------------------------------------------
def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

# Recupera um usuário pelo seu e-mail---------------------------------------------------------------
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Recupera todos os usuários---------------------------------------------------------------
def get_users(db: Session):
    return db.query(models.User).all();

# Cria um novo usuário no banco de dados---------------------------------------------------------------
def create_user(db: Session, user: schemas.UserCreate):
    try:
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = models.User(name=user.name, email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"Error creating user: {e}")
        raise

# Deleta um usuário específico pelo seu ID---------------------------------------------------------------
def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)
    db.commit()
    return user

# Adiciona um filme aos favoritos de um usuário---------------------------------------------------------------
def favorite_movie(db: Session, user_id: int, tmdb_id: int, title: str, image: str):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        return None

    # Obtém detalhes do filme do TMDB---------------------------------------------------------------
    movie_details = get_json("/movie", f"/{tmdb_id}?language=en-US")
    movie_title = movie_details['original_title']
    movie_image = f"https://image.tmdb.org/t/p/w185{movie_details['poster_path']}"

    # Verifica se o filme já está na lista de favoritos do usuário---------------------------------------------------------------
    existing_movie = next((m for m in user.movies if m.tmdb_id == tmdb_id), None)
    if existing_movie is None:
        movie = models.Movie(tmdb_id=tmdb_id, title=movie_title, image=movie_image, user_id=user_id)
        db.add(movie)
        user.movies.append(movie)
        db.commit()
        db.refresh(movie)

    return user.movies

# Lista todos os filmes favoritos de um usuário---------------------------------------------------------------
def get_favorito(db: Session, user_id: int):
    return db.query(models.Movie).filter(models.Movie.user_id == user_id).all()

# Verifica se um filme está na lista de favoritos de um usuário---------------------------------------------------------------
def get_tmdb_id(db: Session, user_id: int, tmdb_id: int):
    return db.query(models.Favorito_movie).filter_by(user_id=user_id, tmdb_id=tmdb_id).first()

# Deleta um filme da lista de favoritos de um usuário---------------------------------------------------------------
def delete_favorito(db: Session, tmdb_id: int, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        return None

    # Remove o filme da lista de favoritos do usuário---------------------------------------------------------------
    favorito = next((m for m in user.movies if m.tmdb_id == tmdb_id), None)
    if favorito:
        user.movies.remove(favorito)
        db.delete(favorito)
        db.commit()
    else:
        favorito = None
    return favorito

# Adiciona um artista aos favoritos de um usuário---------------------------------------------------------------
def favorite_artista(db: Session, user_id: int, tmdb_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        return None

    # Verifica se o artista já está na lista de favoritos do usuário---------------------------------------------------------------
    if not user.artistas:
        artista = models.Artista(tmdb_id=tmdb_id)
        db.add(artista)
        user.artistas.append(artista)
        db.commit()
        db.refresh(artista)
    else:
        existing_artista = next((a for a in user.artistas if a.tmdb_id == tmdb_id), None)
        if existing_artista is None:
            artista = models.Artista(tmdb_id=tmdb_id)
            db.add(artista)
            user.artistas.append(artista)
            db.commit()
            db.refresh(artista)

    return user.artistas

# Lista todos os artistas favoritos de um usuário---------------------------------------------------------------
def get_favorites_artista(db: Session, user_id: int):
    return db.query(models.Artista).filter(models.Artista.user_id == user_id).all()

# Deleta um artista da lista de favoritos de um usuário---------------------------------------------------------------
def delete_favorite_artista(db: Session, tmdb_id: int, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        return None

    # Remove o artista da lista de favoritos do usuário
    favorite_artista = next((a for a in user.artistas if a.tmdb_id == tmdb_id), None)
    if favorite_artista:
        user.artistas.remove(favorite_artista)
        db.delete(favorite_artista)
        db.commit()

    return favorite_artista
