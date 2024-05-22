from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


conn = psycopg.connect("dbname=fastapi_app user=postgres")
cur = conn.cursor()

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_of_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/posts")
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"data": posts}


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                (post.title, post.content, post.published))
    post = cur.fetchone()
    conn.commit()
    return {"data": post}


@app.get("/posts/latest")
def get_latest_post():
    return {"post_detail": my_posts[-1]}


@app.get("/posts/{id}")
def get_post(id: str):
    cur.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):
    cur.execute("""DELETE FROM posts WHERE id = %s""", (str(id),))
    post = cur.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: str, post: Post):
    cur.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",
                (post.title, post.content, post.published, str(id)))
    updated_post = cur.fetchone()
    conn.commit()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return {'data': update_post}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}
