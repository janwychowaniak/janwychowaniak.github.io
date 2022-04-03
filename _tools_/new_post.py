#!/usr/bin/python3


import os
import sys
import datetime


POST_FILEEXT = '.markdown'


def diag(msg_: str):
    print(f'>>> {msg_}', file=sys.stderr)


def get_post_template(post_title_: str,
                      post_date_: str,
                      post_categories_: str):
    return (f'---{os.linesep}'
            f'layout: post{os.linesep}'
            f'title:  "{post_title_}"{os.linesep}'
            f'date:   {post_date_}{os.linesep}'
            f'categories: {post_categories_}{os.linesep}'
            f'---{os.linesep}'
            f'{os.linesep}')


def spare_letter(char_: str):
    if char_.isalnum():
        return char_.lower()
    elif char_ == ' ':
        return '-'
    else:
        return ''


if __name__ == '__main__':

    if os.path.basename(os.getcwd()) != '_posts':
        print('*** Best invoked from the "_posts" directory', file=sys.stderr)
        sys.exit(1)

    dtnow = datetime.datetime.now()
    post_date = dtnow.strftime("%Y-%m-%d %H:%M:%S")
    sf_prefix = dtnow.strftime("%Y-%m-%d-")


    current_postfiles = [each for each in os.listdir() if each.endswith(POST_FILEEXT)]
    current_categories = set()
    for cpf in current_postfiles:
        with open(cpf) as file:
            categ_line = [line.rstrip() for line in file if line.startswith('categories: ')]
            if categ_line:
                current_categories.update(categ_line[0].split()[1:])

    post_title = input('Post title: ')
    suggested_filename = sf_prefix + ''.join([spare_letter(c) for c in post_title]) + POST_FILEEXT

    diag('Categories existing so far:')
    diag(f"  {' '.join(current_categories)}")
    post_categories = input('Post categories: ')

    diag('-----'*10)
    diag(f'Post title         : {post_title}')
    diag(f'Post date          : {post_date}')
    diag(f'Post categories    : {post_categories}')
    diag(f'Suggested filename : {suggested_filename}')
    diag('-----'*10)

    print(get_post_template(post_title, post_date, post_categories))
