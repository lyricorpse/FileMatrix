#!/usr/bin/env python3

import os
import shutil
import argparse
import colors

work_dir = os.path.dirname(os.path.realpath(__file__))
home_dir = os.getenv('HOME')
snippets_dir = os.path.join(home_dir, '.vim/bundle/snipmate.vim/snippets')
matrix = os.path.join(work_dir, 'matrix')

files = {
    'tmux': [home_dir, '.tmux.conf'],
    'vim': [home_dir, '.vimrc'],
    'bash': [home_dir, '.bash_profile'],
    'zsh': [home_dir, '.zshrc'],
    'tex': [snippets_dir, 'tex.snippets'],
    'ncl': [snippets_dir, 'ncl.snippets'],
}


def collect(args):

    if not os.path.isdir(matrix):

        os.mkdir(matrix)

    for file2backup in args.target:

        if file2backup in files:

            print(colors.green('\nCollecting ' + file2backup + '...\n'))
            shutil.copy(
                os.path.join(files[file2backup][0], files[file2backup][1]),
                matrix
            )

        else:

            print(colors.red('\n' + file2backup + ' is not supported!\n'))


def deploy(args):

    for file2backup in args.target:

        if file2backup in files:

            if os.path.exists(os.path.join(matrix, files[file2backup][1])):

                print(colors.green('\nDeploying ' + file2backup + '...\n'))
                shutil.copy(
                    os.path.join(matrix, files[file2backup][1]),
                    os.path.join(files[file2backup][0], files[file2backup][1])
                )

            else:

                print(colors.red('\n' + file2backup + ' not in matrix!\n'))

        else:

            print(colors.red('\n' + 'Wrong ' + file2backup + 'name!\n'))


def main():

    parser = argparse.ArgumentParser(
        description='FileMatrix: a backup & deploy system.')

    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 0.01')

    subparsers = parser.add_subparsers(help='running mode')
    subparsers.required = True
    subparsers.dest = 'mode'

    parser_collect = subparsers.add_parser(
        'collect',
        help='Collect your files.')

    parser_collect.add_argument(
        '-t', '--target',
        required=True,
        nargs='*',
        help='The target to be collected.')

    parser_deploy = subparsers.add_parser(
        'deploy',
        help='Deploy your files.')

    parser_deploy.add_argument(
        '-t', '--target',
        required=True,
        nargs='*',
        help='The target to be deployed.')

    args = parser.parse_args()

    if args.mode == 'collect':
        collect(args)

    elif args.mode == 'deploy':
        deploy(args)

if __name__ == '__main__':
    main()
