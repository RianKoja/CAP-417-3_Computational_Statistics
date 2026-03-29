# Set Up

Based initially on https://github.com/osintalex/pyo3-example


## Original readme:
Make sure you install [rust](https://www.rust-lang.org/tools/install),
[pyenv](https://github.com/pyenv/pyenv#installation), and
[pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv#installation).

You don't have to use `pyenv` and `pyenv-virtualenv` - pretty much any
python and virtual environment manager is compatible if you want to use
those instead.

```shell
# can be any python version supported by maturin
# I just put 3.10.0 since I like 3.10
pyenv virtualenv 3.10.0 ejemplo
pyenv activate ejemplo
pip install maturin pytest
maturin develop
```

Then you should be able to run Python like so in the created virtual environment:

```python
from ejemplo import check_limit

flag: bool = check_limit(3)
print(flag)
```

You can also run python tests with `pytest` after running maturin develop, which
will build a new version of the library and install it into the active
virtual environment.

To edit the type annotations and docstrings on the modules you are exposing in
Python, you need to change what is in the `ejemplo.pyi` file.

## Debugging in Rust

You can run code in the `src/main.rs` file by running `cargo run`.
However, you first, have to change the `Cargo.toml` entry of `lib.crate-type` to
`lib`.

This file will not be distributed as part of the python package; it only exists
to provide a Rust executable for debugging your library logic in Rust.

You can read more on how to do this 
[here](https://code.visualstudio.com/docs/languages/rust#_debugging); this is a 
sample debug configuration:

```JSON
{
    "name": "Debug ejemplo",
    "type": "lldb",
    "request": "launch",
    "program": "${workspaceRoot}/target/debug/${workspaceRootFolderName}",
    "args": [],
    "cwd": "${workspaceRoot}",
    "sourceLanguages": [
        "rust"
    ]
}
```

## Pyo3 Usage

See [here](https://pyo3.rs/v0.20.2/) for how to write Python in Rust with Pyo3.
