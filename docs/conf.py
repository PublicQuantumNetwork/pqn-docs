project = 'Public Quantum Network'
copyright = '2026, Benjamin Nussbaum, Marcos Frenkel, Soroush Hoseini'
author = 'Benjamin Nussbaum, Marcos Frenkel, Soroush Hoseini'

extensions = ['myst_parser']

templates_path = ['_templates']
exclude_patterns = ['build']

language = "en"

html_theme = "pydata_sphinx_theme"
html_static_path = ['_static']
html_baseurl = 'https://publicquantumnetwork.github.io/pqn-docs/'

html_theme_options = {
    "logo": {
        "text": "Public Quantum Network",
    },
    "external_links": [
        {
            "url": "https://github.com/PublicQuantumNetwork/pqn-stack",
            "name": "pqn-stack",
        },
        {
            "url": "https://github.com/PublicQuantumNetwork/pqn-gui",
            "name": "pqn-gui",
        },
    ],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/PublicQuantumNetwork",
            "icon": "fa-brands fa-github",
        }
    ],
}
