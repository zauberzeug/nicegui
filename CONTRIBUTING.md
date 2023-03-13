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

To set up a local development environment for NiceGUI, you'll need to have Python 3 and pip installed.

You can then use the following command to install NiceGUI in editable mode:

```bash
python3 -m pip install -e .
```

This will install the `nicegui` package and all its dependencies, and link it to your local development environment so that changes you make to the code will be immediately reflected.
Thereby enabling you to use your local version of NiceGUI in other projects.
To run the tests you need some additional setup which is described in [tests/README.md](https://github.com/zauberzeug/nicegui/blob/main/tests/README.md).

There is no special Python version required for development.
At Zauberzeug we mainly use 3.11.
This means we sometimes miss some incompatibilities with 3.7.
But these will hopefully be uncovered by the GitHub Actions (see below).
Also we use the 3.7 Docker container described below to verify compatibility in cases of uncertainty.

### Alternative: Docker

You can also use Docker for development.
Simply start the development container using the command:

```bash
./docker.sh up app
```

By default, the development server listens to http://localhost:80/.

The configuration is written in the `docker-compose.yml` file and automatically loads the `main.py` which contains the website https://nicegui.io.
Every code change will result in reloading the content.
We use Python 3.7 as a base to ensure compatibility (see `development.dockerfile`).

To view the log output, use the command

```bash
./docker.sh log
```

## Code formatting

We use [autopep8](https://github.com/hhatto/autopep8) with a 120 character line length to format our code.
Before submitting a pull request, please run

```bash
autopep8 --max-line-length=120 --experimental  --in-place --recursive .
```

on your code to ensure that it meets our formatting guidelines.
Alternatively you can use VSCode, open the nicegui.code-workspace file and install the recommended extensions.
Then the formatting rules are applied whenever you save a file.

## Running tests

Our tests are built with pytest and require python-selenium with ChromeDriver.
See [tests/README.md](https://github.com/zauberzeug/nicegui/blob/main/tests/README.md) for detailed installation instructions and more infos about the test infrastructure and tricks for daily usage.

Before submitting a pull request, please make sure that all tests are passing.
To run them all, use the following command in the root directory of NiceGUI:

```bash
pytest
```

## Documentation

New features should be well documented in [website/reference.py](https://github.com/zauberzeug/nicegui/blob/main/website/reference.py).
By calling the `example(...)` function with an element as a parameter the docstring is used as a description.
The docstrings are written in restructured-text.

Because it has [numerous benefits](https://nick.groenen.me/notes/one-sentence-per-line/) we write each sentence in a new line.

### Demos

Besides the documentation/reference (see above) we collect useful, but compact demonstrations.
Each demo should be about one concept.
Please try to make them as minimal as possible to show what is needed to get some kind of functionality.
We are happy to merge pull requests with new demos which show new concepts, ideas or interesting use cases.

## Pull requests

To get started, fork the repository on GitHub, make your changes, and open a pull request (PR) with a detailed description of the changes you've made.

When submitting a PR, please make sure that the code follows the existing coding style and that all tests are passing.
If you're adding a new feature, please include tests that cover the new functionality.

## Thank you!

Thank you for your interest in contributing to NiceGUI!
We're looking forward to working with you!
