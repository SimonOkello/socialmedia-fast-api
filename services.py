from databases import my_posts


def find_post(id) -> int:
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return post
        return None
