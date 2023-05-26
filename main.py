from typing import Any
from fastapi import FastAPI, Response, status, HTTPException
from random import randrange
from typing import Optional
from pydantic import BaseModel

# from schemas import CreatePost, Post

# from databases import my_posts
# from services import find_post

app = FastAPI()

my_posts = [
    {
        "id": 1,
        "title": "string",
        "content": "string",
        "published": True,
        "rating": 0
    },
    {
        "id": 2,
        "title": "string",
        "content": "string",
        "published": True,
        "rating": 0
    },
    {
        "id": 3,
        "title": "string",
        "content": "string",
        "published": True,
        "rating": 0
    },
    {
        "id": 4,
        "title": "string",
        "content": "string",
        "published": True,
        "rating": 0
    },

]


def find_post(id) -> int:
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return post
        return None



class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None



@app.get('/posts/latest')
def latest_posts():
    latest_posts = my_posts[len(my_posts)-1]
    return {
        'status': True,
        'message': 'Latest posts',
        'data': latest_posts
    }


@app.get('/posts', status_code=status.HTTP_200_OK)
async def posts():
    posts = my_posts
    return {
        'status': True,
        'message': 'Posts',
        'data': posts
    }


@app.get('/posts/{post_id}', status_code=status.HTTP_200_OK)
async def post_detail(post_id: int, response: Response):
    post = find_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
    return {
        'status': True,
        'message': 'Post detail',
        'data': post
    }


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: CreatePost) -> Any:
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {
        'status': True,
        'message': 'Post created successfully',
        'data': post_dict
    }
