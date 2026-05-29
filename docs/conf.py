project = 'Public Quantum Network'
copyright = '2026, Public Quantum Network'
author = 'Public Quantum Network Team'

extensions = ['myst_parser', 'sphinxcontrib.mermaid']

templates_path = ['_templates']
exclude_patterns = ['build', 'adr']

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
            "url": "https://github.com/PublicQuantumNetwork/pqn-node",
            "name": "pqn-node",
        },
        {
            "url": "https://github.com/PublicQuantumNetwork/pqn-gui",
            "name": "pqn-gui",
        },
        {
            "url": "https://github.com/PublicQuantumNetwork/pqn-hardware",
            "name": "pqn-hardware",
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
