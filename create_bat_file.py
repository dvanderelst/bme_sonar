# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 17:15:51 2021

@author: dieter
"""
import os
import sys

def make_bat(python_script, bat_name=None):
    print('Make bat file:')
    executable = sys.executable

    # Get path to anaconda3
    index = executable.find('anaconda3')
    anaconda = executable[0:index] + 'anaconda3'

    # Get current anaconda environment
    parts = executable.split(os.sep)
    environment = None
    if 'envs' in parts:
        index = parts.index('envs')
        environment = parts[index + 1]

    print('> Executable:', anaconda)
    print('> Anaconda:', anaconda)
    print('> Environment:', environment)

    script = '*Scripts*activate.bat'
    script = script.replace('*', os.sep)
    
    line1 = 'call ' + anaconda + script + ' ' + anaconda 
    line2 = 'call activate ' + str(environment)
    line3 = 'call python ' + python_script
    
    name = python_script.replace('.py', '')
    name = 'run_' + name + '.bat'
    if bat_name: name = bat_name

    print('> bat file:', name)
    
    f = open(name, 'w')
    f.write(line1 + '\n')
    if environment is not None: f.write(line2 + '\n')
    f.write(line3 + '\n')
    f.close()
    
    
make_bat('Run.py', 'Run.bat')

