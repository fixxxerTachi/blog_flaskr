activate_this='/home/tachi/.virtualenvs/sandbox2/bin/activate_this.py'
execfile(activate_this,dict(__file__=activate_this))
import sys
'''
sys.path.append('/home/tachi/prac_flaskr')
from flaskr import app as application
'''
sys.path.append('/home/tachi/prac_flask')
from tachilab_views import app as application
