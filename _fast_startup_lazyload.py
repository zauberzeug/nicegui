import time
from typing import TYPE_CHECKING

start = time.time()
if TYPE_CHECKING:
    import nicegui
else:
    from tf_lazy_loader import dynamic_import
    nicegui = dynamic_import('nicegui')

if __name__ == '__main__':
    nicegui.ui.textarea('Hello!')
    nicegui.ui.run(
        reload=False,
        show=False,
        native=True,
    )
print(time.time() - start)
