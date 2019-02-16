__version__ = '0.3.1'

import sys
import os
import pwd
from pathlib import Path

import click
import crayons


def update_symlink(filename, force=None):
    force = False if force is None else force
    home = str(Path.home())
    try:
        os.symlink(f'{home}/dotfiles/{filename}', f'{home}/{filename}')
        return True
    except FileExistsError:
        if force:
            os.remove(f'{home}/{filename}')
            os.symlink(f'{home}/dotfiles/{filename}', f'{home}/{filename}')
            return True
    return False


def get_dotfiles(home, directory):
    dotfile_dirlist = map(
        lambda filename: f'{home}/{directory}/{filename}',
        os.listdir(f'{home}/{directory}'),
    )
    dotfiles_paths = filter(os.path.isfile, dotfile_dirlist)
    dotfiles = map(
        lambda path: path.replace(f'{home}/{directory}/', ''), dotfiles_paths
    )
    return dotfiles


def check_dotfiles_directory_exists(home, directory):
    return os.path.isdir(f'{home}/{directory}')


@click.command()
@click.option(
    '--directory',
    '-d',
    default="dotfiles",
    help="Dotfiles directory name. Must be located in home dir.",
)
@click.option('--force', is_flag=True, help="Overwrite existing symlinks.")
def dotup(directory, force):
    home = str(Path.home())

    exists = check_dotfiles_directory_exists(home, directory)
    if not exists:
        print(
            f'\nError: no dotfile directory found at {crayons.yellow(f"{home}/{directory}")}\n'
        )
        print(
            f'Use {crayons.cyan("dotup --directory")} to specify your dotfile directory name.'
        )
        return

    print(f'\nSymlinking dotfiles found in {crayons.cyan(f"{home}/{directory}")}\n')

    non_dotfiles = []
    dotfiles = get_dotfiles(home, directory)
    for filename in dotfiles:
        if filename[0] != '.':
            non_dotfiles.append(filename)
            continue

        success = update_symlink(filename, force)
        if success:
            print(
                f'Symlinked {crayons.red(filename)}@ -> {home}/{directory}/{filename}'
            )
        else:
            prompt_remove = input(
                f'\nFile already exists at {crayons.yellow(f"{home}/{filename}")}, overwrite it? [y/n] '
            )
            if prompt_remove == 'y':
                update_symlink(filename, True)
                print(
                    f'Symlinked {crayons.red(filename)}@ -> {home}/{directory}/{filename}'
                )
            else:
                print(f'{crayons.magenta("Skipping")} {filename}')

    for filename in non_dotfiles:
        print(
            f'\n{crayons.magenta("Skipped")} {crayons.yellow(f"{home}/{directory}/{filename}")}',
            f'-- filename does not begin with \033[4m{crayons.cyan(".")}\033[0m',
        )


if __name__ == "__main__":
    dotup()
