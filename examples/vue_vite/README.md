# Custom SFC Vue Component using Vite

This example demonstrates how to build Single-File Component (SFC) Vue components with Vite in NiceGUI.
Using Vite rather than NiceGUI's vbuild based build step currently supports more features of the SFC spec.
It might be useful to see also:

1. `custom_vue_component`: an examples of a custom Vue component without a build step
2. `signature_pad`: an example with a Rollup-based build step and Javascript dependency

There are two implementations of a counter components. `CounterOptions` is implemented using the options API, and `CounterComposition` uses the composition API. Both use Typescript and Vue's Single-File Component (SFC) syntax.

## Running

Run the demo with `python demo.py`. With this setup you could modify the Vue components and the changes would be reflected live if you also kept Vite's build-watch process running at the same time.

```bash
$ npm watch
```

Alternatively the components can be rebuilt with:

```bash
$ npm watch
```
