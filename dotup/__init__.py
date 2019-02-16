__version__ = '0.2.0'

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


@click.command()
@click.option(
    '--force', '-f', default=False, help="Overwrite existing symlinks.", type=bool
)
def dotup(force):
    non_dotfiles = []
    home = str(Path.home())
    for filename in filter(os.path.isfile, os.listdir(f'{home}/dotfiles')):
        if filename[0] != '.':
            non_dotfiles.append(filename)
            continue

        success = update_symlink(filename, force)
        if success:
            print(f'Symlinked {crayons.red(filename)}@ -> {home}/dotfiles/{filename}')
        else:
            prompt_remove = input(
                f'File already exists at {crayons.yellow(f"{home}/{filename}")}, overwrite it? [y/n] '
            )
            if prompt_remove == 'y':
                update_symlink(filename, True)
            else:
                print(f'{crayons.magenta("Skipping")} {filename}')

    for filename in non_dotfiles:
        print(
            f'\n{crayons.magenta("Skipped")} {crayons.yellow(f"{home}/{filename}")},',
            f'filename does not begin with \033[4m{crayons.cyan(".")}\033[0m',
        )


if __name__ == "__main__":
    dotup()
