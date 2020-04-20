"""This is a simple script to update the repo with either a new package or a new version of a package"""
from os import environ, path, mkdir

PACKAGE_NAME = environ.get('PACKAGE_NAME', '0')
PACKAGE_FOLDER_NAME = PACKAGE_NAME.replace('_', '-')
PACKAGE_VERSION = environ.get('PACKAGE_VERSION', '0')

NEW_VERSION_STRING = f'    <a href="git+ssh://git@{PACKAGE_NAME}.github.com/nishalparbhu/{PACKAGE_NAME}@' \
                     f'{PACKAGE_VERSION}#egg={PACKAGE_NAME}-{PACKAGE_VERSION[1:]}" data-requires-python="&gt;=3.6.0">' \
                     f'{PACKAGE_NAME}-{PACKAGE_VERSION[1:]}</a><br/>\n'

NEW_PACKAGE_STRING = f'		<p><a href="{PACKAGE_FOLDER_NAME}/">{PACKAGE_NAME}</a></p>\n'

NEW_PACKAGE_INDEX = f'<!DOCTYPE html>\n<html>\n  <head>\n    <title>Links for {PACKAGE_NAME}</title>\n  </head>\n  ' \
                    f'<body>\n    <h1>Links for {PACKAGE_NAME}</h1>\n{NEW_VERSION_STRING}  </body>\n</html>'


def create_new_package():
    with open('index.html', 'r') as base_index_file:
        line_list = base_index_file.readlines()

    for line in line_list:
        if '</body>' in line:
            line_list[line_list.index(line)-1:line_list.index(line)-1] = [NEW_PACKAGE_STRING]
            break

    with open('index.html', 'w') as new_base_index_file:
        new_base_index_file.writelines(line_list)

    mkdir(PACKAGE_FOLDER_NAME)

    with open(f'{PACKAGE_FOLDER_NAME}/index.html', 'w') as new_package_html_file:
        new_package_html_file.writelines(NEW_PACKAGE_INDEX)
    return True


def update_existing_package():
    with open(f'{PACKAGE_FOLDER_NAME}/index.html', 'r') as package_index_file:
        line_list = package_index_file.readlines()

    for line in line_list:
        if '</body>' in line:
            line_list[line_list.index(line):line_list.index(line)] = [NEW_VERSION_STRING]
            break

    with open(f'{PACKAGE_FOLDER_NAME}/index.html', 'w') as new_package_index_file:
        new_package_index_file.writelines(line_list)
    return True


if PACKAGE_NAME != '0' and PACKAGE_VERSION != '0':
    if path.exists(PACKAGE_FOLDER_NAME):
        if path.exists(f'{PACKAGE_FOLDER_NAME}/index.html'):
            result = update_existing_package()
            if result:
                print(f'Updated package {PACKAGE_NAME} with new version {PACKAGE_VERSION}')
    else:
        result = create_new_package()
        if result:
            print(f'New package for {PACKAGE_NAME} for version {PACKAGE_VERSION} successfully created')
