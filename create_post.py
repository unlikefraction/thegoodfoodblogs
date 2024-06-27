import os
from datetime import datetime

def create_post(title):
    post_slug = title.lower().replace(' ', '_')
    filename = f'blog_posts/{post_slug}.html'
    if os.path.exists(filename):
        print(f"Post {filename} already exists!")
        return

    with open(filename, 'w') as f:
        f.write(f"""{{% extends "blog_post.html" %}}
{{% block title %}}{title}{{% endblock %}}
{{% block description %}}Description for {title}{{% endblock %}}
{{% block keywords %}}{title.lower().replace(' ', ', ')}{{% endblock %}}
{{% block content %}}
<p>This is the content of {title}. <em>Feel free to add any HTML, CSS, or JS here.</em></p>
<script>
    console.log('{title} loaded');
</script>
{{% endblock %}}
""")
    print(f"Created new post: {filename}")

if __name__ == "__main__":
    title = input("Enter the title of the new post: ")
    create_post(title)
