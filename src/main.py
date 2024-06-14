from fastapi import FastAPI
from pydantic import BaseModel
import json
import logging


app = FastAPI()

logging.basicConfig(filename='./logs/app.log', level=logging.WARNING, format='{"time": "%(asctime)s", "name": "%(name)s", "level": "%(levelname)s", "message": "%(message)s"}')

logger = logging.getLogger(__name__)

blog_posts = []


class Post(BaseModel):
    id: str
    title: str 
    content: str

class PostItems(BaseModel):
    title: str 
    content: str


class BlogPost:
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content
    def __str__(self) -> str:
        return f'{self.id} - {self.title} - {self.content}'
    
    def toJson(self):
        return {'id': self.id, 'title': self.title, 'content': self.content}

@app.post('/blog')
async def create_blog_post(post: Post):
    try:
        blog_posts.append(BlogPost(post.id, post.title, post.content))
        logger.info('Creating a new blog post')
        return json.dumps({'status':'sucess'}), 201
    except KeyError:
        logger.warning('Invalid request')
        return json.dumps({'error': 'Invalid request'}), 400
    except Exception as e:
        logger.error(str(e))
        return json.dumps({'error': str(e)}), 500


@app.get('/blog')
async def get_blog_posts():
    logger.info('Getting all blog posts')
    return json.dumps({'posts': [blog.toJson() for blog in blog_posts]}), 200


@app.get('/blog/<int:id>')
async def get_blog_post(id):
    for post in blog_posts:
        if post.id == id:
            logger.info(f'Getting blog post with id {id}')
            return json.dumps({'post': post.__dict__}), 200
    logger.warning(f'Blog post with id {id} not found')
    return json.dumps({'error': 'Post not found'}), 404

@app.delete('/blog/<int:id>')
async def delete_blog_post(id):
    for post in blog_posts:
        if post.id == id:
            blog_posts.remove(post)
            logger.info(f'Deleting blog post with id {id}')
            return json.dumps({'status':'sucess'}), 200
    logger.warning(f'Blog post with id {id} not found')
    return json.dumps({'error': 'Post not found'}), 404

@app.put('/blog/<int:id>')
def update_blog_post(id, post: PostItems):
    try:
        for post in blog_posts:
            if post.id == id:
                post.title = post.title
                post.content = post.content
                logger.info(f'Updating blog post with id {id}')
                return json.dumps({'status':'sucess'}), 200
        logger.warning(f'Blog post with id {id} not found')
        return json.dumps({'error': 'Post not found'}), 404
    except KeyError:
        logger.warning('Invalid request')
        return json.dumps({'error': 'Invalid request'}), 400
    except Exception as e:
        logger.error(str(e))
        return json.dumps({'error': str(e)}), 500
