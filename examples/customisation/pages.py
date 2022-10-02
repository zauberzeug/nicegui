import custom


def create():
    for index, name in enumerate(['A', 'B', 'C', 'D'], 1):
        # here we store the custom page builder in a variable and pass the specific contend for every page
        page_builder = custom.page(f'/{name.lower()}', navtitle=f'- {name} -', step=index)
        page_builder(create_content, title=name)


def create_content(title: str) -> None:
    custom.headline(f'Page {title}')
