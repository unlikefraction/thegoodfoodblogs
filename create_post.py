import os
from datetime import datetime
from slugify import slugify

from render import render_all

def create_post(title):
    post_slug = slugify(title)
    filename = f'blog_posts/{post_slug}.html'
    
    # Ensure blog_posts directory exists
    if not os.path.exists('blog_posts'):
        os.makedirs('blog_posts')

    # Ensure static/images directory exists
    images_dir = f'static/images/{post_slug}'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    if os.path.exists(filename):
        print(f"Post {filename} already exists!")
        return

    with open(filename, 'w') as f:
        f.write(f"""{{% extends "base.html" %}}
{{% block title %}}{title} – The Good Food Project{{% endblock %}}

{{% block seo %}}
<!-- Description -->
<meta name="description" content="Description for {title}">
<meta name="keywords" content="{title.lower().replace(' ', ', ')}">

<!-- Open Graph Tags -->
<meta property="og:title" content="{title} – The Good Food Project">
<meta property="og:description" content="Description for {title}">
<meta property="og:image" content="/static/images/{post_slug}/link-share-thumbnail.jpg">

<!-- Twitter Card Tags -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} – The Good Food Project">
<meta name="twitter:description" content="Description for {title}">
<meta name="twitter:image" content="/static/images/{post_slug}/link-share-thumbnail.jpg">
{{% endblock %}}

{{% block blog_title %}}{title}{{% endblock %}}
{{% block blog_date %}}{datetime.now().strftime('%d %B, %Y')}{{% endblock %}}

{{% block blog %}}
<!-- Sources -->
<details>
    <summary>Sources</summary>
    <ol>
        <li><a href="#">Source 1</a></li>
        <li><a href="#">Source 2</a></li>
        <li><a href="#">Source 3</a></li>
        <!-- Add more sources as needed -->
    </ol>
</details>

<!-- Blog Content -->
<div class="blog_content">
    <p>This is the content of {title}</p>
    <p><b>Stay healthful! See you on another Good Food blog.</b></p>
</div>

<!-- Blog Info for search engines -->
<script type="application/ld+json">
    {{
      "@context": "http://schema.org",
      "@type": "Article",
      "headline": "{title} – The Good Food Project",
      "image": "/static/images/{post_slug}/link-share-thumbnail.jpg",
      "author": "Your Name",
      "publisher": {{
        "@type": "Organization",
        "name": "The Good Food Project",
        "logo": {{
          "@type": "ImageObject",
          "url": "/logo.png"
        }}
      }},
      "datePublished": "{datetime.now().strftime('%Y-%m-%d')}"
    }}
</script>    
{{% endblock %}}
""")
    print(f"Created new post: {filename} and image directory: {images_dir}")

if __name__ == "__main__":
    title = input("Enter the title of the new post: ")
    create_post(title)
    render_all()
    
    print("To run the server, run `python server.py`")
