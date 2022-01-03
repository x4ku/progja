# Contributing Instructions

Instructions for contributing to this project.

## Setup

This project requires Python 3, `pip`, and `virtualenv`.

You can install `virtualenv` with `pip`:
```sh
$ pip install virtualenv
```

### Virtual Environment

Source the provided `bin/venv` script in your shell to set up a virtual
environment for this project, install dependencies, and activate the virtual
environment:
```sh
$ . bin/venv
```

Install the development dependencies as well:
```sh
$ pip install -r requirements-dev.txt
```

> To deactivate the virtual environment in the future:
> ```
> $ deactivate
> ```

### Sandbox

Anything placed in the `sandbox/` directory of this project will be ignored by
version control. You can place your own notebooks, scripts, and other files in
this directory.

### Jupyter

`jupyter` and `pandas` are both available if you would like to use them to work
on this project.

In order to use packages installed in the virtual environment with Jupyter,
you'll have to create a new ipython kernel for the project. The following
command should create this kernel for you:
```sh
$ python -m ipykernel install --user --name progja
```

> If you would like to uninstall this kernel in the future, you can do so with
> the following command:
> ```sh
> $ jupyter kernelspec uninstall progja
> ```

You can start a jupyter notebook server with the following command:
```sh
$ jupyter notebook
```

After starting the server, the web app should be available at:
http://localhost:8888.

Feel free to create your own notebooks in the `sandbox/` directory. Make sure
you have the `progja` kernel selected (Kernel > Change kernel) or you will not
be able to import the packages installed to the virtual environment.

### Google Text-to-Speech API

> Note: We are not currently generating and distributing audio files, but we may
> do so in the future. We'll just keep these instructions here for now.

Audio files are generated using the Google Cloud Text-to-Speech API. In order to
generate audio, you will need to have a Google Cloud account and a credentials
file. Set the path to your credentials file in the
`GOOGLE_APPLICATION_CREDENTIALS` environment variable. See the link below for
more information.

https://cloud.google.com/docs/authentication/getting-started

If you would like to use these credentials in a Jupyter notebook, you'll have
to pass the environment variable when you start the notebook server:
```sh
env GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS jupyter notebook
```

In a Jupyter notebook, you can print out the current environment variables to
verify that they are set properly by running the `%env` command. Note that if
you change the environment variable value, you'll have to restart the notebook
server.

## Development

Make sure your virtual environment is activated.

### Build Script

The entire pipeline can be executed using the `bin/build` script.
```sh
$ bin/build
```

You can skip individual steps using the `--skip` flag.
```sh
$ bin/build --skip download,convert
```

See the `bin/build` script for more information.

### Unit Tests

You can run unit tests using the `unittest` module.
```sh
$ python -m unittest -v
```

You can also run specific tests:
```sh
$ python -m unittest -v tests.test_kanji
$ python -m unittest -v tests.test_kanji.TestKanjiCompositions
```

## Anki Decks

You will first need to build the project and generate the deck import files for
each path level. You should have `deck-level-*.csv` files within the
`progja/data` directory before proceeding with the steps below.

**Warning**: Please make sure you back up your Anki profile before importing a
deck in order to avoid potential data loss or corruption. It might also be a
good idea to use a separate Anki profile for this.

Create a new note type for the cards in this project.
1. Go to `Tools` > `Manage Note Types`
2. Click `Add`
    1. Clone the "Basic" note type
    2. Name it "Progressive Japanese Note"
    3. Click `OK`
3. With the new note type selected, click `Fields...`
4. Click `Add`
    1. Name the field "ID"
    2. Click-and-drag the new field to the first position in the field list
    3. Click `Save`
5. With the new note type selected, click `Cards...`
6. Click `Styling`
    1. Copy the contents of `progja/data/deck-style.css`
    2. Paste the contents into the text area
    3. Click `Save`
7. Close the note type manager

Create a parent deck called "Progressive Japanese". The decks created/imported
by the steps below should be placed under this parent deck.

Import each deck (the steps for level 1 are shown below):
1. Click `Create Deck` in the main Anki interface
    1. Name it "Progressive Japanese (Lv. 1)"
    2. Click `OK`
2. Click `Import File`
    1. Locate the `progja/data/deck-level-1.csv` file
    2. Click `Open`
    3. Select the "Progressive Japanese Note" note type
    4. Select the "Progressive Japanese (Lv. 1)" deck
    5. Select `Update existing notes when first field matches`
    6. Select `Allow HTML in fields`
    7. Ensure the fields are in the correct order (`ID`, `Front`, `Back`)
        - Field 4 should be mapped to `Tags`
    8. Click `Import`
3. Repeat the above steps for each deck level

## Packaging

This project is packaged using `setuptools` and PyPA build.

### Test the Installation

Test the package installation with `pip`:
```sh
$ pip install .
```

You should see that the package is installed:
```sh
$ pip freeze | grep progja
progja @ file:///.../progja
```

> To upgrade the package:
> ```sh
> $ pip install --upgrade .
> ```
>
> To remove the package:
> ```sh
> $ pip uninstall progja
> ```
>
> You can also install the package in "editable" mode while testing:
> ```sh
> $ pip install --editable .
> ```

### Build a Distribution

Invoke PyPA build to build a distribution:
```sh
$ python -m build
```

This will create a wheel and a `.tar.gz` distribution in the `dist/` directory.

### Upload to TestPyPI

```sh
$ twine upload -r testpypi dist/*
```

Install and test the package from TestPyPI:
```sh
$ pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  progja
```

See https://twine.readthedocs.io for more information.

### Upload to PyPI

**Warning**: Please make sure to upload and test with TestPyPI before uploading
to PyPI. You can only upload a single package per version in PyPI.

```sh
$ twine upload dist/*
```

Install and test the package from PyPI:
```sh
$ pip install progja
```
