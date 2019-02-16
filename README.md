<h3 align="center">
  Dotup
</h3>
<h5 align="center">
  <i>Symlink your dotfiles with ease.</i>
</h5>

---

Dotup will generate symlinks to your dotfiles and place them in your home directory through a convenient CLI.

### Install

```shell
$ pip install dotup
```

### Usage

By default, _dotup_ expects to find a directory called `dotfiles` in your home directory (`~/dotfiles`).

```shell
$ dotup
# specify different dotfiles directory location at ~/dots
$ dotup --directory dots
```

To force symlink creation you can pass the `-f`, or `--force` flag.

```shell
$ dotup --force
```

Help

```shell
$ dotup --help
```

### Development

Pull requests are welcome, please consider creating an issue first about the change you would like to make.

### Deploy

To deploy a new version:

1. Make a semantic version update to `dotup/__init__.py` and `pyproject.toml` files.
2. Run `poetry-setup` see [poetry-setup](https://github.com/orsinium/poetry-setup) for installation
3. Commit updated versions
4. Run `poetry build`
5. Run `poetry publish`
