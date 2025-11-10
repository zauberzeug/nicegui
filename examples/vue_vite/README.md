# Custom SFC Vue Component using Vite

This example demonstrates how to build Single-File Component (SFC) Vue components with Vite in NiceGUI.
Using Vite rather than NiceGUI's vbuild based build step currently supports more features of the SFC spec.
It might be useful to see also:

1. `custom_vue_component`: an example of a custom Vue component without a build step
2. `signature_pad`: an example with a Rollup-based build step and Javascript dependency

There are two implementations of a counter component.
`CounterOptions` is implemented using the options API, and `CounterComposition` uses the composition API.
Both use TypeScript and Vue's Single-File Component (SFC) syntax.

## Usage

Run the example with `python demo.py`.

To enable building/rebuilding the components, install the npm dependencies with:

```bash
npm install
```

In order to have modifications to the Vue components be reflected live, you can run Vite's build-watch process in parallel with the NiceGUI server:

```bash
$ npm run watch &
$ python demo.py
```

Alternatively you can rebuild components manually with:

```bash
$ npm run build
```
