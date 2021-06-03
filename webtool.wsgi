import sys
sys.path.append('/var/www/jforseth.tech/')

activate_this = '/var/www/jforseth.tech/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from webtool import app as application

