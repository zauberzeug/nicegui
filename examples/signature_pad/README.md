# Use Node Modules as Third-party Dependencies

This example demonstrates how to use third-party node modules as dependencies in a NiceGUI app.
The app uses the [signature_pad](https://www.npmjs.com/package/signature_pad) node module to create a signature pad.
In package.json, the signature_pad module is listed as a dependency,
while signature_pad.js and signature_pad.py define the new UI element which can be used in main.py.

1. First, install the third-party node modules (assuming you have NPM installed):

   ```bash
   npm install
   ```

   This will create a node_modules directory containing the signature_pad module.

2. Now you can run the app as usual:

   ```bash
   python3 main.py
   ```
