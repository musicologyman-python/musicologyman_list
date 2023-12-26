#!/usr/bin/env python3

from argparse import ArgumentParser
from collections.abc import Iterable
from itertools import groupby
from pathlib import Path

from colorama import Fore, Back, Style
from icecream import ic

def list_dirs(root: Path, recurse: bool=False, leader=' '):
    for p in sorted((p for p in root.iterdir() 
                     if p.is_dir() and not p.is_symlink()), 
                    key=lambda p:p.name.lower()):
        print(Fore.MAGENTA + Style.BRIGHT + leader + str(p))
        if recurse:
            list_dirs(p, recurse=recurse, leader=leader)

def get_files(root: Path, recurse: bool=True):
    yield from sorted((p for p in root.iterdir() 
                       if p.is_file() and not p.is_symlink()), 
                       key=lambda p:p.name.lower())
    if recurse:
        for p in root.iterdir():
            if p.is_dir() and not p.is_symlink():
                yield from get_files(p)
    

def by_suffix(files: Iterable[Path], relative_to: Path):
    sort_key = lambda p: (p.suffix.lower(), str(p).lower())
    sorted_by_suffix = sorted(files, 
                              key=lambda p: (p.suffix.lower(), str(p).lower()))
    for suffix, files in groupby(sorted_by_suffix, key=lambda p: p.suffix):
        if suffix:
            print(Fore.CYAN + Style.BRIGHT + suffix)
        else:
            print(Fore.CYAN + Style.BRIGHT + '(no suffix)')
        for p in files:
            print(Fore.YELLOW + Style.NORMAL + 
                  f'    {str(p.relative_to(relative_to))}')

def list_suffixes(files: Iterable[Path]):
    suffixes = sorted(set((p.suffix for p in files if p.suffix)), 
                      key=str.lower)
    for suffix in suffixes:
        print(Fore.MAGENTA + Style.NORMAL + suffix)

def setup():
    parser = ArgumentParser()
    parser.add_argument('root', type=Path, default=Path('.'), nargs='?')
    parser.add_argument('--recurse', '-r', action='store_true')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--dirs-only', '-d', action='store_true')
    group.add_argument('--by-suffix', '-x', action='store_true')
    group.add_argument('--suffixes', action='store_true')
    return parser.parse_args()

def main():
    args = setup()

    files = get_files(args.root, recurse=args.recurse)
    if args.by_suffix:
        by_suffix(files, relative_to=args.root)
    elif args.suffixes:
        list_suffixes(files)
    elif args.dirs_only:
        list_dirs(args.root, recurse=args.recurse)
    else:
        for p in files:
            print(' ' + Fore.YELLOW + Style.NORMAL + str(p))
    ic(args)

if __name__ == '__main__':
    main()
