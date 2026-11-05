"""把标题转成 URL 友好的 slug。"""


def slugify(title):
    return title.lower().replace(" ", "-")
