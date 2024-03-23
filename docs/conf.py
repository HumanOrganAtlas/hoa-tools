"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# Project information
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "hoa-tools"
copyright = "2024, University College London"
author = "David Stansby"

# General configuration
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# Extension configuration
extensions = ["numpydoc", "sphinx_automodapi.automodapi"]

automodapi_toctreedirnm = "_api_autogen"
numpydoc_show_class_members = False

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
