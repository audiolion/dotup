from pathlib import Path

import pytest

from dotup import (
    __version__,
    get_dotfiles,
    check_dotfiles_directory_exists,
    update_symlink,
)

dotfile_names = ['bashrc', 'bash_profile', 'zshrc', 'vimrc', 'gitconfig']

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
