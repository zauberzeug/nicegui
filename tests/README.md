# Automated Tests for NiceGUI

## Motivation

Testing a user interface is hard work.
But to ensure NiceGUI is working as expected it is of utmost importance.
Even if automated testing needs a lot of infrastructure and results in long execution times, we believe that it's worth the effort when compared to manual testing.

## Setup

Please be aware that the below commands install the latest version of the ChromeDriver binary, which is compatible with the version of Google Chrome installed on your system.
If you have a different version of Chrome installed, you may need to install a different version of ChromeDriver or update your Chrome installation to be compatible with the installed ChromeDriver version.

### Mac

```bash
brew install cask chromedriver
```

Note: The above instructions assume that you have already installed Homebrew (a package manager for macOS) on your system.
If you haven't, you can follow the instructions on https://brew.sh/ to install it.

### Windows

```powershell
choco install chromedriver
```

Note: The above instructions assume that you have already installed Chocolatey (a package manager for Windows) on your system.
If you haven't, you can follow the instructions on https://chocolatey.org/install to install it.

### Linux

```bash
sudo apt-get update
sudo apt-get install chromium-chromedriver
```

Note: The above instructions assume that you are using a Debian-based Linux distribution.
If you are using a different distribution, the package manager and package names may differ.
Please refer to the documentation for your distribution for more information.

## Usage

Because Selenium queries are quite cumbersome and lengthy, we introduced a `Screen` class.
This provides a high-level interface to work with the currently displayed state of the web browser.
The workflow is as follows:

1. Get the `screen` fixture by providing `screen: Screen` as an argument to the function.
2. Write your NiceGUI code inside the function.
3. Use `screen.open(...)` with the appropriate URL path to start querying the website.
4. For example, use `screen.should_contain(...)` with some text as parameter to ensure that the text is shown.

Here is a very simple example:

```py
from nicegui import ui
from nicegui.testing import Screen

def test_hello_world(screen: Screen):
    ui.label('Hello, world')

    screen.open('/')
    screen.should_contain('Hello, world')
```

Have a look at the existing tests for more examples.
Internally we use selenium-fixture (see `conftest.py`).
To access the webdriver directly you can use the `screen.selenium` property.
Have a look at https://selenium-python.readthedocs.io/getting-started.html for documentation of the available method calls to the webdriver.

## SharedScreen vs Screen

For faster test execution, most tests use `SharedScreen` instead of `Screen`. SharedScreen reuses a single server across multiple tests, avoiding the overhead of starting/stopping the server for each test.

### When to use SharedScreen

Use `SharedScreen` for tests that:
- Only define UI pages and interact with them via the browser
- Don't require custom server configuration
- Don't use lifecycle handlers

```py
from nicegui import ui
from nicegui.testing import SharedScreen

def test_hello_world(shared_screen: SharedScreen):
    @ui.page('/')
    def page():
        ui.label('Hello, world')

    shared_screen.open('/')
    shared_screen.should_contain('Hello, world')
```

### When to use Screen

Use the regular `Screen` fixture for tests that:
- Modify `ui_run_kwargs` (e.g., `storage_secret`, `favicon`, `prod_js`, `root`)
- Use `@pytest.mark.nicegui_main_file`
- Use lifecycle handlers (`app.on_startup()`, `app.on_shutdown()`, `app.shutdown()`)
- Directly manipulate `Server.instance`

```py
from nicegui import ui
from nicegui.testing import Screen

def test_with_storage(screen: Screen):
    screen.ui_run_kwargs['storage_secret'] = 'test_secret'
    # ... test code
```

### Mixing SharedScreen with User fixture

`SharedScreen` and `User` fixtures can be freely mixed in the same pytest session. SharedScreen automatically detects when the event loop has been reset (e.g., by a previous User test) and recovers by restarting the shared server.

This means you can run all tests together:

```bash
pytest tests/
```
