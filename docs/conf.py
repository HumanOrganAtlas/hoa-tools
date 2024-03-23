"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import hoa_tools

# Project information
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = "hoa-tools"
project_copyright = "2024, University College London"
author = "David Stansby"
version = hoa_tools.__version__
release = hoa_tools.__version__

# General configuration
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
default_role = "any"
nitpicky = True

# Internationalisation
language = "en"

# Extension configuration
extensions = ["numpydoc", "sphinx_automodapi.automodapi", "sphinx.ext.intersphinx"]

automodapi_toctreedirnm = "_api_autogen"
numpydoc_show_class_members = False
intersphinx_mapping = {"pandas": ("https://pandas.pydata.org/docs/", None)}

# Options for HTML output
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_css_files = [
    "hoa-style.css",
]
html_theme_options = {
    "logo": {
        "text": "HOA Tools",
    }
}
html_use_index = False
html_show_sourcelink = False
html_show_copyright = False
html_sidebars = {"**": ["sidebar-nav-bs", "sidebar-ethical-ads"]}
