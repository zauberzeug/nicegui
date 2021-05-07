import justpy as jp

def hello_world():
    wp = jp.WebPage()
    jp.Hello(a=wp)
    return wp

app = jp.app
jp.justpy(hello_world, start_server=False)