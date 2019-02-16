__version__ = '0.2.1'

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


def get_dotfiles(home):
    dirlist = map(
        lambda filename: f'{home}/dotfiles/{filename}', os.listdir(f'{home}/dotfiles')
    )
    dotfiles_paths = filter(os.path.isfile, dirlist)
    dotfiles = map(lambda path: path.replace(f'{home}/dotfiles/', ''), dotfiles_paths)
    return dotfiles


@click.command()
@click.option(
    '--force', '-f', default=False, help="Overwrite existing symlinks.", type=bool
)
def dotup(force):
    home = str(Path.home())
    non_dotfiles = []
    dotfiles = get_dotfiles(home)
    for filename in dotfiles:
        if filename[0] != '.':
            non_dotfiles.append(filename)
            continue

        success = update_symlink(filename, force)
        if success:
            print(f'Symlinked {crayons.red(filename)}@ -> {home}/dotfiles/{filename}')
        else:
            prompt_remove = input(
                f'\nFile already exists at {crayons.yellow(f"{home}/{filename}")}, overwrite it? [y/n] '
            )
            if prompt_remove == 'y':
                update_symlink(filename, True)
                print(
                    f'Symlinked {crayons.red(filename)}@ -> {home}/dotfiles/{filename}'
                )
            else:
                print(f'{crayons.magenta("Skipping")} {filename}')

    for filename in non_dotfiles:
        print(
            f'\n{crayons.magenta("Skipped")} {crayons.yellow(f"{home}/{filename}")},',
            f'filename does not begin with \033[4m{crayons.cyan(".")}\033[0m',
        )


if __name__ == "__main__":
    dotup()
