#!/usr/local/bin/python3

import sys
import os
import pwd
from pathlib import Path

import click
import crayons


def update_symlink(source, dest, force=None):
    force = False if force is None else force

@click.command('dotup')
@click.option('--force', '-f', default=False, help="Overwrite existing symlinks.", type=bool)
def update_symlinks(force):
    print(force)
    return
    username = pwd.getpwuid(os.getuid()).pw_name
    skipped = []
    home = str(Path.home())
    for filename in os.listdir(f'{home}/dotfiles'):
        if filename[0] != '.':
            skipped.append(filename)
            continue
        try:
            os.symlink(f'{home}/dotfiles/{filename}', f'{home}/{filename}')
            print(f'Symlinked {crayons.red(filename)}@ -> {home}/dotfiles/{filename}')
        except FileExistsError:
            if force:
            force_remove = input(f'File already exists at {crayons.yellow(f"{home}/{filename}")}, overwrite it? [y/n] ')
            if force_remove == 'y':
                os.remove(f'{home}/{filename}')
                os.symlink(f'{home}/dotfiles/{filename}', f'{home}/{filename}')
                print(f'Symlinked {crayons.red(filename)}@ -> {home}/dotfiles/{filename}')
            else:
                print(f'{crayons.magenta("Skipping")} {filename}')
    for filename in skipped:
        print(f'\n{crayons.magenta("Skipped")} {crayons.yellow(f"{home}/{filename}")}, filename does not begin with \033[4m{crayons.cyan(".")}\033[0m')

if __name__ == "__main__":
    update_symlinks()
