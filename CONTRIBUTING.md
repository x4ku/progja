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

### flake8

You can use `flake8` to check for code style and quality issues:
```sh
$ flake8 progja
$ flake8 pipeline/*
```

## Releases

To release a new version of this project, the project should be packaged and
uploaded to PyPI, the Anki decks should be updated and shared, a git tag should
be created, and the version number should be bumped to the next version.

1. [Package the Project](#package-the-project)
2. [Upload to TestPyPI](#upload-to-testpypi)
3. [Upload to PyPI](#upload-to-pypi)
4. [Update the Anki Decks](#update-the-anki-decks)
5. [Create a Git Tag](#create-a-git-tag)
6. [Bump the Version Number](#bump-the-version-number)

### Package the Project

This project is packaged using `setuptools` and PyPA build.

Invoke PyPA build to build a distribution:
```sh
$ python -m build
```

This will create a wheel and a `.tar.gz` distribution in the `dist/` directory.

Try out this distribution separately as a sanity check. You could do this from a
fresh virtual environment in the `sandbox/` directory, for example.
```sh
$ cd sandbox
$ virtualenv venv
$ . venv/bin/activate
$ pip install ../dist/progja-<version>.tar.gz
$ pip install ipython
```
```sh
$ ipython
In [1]: import progja

In [2]: progja.kanji.load()
...

# (etc)
```

### Upload to TestPyPI

```sh
$ twine upload -r testpypi dist/*
```

> See https://twine.readthedocs.io for more information.

Install and test the package from TestPyPI as a sanity check:
```sh
$ pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  progja
```

### Upload to PyPI

**Warning**: Please make sure to upload and test with TestPyPI before uploading
to PyPI. You can only upload a single file per version in PyPI.

```sh
$ twine upload dist/*
```

> See https://twine.readthedocs.io for more information.

Install and test the package from PyPI as a final check:
```sh
$ pip install progja
```

### Update the Anki Decks

**Warning**: Please make sure you back up your Anki profile before proceeding in
order to avoid potential data loss or corruption. It is also recommended that
you perform this step from a separate Anki profile.

Make sure you have the latest version of each deck installed. Import each data
file using the steps below:

1. Click `Import File`
2. Locate the `progja/data/cards/cards-level-<level>.csv` file and click `Open`
3. Select the "Progressive Japanese Note" note type
4. Select the "Progressive Japanese (Lv. <level>)" deck
5. Select `Update existing notes when first field matches`
6. Select `Allow HTML in fields`
7. Ensure the fields are in the correct order (`ID`, `Front`, `Back`)
    - Field 4 should be mapped to `Tags`
8. Click `Import`

Remove all cards from the decks that are not tagged with the latest version
(search for `-tag:progja::version::<version>`).

Make sure to update the CSS for the "Progressive Japanese Note" note type if the
styling has changed.

Sync the decks with AnkiWeb and then share the updated decks from the AnkiWeb.
<br>
https://ankiweb.net/

### Create a Git Tag

Tag the commit with the current version:
```sh
$ git tag <version>
```

Push the tag:
```sh
$ git push origin <version>
```

### Bump the Version Number

Bump the version number in `progja/__init__.py`, commit the change, and push the
commit. Bumping the version number is the last step in the relase process.
