# Automated Tests for NiceGUI

## Motivation

Testing a user interface is hard work.
But to ensure NiceGUI is working as expected it is of utmost importance.
Even if automated testing needs a lot of infrastructure and results in long execution times, we believe that it's worth the effort when compared to manual testing.

## Setup

Usually you don't need to install ChromeDriver at all.
The `selenium` test dependency comes with a helper called Selenium Manager that downloads a matching Chrome and ChromeDriver for you the first time the tests run.
Our tests use this helper first, so on most systems installing the test dependencies is enough.

You only need to install a browser and driver by hand in two cases: on ARM machines other than Apple Silicon Macs (like a Raspberry Pi or an ARM dev container), where the helper has nothing to download, or when you'd rather use a browser that your system installed.
If you do install ChromeDriver yourself, make sure its version matches your Chrome or Chromium — otherwise the tests won't start.
If the browser isn't picked up automatically, point the tests at it with the `CHROME_BINARY_LOCATION` environment variable (our dev container sets it to `/usr/bin/chromium`).
Likewise, the `SE_CHROMEDRIVER` environment variable points Selenium at a specific ChromeDriver and takes precedence over anything the tests would try on their own.

### Mac

Selenium Manager works on all Macs, so you don't need to install anything.

Do not use the Homebrew cask `chromedriver`: it is disabled and no longer updated.
A driver in your `PATH` takes precedence over Selenium Manager, so an outdated one makes the tests fail with "Could not start Chrome WebDriver".
If you have it installed, remove it:

```bash
brew uninstall --cask chromedriver
```

### Windows

```powershell
choco install chromedriver
```

Note: The above instructions assume that you have already installed Chocolatey (a package manager for Windows) on your system.
If you haven't, you can follow the instructions on https://chocolatey.org/install to install it.

### Linux

For Debian:

```bash
sudo apt-get update
sudo apt-get install chromium-driver
```

On Ubuntu, both `chromium-chromedriver` and `chromium-driver` resolve to the same transitional stub that pulls in the Chromium snap, which is a dead end in containers, WSL, and minimal CI images.
Prefer Selenium Manager (see above), or install a matching ChromeDriver manually.
If Chromium is already installed as a snap, as it is on Ubuntu desktop, see [Snap-based Chromium](#snap-based-chromium) below.

For Arch-based Linux distribution:

```bash
sudo pacman -S chromium
```

If you are using a different distribution, the package manager and package names may differ.
Please refer to the documentation for your distribution for more information.

#### Snap-based Chromium

Selenium Manager finds the snap's Chromium but downloads an upstream ChromeDriver that cannot launch the snap-confined browser, so the tests hang indefinitely.
Use the ChromeDriver shipped with the snap instead and leave `CHROME_BINARY_LOCATION` unset, so that the driver starts its own Chromium:

```bash
export SE_CHROMEDRIVER=/snap/bin/chromium.chromedriver
```

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
