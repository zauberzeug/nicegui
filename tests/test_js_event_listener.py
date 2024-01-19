if __name__ == "__main__":
    from nicegui import ui

    ui.input("press `enter` key").on("keyup.enter", js_handler="(evt) => alert(evt)")

    ui.run(reload=False)
