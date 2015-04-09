# -*- coding: utf-8 -*-

import os
import sys
import argparse
import shutil
import jinja2
import codecs
import platform
import subprocess

from utils import colors, query_yes_no

# Environment variables
cwd = os.getcwd()
script_dir = os.path.dirname(os.path.realpath(__file__))

# Jinja2 Environment
template_loader = jinja2.FileSystemLoader(searchpath=os.path.join(script_dir, "templates"))
template_env = jinja2.Environment(loader=template_loader)


def generate_brief(template_var):
    template = template_env.get_template('brief.jinja2')
    return template.render(template_var)


def generate_crsf_secret_key():
    return 


def main(argv):
    parser = argparse.ArgumentParser(description='Create a flask skeleton application using some command line options.')
    parser.add_argument('appname', help='The application name')
    parser.add_argument('-b', '--bower', help='Dependencies installed using bower')
    parser.add_argument('-n', '--no-debug', action='store_false')
    parser.add_argument('-v', '--virtualenv', action='store_true')
    parser.add_argument('-d', '--database', action='store_true')
    parser.add_argument('-g', '--git', action='store_true')
    args = parser.parse_args()

    errors = []
    bower = None
    bower_exe = None
    if args.bower:
        bower = args.bower.split(',')
        bower_exe = shutil.which('bower')
        if not bower_exe:
            errors.append('Bower executable could not be found.')
    virtualenv = args.virtualenv
    virtualenv_exe = None
    if virtualenv:
        virtualenv_exe = shutil.which('virtualenv')
        if not virtualenv_exe:
            errors.append('Virtualenv executable could not be found.')
            virtualenv = False

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
        'end': colors.ENDC,
        'database': args.database,
        'git': args.git
    }

    if virtualenv:
        template_var['virtualenv_exe'] = virtualenv_exe

    if bower:
        template_var['bower_exe'] = bower_exe

    print(generate_brief(template_var))
    if len(errors) > 0:
        template = template_env.get_template('errors.jinja2')
        template_var = {
            'errors': errors,
            'red': colors.FAIL,
            'end': colors.ENDC
        }
        print(template.render(template_var))
        sys.exit(1)

    if query_yes_no("Is this correct ?"):
        if args.database:
            skeleton_dir = 'skel_db'
            config_file = 'config_db.jinja2'
        else:
            skeleton_dir = 'skel'
            config_file = 'config.jinja2'
        # Copying the whole skeleton into the new path. Error if the path already exists
        # TODO error handling here.
        print('Copying Skeleton...\t\t\t', end="", flush=True)
        shutil.copytree(os.path.join(script_dir, skeleton_dir), fullpath)
        print("{green}Ok{end}".format(green=colors.OKGREEN, end=colors.ENDC))
        # Creating the configuration file using the command line arguments
        print('Creating config file...\t\t\t', end="", flush=True)
        template = template_env.get_template(config_file)
        template_var = {
            'secret_key': secret_key,
            'debug': debug,
        }
        with open(os.path.join(fullpath, 'config.py'), 'w') as fd:
            fd.write(template.render(template_var))

        print("{green}Ok{end}".format(green=colors.OKGREEN, end=colors.ENDC))

        if virtualenv:
            # If virtualenv is requested, then create it and install the required libs to work
            print('Creating the virtualenv...\t\t', end="", flush=True)
            output, error = subprocess.Popen(
                [virtualenv_exe, os.path.join(fullpath, 'venv'), '--no-site-package'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ).communicate()
            if error:
                with open('virtualenv_error.log', 'w') as fd:
                    fd.write(error.decode('utf-8'))
                    print("{red}An error occured during the creation of the virtualenv. Please consult {yellow}virtualenv_error.log{red} file for details.{end}".format(
                        red=colors.FAIL,
                        yellow=colors.WARNING,
                        end=colors.ENDC))
                    sys.exit(2)
            venv_bin = os.path.join(fullpath, 'venv/bin')
            print("{green}Ok{end}".format(green=colors.OKGREEN, end=colors.ENDC))
            print("Installing Python Dependencies...\t", end="", flush=True)
            output, error = subprocess.Popen(
                [os.path.join(venv_bin, 'pip'), 'install', '-r', os.path.join(fullpath, 'requirements.txt')],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ).communicate()
            if error:
                with open('pip_error.log', 'w') as fd:
                    fd.write(error.decode('utf-8'))
                    print("{red}An error occured during the installation of dependencies. Please consult {yellow}pip_error.log{red} file for details.{end}".format(
                        red=colors.FAIL,
                        yellow=colors.WARNING,
                        end=colors.ENDC))
                    sys.exit(2)
            print("{green}Ok{end}".format(green=colors.OKGREEN, end=colors.ENDC))

        if bower:
            os.chdir(os.path.join(fullpath, 'app', 'static'))
            for dependency in bower:
                print("Bower {}...\t\t\t".format(dependency.title()), end="", flush=True)
                output, error = subprocess.Popen(
                    [bower_exe, 'install', dependency],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                ).communicate()
                if error:
                    with open('bower_error.log', 'w') as fd:
                        fd.write(error.decode('utf-8'))
                    print("{red}An error occured during the installation of {dep}. Please consult {yellow}bower_error.log{red} file for details.{end}".format(
                        red=colors.FAIL,
                        yellow=colors.WARNING,
                        end=colors.ENDC,
                        dep=dependency))
                print("{green}Ok{end}".format(green=colors.OKGREEN, end=colors.ENDC))

        if args.git:
            print('Git Init...\t\t\t\t', end="", flush=True)
            output, error = subprocess.Popen(
                ['git', 'init', fullpath],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ).communicate()
            if error:
                with open('git_error.log', 'w') as fd:
                    fd.write(error.decode('utf-8'))
                    print("{red}An error occured during the creation of the virtualenv. Please consult "
                          "{yellow}virtualenv_error.log{red} file for details.{end}".format(
                              red=colors.FAIL,
                              yellow=colors.WARNING,
                              end=colors.ENDC))
                    sys.exit(2)
            print("{green}Ok{end}".format(green=colors.OKGREEN, end=colors.ENDC))
            print('Generating Gitignore...\t\t\t', end="", flush=True)
            shutil.copyfile(os.path.join(script_dir, 'templates', 'gitignore'), os.path.join(fullpath, '.gitignore'))
            print("{green}Ok{end}".format(green=colors.OKGREEN, end=colors.ENDC))

    else:
        print("Aborting")
        sys.exit(0)

if __name__ == '__main__':
    main(sys.argv)
