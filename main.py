from dataclasses import dataclass
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import frontmatter
import os
import pyromark

OUT_DIR = "./public"
TEMPLATE_DIR = "./templates"


@dataclass
class Post:
    title: str
    date: str
    tags: list[str]
    slug: str
    content: str
    html_content: str = ""


def load_post(filepath: str) -> Post:
    def generate_slug(filepath: str, post_date: datetime) -> str:
        filename = filepath.split("/")[-1].replace(".md", "")
        date_str = post_date.strftime("%Y/%m/%d")
        return f"posts/{date_str}/{filename}"

    with open(filepath, "r") as f:
        post_data = frontmatter.load(f)

    title = post_data.get("title", "Untitled")
    date = post_data.get("date", datetime.now())
    slug = generate_slug(filepath, date)
    tags = post_data.get("tags", [])
    content = post_data.content
    html_content = pyromark.html(content)

    return Post(
        title=title,
        date=date,
        tags=tags,
        slug=slug,
        content=content,
        html_content=html_content,
    )


def render_site():
    os.makedirs(OUT_DIR, exist_ok=True)

    posts = [load_post("content/posts/java_and_truthy_checks.md")]
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    index_template = env.get_template("index.html")
    index_html = index_template.render(posts=posts, site_title="trevenue44")
    with open(os.path.join(OUT_DIR, "index.html"), "w") as f:
        f.write(index_html)

    post_template = env.get_template("post.html")
    for post in posts:
        post_html = post_template.render(post=post, site_title="trevenue44")
        post_path = os.path.join(OUT_DIR, f"{post.slug}.html")
        os.makedirs(os.path.dirname(post_path), exist_ok=True)
        with open(post_path, "w") as f:
            f.write(post_html)


def main():
    render_site()


if __name__ == "__main__":
    main()
