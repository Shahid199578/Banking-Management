# This file must be used with Python 3. For Python 2 environments, use activate_this.py instead.

import os
import sys

# Get the directory of this script
this_dir = os.path.dirname(os.path.abspath(__file__))

# Determine the path to the virtual environment directory
venv_dir = os.path.join(this_dir, '..')

# Define the path to the activate script based on the Python version
if sys.version_info >= (3, 0):
    activate_script = os.path.join(venv_dir, 'bin', 'activate')
else:
    activate_script = os.path.join(venv_dir, 'bin', 'activate_this.py')

# Execute the activate script
with open(activate_script) as f:
    code = compile(f.read(), activate_script, 'exec')
    exec(code, dict(__file__=activate_script))

