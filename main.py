from dataclasses import dataclass
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import frontmatter
import os
import pyromark

OUT_DIR = "./public"
TEMPLATE_DIR = "./templates"
STATIC_DIR = "./static"


@dataclass
class Post:
    title: str
    date: str
    tags: list[str]
    slug: str
    content: str
    html_content: str = ""
    excerpt: str = ""


def load_post(filepath: str) -> Post:
    def generate_slug(filepath: str, post_date: datetime) -> str:
        filename = filepath.split("/")[-1].replace(".md", "")
        date_str = post_date.strftime("%Y/%m/%d")
        return f"posts/{date_str}/{filename}"

    def generate_date_string(date: datetime | None) -> str:
        FORMAT = "%d %B, %Y %I.%M %p"
        if date is None:
            return datetime.now().strftime(FORMAT)
        try:
            return date.strftime(FORMAT)
        except ValueError:
            return datetime.now().strftime(FORMAT)

    with open(filepath, "r") as f:
        post_data = frontmatter.load(f)

    title = post_data.get("title", "Untitled")
    date = generate_date_string(post_data.get("date"))
    slug = generate_slug(filepath, post_data.get("date", datetime.now()))
    tags = post_data.get("tags", [])
    content = post_data.content
    html_content = pyromark.html(content)
    excerpt = post_data.get(
        "excerpt", content[:200] + "..." if len(content) > 200 else content
    )

    return Post(
        title=title,
        date=date,
        tags=tags,
        slug=slug,
        content=content,
        html_content=html_content,
        excerpt=excerpt,
    )


def copy_static_files():
    if not os.path.exists(STATIC_DIR):
        return
    for root, _dirs, files in os.walk(STATIC_DIR):
        for file in files:
            src_path = os.path.join(root, file)
            rel_path = os.path.relpath(src_path, STATIC_DIR)
            dest_path = os.path.join(OUT_DIR, rel_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(src_path, "rb") as src_file:
                with open(dest_path, "wb") as dest_file:
                    dest_file.write(src_file.read())


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

    copy_static_files()


def main():
    render_site()

    print("Site generated successfully.")
    print("contents for ./public:")
    for root, _dirs, files in os.walk(OUT_DIR):
        level = root.replace(OUT_DIR, "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 2 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")


if __name__ == "__main__":
    main()
