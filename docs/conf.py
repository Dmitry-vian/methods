# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import django
sys.path.insert(0, os.path.abspath('..'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'methods.settings')
django.setup()



# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Документация методов API'
copyright = '2024, Михалкин Дмитрий'
author = 'Михалкин Дмитрий'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo',
              'sphinx.ext.viewcode',
              'sphinx.ext.autodoc']

autodoc_default_options = {
    'exclude-members': 'description, basename, detail, name, suffix, id, command, output, objects, queryset'
}

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.html': 'html'
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
