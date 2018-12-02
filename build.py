import os
import subprocess

from pybuilder.core import Author
from pybuilder.core import init
from pybuilder.core import use_bldsup
from pybuilder.core import use_plugin
from pybuilder.core import task

use_bldsup(build_support_dir = os.path.join("src", "main", "python"))
import ess2bmp

use_plugin("python.core")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")

default_task = "publish"

@task
def convertAllIn(project):
	# normpath() allows for linux shortcuts like "~" to be parsed correctly,
	# and "foo/bar/../" is parsed correctly as "foo/"
	directory = os.path.normpath(project.get_property("directory"))
	output_dir = directory + "_bmp"

	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	file_names = [file for file in os.listdir(directory) if file.endswith(".ess")]
	for file_name in file_names:
		bmp_file_name = file_name[:-3] + "bmp"
		qualified_file_name = os.path.join(directory, file_name)
		qualified_bmp_name = os.path.join(output_dir, bmp_file_name)

		ess2bmp.ess_to_bmp(qualified_file_name, qualified_bmp_name)

@init
def initialize(project):
	project.version = "1.0"
	project.summary = "Fall 2018 Systems Programming Project 4"
	project.authors = [Author("Dylan Knox", "dknox2@my.westga.edu")]