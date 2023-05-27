from typing import Any
from fastapi import FastAPI, Response, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from schemas import CreatePost
import time
from decouple import config

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(
            host=config('DATABASE_HOST'), database=config('DATABASE_NAME'), user=config('DATABASE_USER'), password=config('DATABASE_PASSWORD'), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful')
        break
    except Exception as e:
        print('Connection to database failed')
        print('ERROR:', str(e))
        time.sleep(2)


@app.get('/api/v1/posts/latest')
def latest_posts():
    cursor.execute('SELECT * FROM post')
    posts = cursor.fetchall()
    latest_posts = posts[len(posts)-1]
    return {
        'status': True,
        'message': 'Latest posts',
        'data': latest_posts
    }


@app.get('/api/v1/posts', status_code=status.HTTP_200_OK)
async def posts():
    cursor.execute('SELECT * FROM post')
    posts = cursor.fetchall()
    return {
        'status': True,
        'message': 'Posts',
        'data': posts
    }


@app.get('/api/v1/posts/{post_id}', status_code=status.HTTP_200_OK)
async def post_detail(post_id: int, response: Response):
    cursor.execute('SELECT * FROM post WHERE id = %s', (str(post_id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    return {
        'status': True,
        'message': 'Post detail',
        'data': post
    }


@app.post('/api/v1/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost) -> Any:
    cursor.execute('INSERT INTO post(title,content,published) VALUES(%s,%s,%s) RETURNING *',
                   (post.title, post.content, post.published))
    post = cursor.fetchone()
    conn.commit()
    return {
        'status': True,
        'message': 'Post created successfully',
        'data': post
    }


@app.delete('/api/v1/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, response=Response):
    cursor.execute('DELETE FROM post where id = %s', (str(post_id)))
    conn.commit()
    return {
        'status': True,
        'message': 'Post deleted successfully'
    }
