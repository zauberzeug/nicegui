from nicegui import ui


def scroll_tree_to_position(tree_id: int, text: str) -> None:
    """Scroll the tree to the position of the node with the given text, failing silently if not found."""
    ui.run_javascript(f'''
        Array.from(getHtmlElement({tree_id})?.getElementsByTagName("a") ?? [])
            .find(el => el.innerText.trim() === "{text}")
            ?.scrollIntoView({{block: "center"}});
    ''')
