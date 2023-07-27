from setuptools import setup, find_packages

setup(
    name="tangods_thorlabspm100",
    version="0.0.1",
    description="Tango Device for ThorlabsPM100",
    author="Daniel Schick",
    author_email="dschick@mbi-berlin.de",
    python_requires=">=3.6",
    entry_points={"console_scripts": ["ThorlabsPM100 = tangods_thorlabspm100:main"]},
    license="MIT",
    packages=["tangods_thorlabspm100"],
    install_requires=[
        "pytango",
        "ThorlabsPM100",
    ],
    url="https://github.com/MBI-Div-b/pytango-ThorlabsPM100",
    keywords=[
        "tango device",
        "tango",
        "pytango",
        "thorlabsPM100"
    ],
)
