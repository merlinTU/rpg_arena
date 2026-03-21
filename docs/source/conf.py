import os
import sys

sys.path.insert(0, os.path.abspath('../../src'))
sys.path.insert(0, os.path.abspath('../../tests'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

html_theme = 'furo'
html_theme_options = {
    "navigation_with_keys": True,
    "light_css_variables": {"color-brand-primary": "#FF6600"},
    "dark_css_variables": {"color-brand-primary": "#FF6600"},
}

templates_path = ['_templates']
exclude_patterns = []
html_static_path = ['_static']