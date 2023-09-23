from nicegui import ui

ui.markdown("""
#### Feature request: 
- [Add Seek](https://github.com/zauberzeug/nicegui/discussions/1636)
            
#### HTML Docs:
- [Audio](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/audio)    
- [Video](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/video)
""")

url_audio = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
url_video = "https://test-videos.co.uk/vids/bigbuckbunny/mp4/h264/360/Big_Buck_Bunny_360_10s_1MB.mp4"
seek_to_video = 0
seek_to_audio = 0

with ui.row():
    with ui.column():
        ui.label("Audio: Sound Helix")
        a = ui.video(url_audio)
        with ui.row():
            ui.button('Play', on_click=lambda: a.play())
            ui.button('Pause', on_click=lambda: a.pause())
            ui.button('Seek', on_click=lambda: a.seek(seek_to_audio))
            ui.number("Position", value=seek_to_audio).bind_value(globals(), 'seek_to_audio')

    with ui.column():
        ui.label("Video: Big Buck Bunny")
        v = ui.video(url_video)
        with ui.row():
            ui.button('Play', on_click=lambda: v.play())
            ui.button('Pause', on_click=lambda: v.pause())
            ui.button('Seek', on_click=lambda: v.seek(seek_to_video))
            ui.number("Position", value=seek_to_video).bind_value(globals(), 'seek_to_video')

ui.run()