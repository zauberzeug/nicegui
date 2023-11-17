from nicegui import ui


def main_demo() -> None:
    ui.code('''
        from nicegui import ui
        
        ui.label('Code inception!')
            
        ui.run()
    ''').classes('w-full')
