"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

from typing import Any

import hoa_tools
import sphinx.application

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
extensions = [
    "numpydoc",
    "autoapi.extension",
    "sphinx.ext.intersphinx",
    "matplotlib.sphinxext.plot_directive",
]

# autodoc_default_options = {'members': True}
autoapi_dirs = ["../src/hoa_tools/"]
autoapi_ignore = ["*tests/test_*.py"]

intersphinx_mapping = {
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "unyt": ("https://unyt.readthedocs.io/en/stable/", None),
    "zarr": ("https://zarr.readthedocs.io/en/main/", None),
}


def skip_private_modules(
    app: sphinx.application.Sphinx,
    what: str,
    name: str,
    obj: object,
    skip: bool,
    options: dict[str, Any],
) -> bool:
    """
    Skip any modules starting with '_'.
    """
    return "._" in name


def setup(app: sphinx.application.Sphinx) -> None:
    """
    Setup Sphinx app.
    """
    app.connect("autoapi-skip-member", skip_private_modules)


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
