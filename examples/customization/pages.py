import custom


def create():
    for name in ['A', 'B', 'C', 'D']:
        # here we store the custom page builder in a variable and pass the specific contend for every page
        page_builder = custom.page(f'/{name.lower()}', navtitle=f'- {name} -')
        page_builder(create_content, title=name)


def create_content(title: str) -> None:
    custom.headline(f'Page {title}')
