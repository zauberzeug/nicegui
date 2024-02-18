# Contributing to NiceGUI

We're thrilled that you're interested in contributing to NiceGUI!
Here are some guidelines that will help you get started.

## Reporting issues

If you encounter a bug or other issue with NiceGUI, the best way to report it is by opening a new issue on our [GitHub repository](https://github.com/zauberzeug/nicegui).
When creating the issue, please provide a clear and concise description of the problem, including any relevant error messages and code snippets.
If possible, include steps to reproduce the issue.

## Code of Conduct

We follow a [Code of Conduct](https://github.com/zauberzeug/nicegui/blob/main/CODE_OF_CONDUCT.md) to ensure that everyone who participates in the NiceGUI community feels welcome and safe.
By participating, you agree to abide by its terms.

## Contributing code

We are excited that you want to contribute code to NiceGUI.
We're always looking for bug fixes, performance improvements, and new features.

## Setup

### Dev Container

The simplest way to setup a fully functioning development environment is to start our Dev Container in VS Code:

1. Ensure you have VS Code, Docker and the Remote-Containers extension installed.
2. Open the project root directory in VS Code.
3. Press `F1`, type `Remote-Containers: Open Folder in Container`, and hit enter (or use the bottom-left corner icon in VS Code to reopen in container).
4. Wait until image has been build.
5. Happy coding.

### Locally

To set up a local development environment for NiceGUI, you'll need to have Python 3.8+ and pip installed.

You can then use the following command to install NiceGUI in editable mode:

```bash
python3 -m pip install -e .
```

This will install the `nicegui` package and all its dependencies, and link it to your local development environment so that changes you make to the code will be immediately reflected.
Thereby enabling you to use your local version of NiceGUI in other projects.
To run the tests you need some additional setup which is described in [tests/README.md](https://github.com/zauberzeug/nicegui/blob/main/tests/README.md).

There is no special Python version required for development.
At Zauberzeug we mainly use 3.11.
This means we sometimes miss some incompatibilities with older versions.
But these will hopefully be uncovered by the GitHub Actions (see below).
Also we use the 3.8 Docker container described below to verify compatibility in cases of uncertainty.

### Plain Docker

You can also use Docker for development by starting the development container using the command:

```bash
./docker.sh up app
```

By default, the development server listens to http://localhost:80/.

The configuration is written in the `docker-compose.yml` file and automatically loads the `main.py` which contains the website https://nicegui.io.
Every code change will result in reloading the content.
We use Python 3.8 as a base to ensure compatibility (see `development.dockerfile`).

To view the log output, use the command

```bash
./docker.sh log
```

## Coding Style Guide

### Formatting

We use [autopep8](https://github.com/hhatto/autopep8) with a 120 character line length to format our code.
Before submitting a pull request, please run

```bash
autopep8 --max-line-length=120 --experimental  --in-place --recursive .
```

on your code to ensure that it meets our formatting guidelines.
Alternatively you can use VSCode, open the nicegui.code-workspace file and install the recommended extensions.
Then the formatting rules are applied whenever you save a file.

### Imports

We use `isort` to automatically sort imports.

### Single vs Double Quotes

Regarding single or double quotes: [PEP 8](https://peps.python.org/pep-0008/) doesn't give any recommendation, so we simply chose single quotes and sticked with it.
On qwerty keyboards it's a bit easier to type, is visually less cluttered, and it works well for strings containing double quotes from the English language.

### F-Strings

We use f-strings where ever possible because they are generally more readable - once you get used to them.
There are only a few places in the code base where performance really matters and f-strings might not be the best choice.
These places should be marked with a `# NOTE: ...` comment when diverging from f-string usage.

## Running tests

Our tests are built with pytest and require python-selenium with ChromeDriver.
See [tests/README.md](https://github.com/zauberzeug/nicegui/blob/main/tests/README.md) for detailed installation instructions and more infos about the test infrastructure and tricks for daily usage.

Before submitting a pull request, please make sure that all tests are passing.
To run them all, use the following command in the root directory of NiceGUI:

```bash
pytest
```

## Documentation

### New Elements

If you plan to implement a new element you can follow these suggestions:

1. Ensure with the maintainers that the element is a good fit for NiceGUI core;
   otherwise it may be better to create a separate git repository for it.
2. Clone the NiceGUI repository and launch `main.py` in the root directory.
3. Run `python3 -m pip install -e .` in the repository as explained above.
4. Create a `test.py` file or similar where you can experiment with your new element.
5. Look at other similar elements and how they are implemented in `nicegui/elements`.
6. Create a new file with your new element alongside the existing ones.
7. Make sure your element works as expected.
8. Add a documentation file in `website/documentation/content`.
   By calling the `@doc.demo(...)` function with an element as a parameter the docstring is used as a description.
   The docstrings are written in restructured-text.
   Refer to the new documentation page using `@doc.intro(...)` in any documentation section `website/documentation/content/section_*.py`.
9. Create a pull-request (see below).

### Additional Demos

There is a separate page for each element where multiple interactive demos can be listed.
Please help us grow the number of insightful demos by following these easy steps:

1. Clone the NiceGUI repository and launch `main.py` in the root directory.
2. Run `python3 -m pip install -e .` in the repository as explained above.
3. In the newly opened browser window you can navigate to the documentation page where you want to change something.
4. Open the code in your editor (for example [website/more_documentation/table_documentation.py](https://github.com/zauberzeug/nicegui/blob/main/website/more_documentation/table_documentation.py)).
5. In the `more()` function insert an inner function containing your demo code.
6. Add the `@text_demo` decorator to explain the demo.
7. Make sure the result looks as expected in the rendered documentation.
8. Create a pull-request (see below).

Your contributions are much appreciated.

### Formatting

Because it has [numerous benefits](https://nick.groenen.me/notes/one-sentence-per-line/) we write each sentence in a new line.

### Examples

Besides the documentation with interactive demos (see above) we collect useful, compact stand-alone examples.
Each example should be about one concept.
Please try to make them as minimal as possible to show what is needed to get some kind of functionality.
We are happy to merge pull requests with new examples which show new concepts, ideas or interesting use cases.
To list your addition on the website itself, you can use the `example_link` function below the
["In-depth examples" section heading](https://github.com/zauberzeug/nicegui/blob/8a86d2064f8f4464f3819ac5c6763a2cb2d0e990/main.py#L242).
The title should match the example folder name when [snake case converted](https://github.com/zauberzeug/nicegui/blob/8a86d2064f8f4464f3819ac5c6763a2cb2d0e990/website/style.py#L31).

## Pull requests

To get started, fork the repository on GitHub, clone it somewhere on your filesystem, commit and push your changes,
and then open a pull request (PR) with a detailed description of the changes you've made
(the PR button is shown on the GitHub website of your forked repository).

When submitting a PR, please make sure that the code follows the existing coding style and that all tests are passing.
If you're adding a new feature, please include tests that cover the new functionality.

## YouTube

We welcome and support video and tutorial contributions to the NiceGUI community!
As recently [highlighted in a conversation on YouTube](https://www.youtube.com/watch?v=HiNNe4Q32U4&lc=UgyRcZCOZ9i5z6GuDcJ4AaABAg),
creating and sharing tutorials or showcasing projects using NiceGUI can be an excellent way to help others learn and grow,
while also spreading the word about our library.

Please note that NiceGUI is pronounced like "nice guy," which might be helpful to know when creating any video content.

If you decide to create YouTube content around NiceGUI,
we kindly ask that you credit our repository, our YouTube channel, and any relevant videos or resources within the description.
By doing so, you'll be contributing to the growth of our community and helping us receive more amazing pull requests and feature suggestions.

We're thrilled to see your creations and look forward to watching your videos. Happy video-making!

## Thank you!

Thank you for your interest in contributing to NiceGUI!
We're looking forward to working with you!
