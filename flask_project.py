# -*- coding: utf-8 -*-

import os
import sys
import argparse
import shutil
import jinja2
import codecs

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

    bower = None
    if args.bower:
        bower = args.bower.split(',')
        bower_exe = which('bower')
    virtualenv = args.virtualenv
    if virtualenv:
        virtualenv_exe = which('virtualenv')
    debug = args.no_debug
    appname = args.appname
    fullpath = os.path.join(cwd, appname)
    secret_key = codecs.encode(os.urandom(32), 'hex').decode('utf-8')

    template_var = {
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

    template = template_env.get_template('brief.jinja2')
    print(template.render(template_var))
    validate = query_yes_no("Is this correct ?")
    print(validate)
    print(which('virtualenv'))

if __name__ == '__main__':
    main(sys.argv)