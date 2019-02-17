from pathlib import Path

import pytest
import click
from click.testing import CliRunner

from dotup import (
    __version__,
    get_dotfiles,
    check_dotfiles_directory_exists,
    update_symlink,
    dotup,
)

dotfile_names = [
    '.bashrc',
    '.bash_profile',
    '.zshrc',
    '.vimrc',
    '.gitconfig',
    'README.md',
]

CONTENT = u'test'

DOTFILES_DIR_NAME = 'dotfiles'


def test_version():
    assert __version__ == '0.3.1'


@pytest.fixture
def path_home_mock(tmp_path, monkeypatch):
    def mockreturn():
        return tmp_path

    monkeypatch.setattr(Path, 'home', mockreturn)


@pytest.fixture
def dotfiles_dir(tmp_path):
    def _dotfiles_dir(dirname=None):
        dirname = DOTFILES_DIR_NAME if dirname is None else dirname
        path = tmp_path / DOTFILES_DIR_NAME
        path.mkdir()
        return [path, DOTFILES_DIR_NAME]

    return _dotfiles_dir


@pytest.fixture
def create_dotfiles():
    def _create_dotfiles(path):
        for name in dotfile_names:
            f = path / name
            f.write_text(CONTENT)

    return _create_dotfiles


def test_update_symlink_successful_symlink(dotfiles_dir, path_home_mock):
    path, dir_name = dotfiles_dir()
    f = path / dotfile_names[0]
    f.write_text(CONTENT)

    assert update_symlink(dir_name, dotfile_names[0])


def test_update_symlink_unsuccessful_symlink_file_exists(
    dotfiles_dir, path_home_mock, tmp_path
):
    path, dir_name = dotfiles_dir()

    f = path / dotfile_names[1]
    f.write_text(CONTENT)

    f = tmp_path / dotfile_names[1]
    f.write_text(CONTENT)

    assert not update_symlink(dir_name, dotfile_names[1])


def test_update_symlink_successful_symlink_file_exists_force(
    dotfiles_dir, path_home_mock, tmp_path
):
    path, dir_name = dotfiles_dir()

    f = path / dotfile_names[1]
    f.write_text(CONTENT)

    f = tmp_path / dotfile_names[1]
    f.write_text(CONTENT)

    assert update_symlink(dir_name, dotfile_names[1], True)


def test_get_dotfiles(dotfiles_dir, create_dotfiles, tmp_path):
    path, dir_name = dotfiles_dir()
    create_dotfiles(path)

    dotfiles = get_dotfiles(tmp_path, dir_name)
    assert set(dotfiles) == set(dotfile_names)


def test_get_dotfiles_no_dirs(dotfiles_dir, create_dotfiles, tmp_path):
    path, dir_name = dotfiles_dir()
    create_dotfiles(path)

    sub_dir = path / 'subdir'
    sub_dir.mkdir()

    dotfiles = get_dotfiles(tmp_path, dir_name)
    assert 'subdir' not in set(dotfiles)


def test_check_dotfiles_directory_exists(dotfiles_dir, tmp_path):
    _, dir_name = dotfiles_dir()
    assert check_dotfiles_directory_exists(tmp_path, dir_name)
    assert not check_dotfiles_directory_exists(tmp_path, 'nonexistant-dir')


def test_dotup(dotfiles_dir, create_dotfiles, path_home_mock, tmp_path):
    path, dir_name = dotfiles_dir()
    create_dotfiles(path)

    runner = CliRunner()
    result = runner.invoke(dotup)
    assert result.exit_code == 0
    assert 'Skipped' in result.output
    assert 'Symlinked' in result.output

    f = tmp_path / dotfile_names[0]
    f.write_text(CONTENT)
    f = tmp_path / dotfile_names[1]
    f.write_text(CONTENT)
    result = runner.invoke(dotup, input='y\nn\n')
    assert result.exit_code == 0
    assert 'File already exists at' in result.output
    assert 'Skipped' in result.output
    assert 'Skipping' in result.output
    assert 'Symlinked' in result.output


def test_dotup_directory_doesnt_exist(tmp_path, path_home_mock):
    runner = CliRunner()
    result = runner.invoke(dotup, ['--directory', 'nonexistant-dir'])
    assert result.exit_code == 0
    assert 'Error: no dotfile directory found at' in result.output
    assert (
        'Use dotup --directory to specify your dotfile directory name' in result.output
    )
