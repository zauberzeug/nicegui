from nicegui import ui

"""
More advanced example using all the slots and properties of the splitter
including a tooltip, a custom separator, and a callback.

Known Issues: Horizontal splitting `horizontal=False` displays OK visually but
the movement of the splitter is not working.
"""

lhs = """
Optio voluptate et nihil ex voluptatem hic magnam inventore tempore nihil et nihil ut reiciendis. Omnis fugit voluptas in sunt magnam in vel occaecati consequatur non dolorem ducimus. Eligendi cum aut dicta magni qui quia. Quisquam sed et qui modi maxime. Exercitationem fugiat qui cum soluta eum ut aperiam perspiciatis maiores enim porro rerum.
Iure doloremque molestiae harum sapiente corrupti dolores omnis quaerat pariatur occaecati odio praesentium provident corrupti. Et ipsa qui velit aliquid delectus non. Aperiam aut veritatis ullam at nulla omnis a quidem enim dolorum quod temporibus sed sed. Ea ut consequuntur ipsam sunt unde est est quia deleniti amet et.
Ex dolorem non pariatur cupiditate aliquid ipsam voluptatem doloremque voluptate. Repellendus sed ut deleniti non quo provident ducimus et. Molestiae velit earum nisi beatae consequatur amet sint quo occaecati pariatur ipsa et reprehenderit. Dolore reiciendis molestiae dolor laborum minus quisquam quia reiciendis officia id porro omnis reprehenderit excepturi aspernatur. Et ea rerum alias perspiciatis est sequi commodi nisi. In sit magni neque ex quibusdam et dolorem cumque tempore et quasi ut aspernatur.
"""
rhs = """
Ipsum et quidem repudiandae hic ut soluta qui odit qui qui ad possimus. Est dolores saepe maxime omnis sed voluptatibus consequuntur aperiam sed iste. Non accusamus saepe sunt atque libero iure sed neque autem dicta omnis dolorem. Culpa maiores ad omnis magnam non sunt non.
Eveniet aliquid quas harum iusto aut eum mollitia deserunt sint recusandae reprehenderit corrupti qui. Nobis quia eos iusto odio et repellat. Ea dolores qui ducimus neque et ut facere inventore aut dicta suscipit nobis est id. Illo omnis nemo ut voluptas quis sit neque. Soluta omnis ea quo accusamus culpa a est ipsa accusantium quia error incidunt dolores blanditiis.
"""

with ui.splitter(horizontal=False, reverse=False, value=60, on_change=lambda e: ui.notify(e.value)) as splitter:
    ui.tooltip('Please drag left and right').classes('bg-green')  # default slot contents (optional)
    with splitter.add_slot('before'):
        ui.label(lhs)
    with splitter.add_slot('after'):
        ui.label(rhs)
    with splitter.add_slot('separator'):  # separator slot contents (optional)
        ui.icon('lightbulb').classes('text-green')

ui.label().bind_text_from(splitter, 'value')

ui.run(dark=True)
