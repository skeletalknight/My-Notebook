from setuptools import setup

setup(
    name="mkdocs-replace-plugin",
    version="0.1",
    py_modules=["mkdocs_replace_plugin"],
    entry_points={
        'mkdocs.plugins': [
            'replace = mkdocs_replace_plugin:ReplacePlugin',
        ]
    },
)   