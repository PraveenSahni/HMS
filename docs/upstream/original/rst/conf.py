# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GNU Health Hospital Information System'
copyright = '2025, GNU Solidario'

# release has to be defined inside rst_prolog so that sphinx substitution extensions can use it inside code blocks
rst_prolog = """
.. |version| replace:: 5.0
.. |release| replace:: 5.0.0
.. |version_nodot| replace:: 50
.. |author| replace:: GNU Solidario
.. |tryton_version| replace:: 7.0
.. |tryton_bigger| replace:: 7.1
.. |gunicorn_version| replace:: 23.0
"""

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.todo',
        'sphinx_toolbox.wikipedia',
        'sphinxcontrib.images',
        'sphinx_substitution_extensions'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

todo_include_todos = True
todo_link_only = True


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_sidebars = { '**': ['globaltoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html']}

html_static_path = ['_static']
html_css_files = [
    'css/custom.css',
]
