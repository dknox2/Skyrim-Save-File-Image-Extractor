from pybuilder.core import Author
from pybuilder.core import init
from pybuilder.core import use_plugin

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")

default_task = "publish"

@init
def initialize(project):
	project.version = "1.0"
	project.summary = "Fall 2018 Systems Programming Project 4"
	project.authors = [Author("Dylan Knox", "dknox2@my.westga.edu")]
