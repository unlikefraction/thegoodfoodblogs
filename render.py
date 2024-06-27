import os
import shutil
import re
from jinja2 import Environment, FileSystemLoader
from dateutil import parser
from datetime import datetime

# Load Jinja2 environment with multiple template directories
env = Environment(loader=FileSystemLoader(['templates', 'blog_posts']))

# List of static pages
static_pages = ['contact.html', 'about.html']

def render_static_page(page):
    template = env.get_template(page)
    output = template.render()
    
    output_path = os.path.join('output', page)
    with open(output_path, 'w') as f:
        f.write(output)
    print(f"Rendered {output_path}")

def render_blog_post(post):
    post_filename = os.path.splitext(os.path.basename(post))[0]
    template = env.get_template(f'{post_filename}.html')
    output = template.render()
    
    output_path = os.path.join('output', f'{post_filename}.html')
    with open(output_path, 'w') as f:
        f.write(output)
    print(f"Rendered {output_path}")

def copy_static_files():
    if os.path.exists('output/static'):
        shutil.rmtree('output/static')
    shutil.copytree('static', 'output/static')
    print("Copied static files")

def render_home(posts):
    template = env.get_template('home.html')
    output = template.render(posts=posts)
    output_path = os.path.join('output', 'index.html')
    with open(output_path, 'w') as f:
        f.write(output)
    print(f"Rendered {output_path}")

def extract_post_metadata(content):
    title = "Untitled"
    date = None

    title_pattern = r"{%\s*block\s+blog_title\s*%}(.*?){%\s*endblock\s*%}"
    date_pattern = r"{%\s*block\s+blog_date\s*%}(.*?){%\s*endblock\s*%}"

    title_match = re.search(title_pattern, content, re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()

    date_match = re.search(date_pattern, content, re.DOTALL)
    if date_match:
        date_str = date_match.group(1).strip()
        try:
            date = parser.parse(date_str)
        except ValueError:
            print(f"Error parsing date: {date_str}")
            date = None

    return title, date

def generate_sitemap(pages, posts):
    now = datetime.now().strftime('%Y-%m-%d')
    sitemap_entries = []

    for page in pages:
        sitemap_entries.append(f"""
    <url>
        <loc>/{page}</loc>
        <lastmod>{now}</lastmod>
    </url>""")

    for post in posts:
        sitemap_entries.append(f"""
    <url>
        <loc>/{post['url']}</loc>
        <lastmod>{now}</lastmod>
    </url>""")

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {''.join(sitemap_entries)}
</urlset>"""

    with open('output/sitemap.xml', 'w') as f:
        f.write(sitemap_content)
    print("Generated sitemap.xml")

def render_all():
    if not os.path.exists('output'):
        os.makedirs('output')

    posts = []

    for page in static_pages:
        render_static_page(page)
    
    for post in os.listdir('blog_posts'):
        if post.endswith('.html'):
            post_path = os.path.join('blog_posts', post)
            render_blog_post(post_path)
            
            with open(post_path, 'r') as f:
                content = f.read()
                title, date = extract_post_metadata(content)
                post_filename = os.path.splitext(post)[0]

                if date:
                    posts.append({
                        'url': f'{post_filename}.html',
                        'title': title,
                        'date': date.strftime('%Y-%m-%d')
                    })

    posts = sorted(posts, key=lambda x: x['date'], reverse=True)

    render_home(posts)
    copy_static_files()
    generate_sitemap(static_pages, posts)

if __name__ == "__main__":
    render_all()
