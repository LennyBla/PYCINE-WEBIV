import requests
import uvicorn
from fastapi import FastAPI 
api_key = "6f77cb8794e999fed44476c8b3303723"
endpoint = "https://api.themoviedb.org/3/discover/movie"

params = f"?include_adult=false&include_video=false&language=en-US&page=1&sort_by=vote_count.desc&year=2023"

url = f"{endpoint}{params}&api_key={api_key}"

headers = {"accept": "application/json"} 

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

def get_json(endpoint, params=None):
    """fornecido o endpoint faz o request e rerorna
    o resultado en json"""
    url = f"https://api.themoviedb.org/3{endpoint}{params}&api_key={api_key}"
    response = requests.get(url)
    return response.json()

# retorna o nome do genero de acordo com o id
def get_genero_id(id):
    for genre in genres:
        if genre['id'] == id:
            #print(id, genre['name'])
            return genre ['name']
    return None

# busca filme pelo título
def get_movie_by_name(name: str):
    data = get_json(
        "https://api.themoviedb.org/3/search/movie",
        f"?query={name}"
    )
    return data

# busca artisa pelo nome
def get_artist_by_name(name: str):
    data = get_json(
        "https://api.themoviedb.org/3/search/person",
        f"?query={name}"
    )
    return data

app = FastAPI()

@app.get('/week')
def get_week_movies():
    data = get_json(
        "https://api.themoviedb.org/3/trending/movie/week?language=en-US",
        ""
    )
    five_movies: [str] = []
    for movie in data['results']:
        five_movies.append(movie)
        if len(five_movies) == 5:
            break
    return five_movies

def filmes_populares():
    data = get_json(
        "https://api.themoviedb.org/3/discover/movie",
        "?sort_by=vote_count.desc&language=en-US"
    )
    results = data['results']
    print("=" * 20)
    for movie in results:
        print(movie['original_title'])
        print(movie['id'])
        print(movie['genre_ids'])
        print(movie['vote_count'])
        print("----")

    print(f"Total: {len(results)}")
   
#Faz a requisição GET para a url
# salva na variável response o resultado na busca do TMDB

response = requests.get(url, headers=headers)

#print(response.txt)

data = response.json()

page = data['page']

print(f"page: {page}")

filme1 = data['results'][0]

#Obtem apenas o titulo do primeiro filme
print(filme1['original_title'])

#IMPRIMIR o título de todos os filmes em "data"

results = data['results']
print("="*20)
for movie in results:
    print(movie['original_title'])
    print(movie['id'])
    print(movie['vote_count'])
    print("------------")
print(f"Total:{len(results)}")

# Obter os gêneros

end = "https://api.themoviedb.org/3/genre/movie/list"
params = "?language=en&api_key=" + api_key
url = f"{end}{params}"

response = requests.get(url)
data = response.json()

if 'genres' in data:
    genres = data['genres']
    print("="*20)
    for genre in genres:
        print(genre['name'])
        print("-------")
else:
    print("Não foi possível obter os gêneros da API.") 
    
if __name__ == "__main__":
    filmes_populares()

    # Obter o nome dos generos
    end = f"https://api.themoviedb.org/3/genre/movie/list"
    params = "?language=en"
    url = f"{end}{params}&api_key={api_key}"
    uvicorn.run("tmdb2:app", host="127.0.0.1", port=8000, reload=True),