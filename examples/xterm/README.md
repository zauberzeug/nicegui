# Use Xterm.js as Third-party Dependency to run Bash

This example demonstrates how to use the [Xterm.js](https://github.com/xtermjs/xterm.js) node module as dependency in a
NiceGUI app. The app starts Bash in a pseudo-terminal (pty) and connects it to the Xterm.js element.

In package.json, the `@xterm/xterm` module is listed as a dependency, while `terminal.js` and `terminal.py` define the
new UI element which is then used in `main.py`.

To run this example:

1. First, install the third-party node modules (assuming you have NPM installed):

   ```bash
   npm install
   ```

   This will create a node_modules directory containing the `@xterm/xterm` module.
   To install `npm`, you can use a node version manager like [nvm](https://github.com/nvm-sh/nvm).

2. Now you can run the app as usual:

   ```bash
   python3 main.py
   ```

> [!WARNING] 
> This example gives the clients full access to the server through Bash. Use with caution!
