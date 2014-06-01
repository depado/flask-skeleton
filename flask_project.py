# -*- coding: utf-8 -*-

import os
import sys
import argparse
import shutil
import jinja2
import codecs
import platform

from utils import colors, query_yes_no, which

# Environment variables
cwd = os.getcwd()
script_dir = os.path.dirname(os.path.realpath(__file__))

# Jinja2 Environment
template_loader = jinja2.FileSystemLoader(searchpath=os.path.join(script_dir, "templates"))
template_env = jinja2.Environment(loader=template_loader)

def generate_help(name):
    template = template_env.get_template('help.jinja2')
    return template.render({'name': name, 'require': colors.WARNING, 'end': colors.ENDC})

def generate_brief(name, bower, debug, virtualenv):

    return template.render(template_var)

def generate_crsf_secret_key():
    return 

def main(argv):
    parser = argparse.ArgumentParser(description='Create a flask skeleton application using some command line options.')
    parser.add_argument('appname', help='The application name')
    parser.add_argument('-b', '--bower', help='Dependencies installed using bower')
    parser.add_argument('-n', '--no-debug', action='store_false')
    parser.add_argument('-v', '--virtualenv', action='store_true')
    args = parser.parse_args()

    errors = []
    bower = None
    bower_exe = None
    if args.bower:
        bower = args.bower.split(',')
        bower_exe = which('bower')
        if not bower_exe:
            errors.append('Bower executable could not be found.')
    virtualenv = args.virtualenv
    if virtualenv:
        virtualenv_exe = which('virtualenv')
        if not virtualenv_exe:
            errors.append('Virtualenv executable could not be found.')
    debug = args.no_debug
    appname = args.appname
    fullpath = os.path.join(cwd, appname)
    secret_key = codecs.encode(os.urandom(32), 'hex').decode('utf-8')

    template_var = {
        'pyversion': platform.python_version(),
        'appname': appname,
        'bower': bower,
        'debug': debug,
        'virtualenv': virtualenv,
        'secret_key': secret_key,
        'path': fullpath,
        'require': colors.WARNING,
        'enabled': colors.OKGREEN,
        'disabled': colors.FAIL,
        'end': colors.ENDC
    }

    if virtualenv:
        template_var['virtualenv_exe'] = virtualenv_exe

    if bower:
        template_var['bower_exe'] = bower_exe

    template = template_env.get_template('brief.jinja2')
    print(template.render(template_var))
    if len(errors) > 0:
        template = template_env.get_template('errors.jinja2')
        template_var = {
            'errors': errors,
            'red': colors.FAIL,
            'end': colors.ENDC
        }
        print(template.render(template_var))
    validate = query_yes_no("Is this correct ?")
    # TODO

if __name__ == '__main__':
    main(sys.argv)
