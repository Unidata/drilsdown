#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import subprocess
import sys
import recommonmark.parser


# -- path -------------------------------------------------------

from os.path import dirname
docs = dirname(dirname(__file__))
root = dirname(docs)
sys.path.insert(0, root)

# -- bash utility function --------------------------------------
def bash(filename):
    """Runs a bash script in the local directory"""
    sys.stdout.flush()
    subprocess.call("bash {}".format(filename), shell=True)


bash('make_links.sh')
# -- source files and parsers -----------------------------------

source_suffix = ['.rst', '.ipynb','.md'] 


# -- Sphinx extensions and configuration ------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'nbsphinx',
    'IPython.sphinxext.ipython_console_highlighting',
    'recommonmark'
]

nbsphinx_allow_errors = True   # exception ipstruct.py ipython_genutils

#tisns is processed by Jinja2 and inserted before each notebook
nbsphinx_prolog = r"""
{% set docname = env.doc2path(env.docname, base='doc') %}

.. only:: html

    .. role:: raw-html(raw)
        :format: html

    .. nbinfo::
        Click here to launch an
        interactive online version of this notebook:
        :raw-html:`<a href="https://weather.rsmas.miami.edu/notebook/gh/unidata/drilsdown/master?filepath=UseCase_Examples/{{ '/'.join(docname.split('/')[2:]) }}"><img alt="nbapp badge" src="https://img.shields.io/badge/Try%20it!-online-orange" style="vertical-align:text-bottom"></a>`

       

.. raw:: latex

    \vfil\penalty-1\vfilneg
    \vspace{\baselineskip}
    \textcolor{gray}{The following section was generated from
    \texttt{\strut{}{{ docname }}}\\[-0.5\baselineskip]
    \noindent\rule{\textwidth}{0.4pt}}
    \vspace{-2\baselineskip}
"""
# This is processed by Jinja2 and inserted after each notebook

# Execute notebooks before conversion: 'always', 'never', 'auto' (default)
#nbsphinx_execute = 'never'

# Use this kernel instead of the one stored in the notebook metadata:
#nbsphinx_kernel_name = 'python3'

# List of arguments to be passed to the kernel that executes the notebooks:
#nbsphinx_execute_arguments = ['--InlineBackend.figure_formats={"png", "pdf"}']

# Execute notebooks before conversion: 'always', 'never', 'auto' (default)
#nbsphinx_execute = 'never'

# Use this kernel instead of the one stored in the notebook metadata:
#nbsphinx_kernel_name = 'python3'

# List of arguments to be passed to the kernel that executes the notebooks:
#nbsphinx_execute_arguments = ['--InlineBackend.figure_formats={"svg", "pdf"}']


# -- General information -------

_release = {}
version = '0.2.1' 
release = '0.2.1'

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']


master_doc = 'index'
# General information about the project.
project = 'DRILSDOWN'
copyright = '2019, DRILSDOWN team'
author = 'DRILSDOWN team'

language = None
exclude_patterns = ['*.txt','*.md','_build', '**.ipynb_checkpoints','Thumbs.db','.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False

# -- Get version information and date from Git ----------------------------

try:
    from subprocess import check_output
    release = check_output(['git', 'describe', '--tags', '--always'])
    release = release.decode().strip()
    today = check_output(['git', 'show', '-s', '--format=%ad', '--date=short'])
    today = today.decode().strip()
except Exception:
    today = '<unknown date>'


# -- html --------------------------
html_theme = 'sphinx_rtd_theme'

# html_static_path = ['_static']
htmlhelp_basename = 'DRILSDOWNdoc'

# -- Options for HTML output ----------------------------------------------

html_title = project + ' version ' + release



# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}


# -- tex ---------------------------
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'DRILSDOWN.tex', 'DRILSDOWN Documentation',
     'DRILSDOWN team', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'DRILSDOWN', 'DRILSDOWN Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'DRILSDOWN', 'DRILSDOWN Documentation',
     author, 'DRILSDOWN', 'One line description of project.',
     'Miscellaneous'),
]



# -- epub --------------------------

# Bibliographic Dublin Core info.
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright


# -- Theme options -----------------

# Options are theme-specific and customize the look and feel of the theme.
html_theme_options = {
'collapse_navigation': False,
'navigation_depth': 3,
'sticky_navigation': False}
