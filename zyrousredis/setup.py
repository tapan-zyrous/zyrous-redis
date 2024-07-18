import setuptools
import toml
import json


# Dependencies for the package
def get_install_requirements():
    """
    The function is used to return the dependent requirement
    """
    packages = []
    try:
        # read the pipfile for required packages
        with open('./Pipfile', 'r', encoding='utf-8') as _file:
            pipfile = _file.read()
        # parse the toml
        pipfile_toml = toml.loads(pipfile)
        pipfile_packages = pipfile_toml['packages'].keys()
        
        # read my pipfile.lock
        with open('./Pipfile.lock', encoding='utf-8') as _file:
            data = json.load(_file)
        pinned_packages = data['default'].items()
    except (FileNotFoundError, KeyError):
        return packages
    

    for package, v in pinned_packages:
        if package in pipfile_packages:
            extras = ""
            if v.get('extras'):
                extras = "[" + ",".join(v.get('extras')) + "]"
            version = v.get('version', '*')
            if version == "*":
                packages.append(f"{package}{extras}")
            else:
                packages.append(f"{package}{extras}{version}")
    return packages

with open('README.md', encoding='utf-8') as file:
    read_me_description = file.read()

with open('pyproject.toml', encoding='utf-8') as toml_file:
    toml_str = toml_file.read()
    parsed_toml = toml.loads(toml_str)

# Setting up
setuptools.setup(
    name="zyrous-redis",
    version=parsed_toml['tool']['commitizen']['version'],
    author="Tapan Parmar",
    author_email="tapan.parmar@zyrous.com",
    long_description_content_type='text/markdown',
    long_description=read_me_description,
    package_dir={"": "src"},
    entry_points={"zyrous_plugins": ["redis = zyrous.redis"]},
    packages=setuptools.find_packages(where="src"),
    python_requires='>=3.8',
    install_requires=get_install_requirements(),
    keywords=["redis", "repository"],
)