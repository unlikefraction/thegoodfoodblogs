import os
from livereload import Server, shell

def rebuild():
    os.system('python render.py')

if __name__ == "__main__":
    server = Server()
    server.watch('templates/', rebuild)
    server.watch('blog_posts/', rebuild)
    server.watch('static/', shell('python render.py'))
    server.serve(root='output')
