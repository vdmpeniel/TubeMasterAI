## Python Manual

### Introduction
pip is the package installer for Python. It allows you to easily install, update,
and manage packages for your Python projects. This manual will guide you through
the most common pip commands and options.

### Create a symbolic link to use the command python instead of python3
sudo ln -s /usr/bin/python3 /usr/bin/python

### Installing pip
To install pip on ubuntu do the following:

sudo apt install python3-pip

You can also update it like this:
pip install --upgrade pip
python -m pip install --upgrade pip





## Using venv
### Installing venv:
sudo apt install python3.12-venv

where python3.x is the version of python running in your environment

### Environment Creation
To create a new virtual environment, use the following command:

python -m venv myenv
		
Replace myenv with the name of your environment.

### Environment Activation
To activate the environment, use the following command:

source myenv/bin/activate  # On Linux/Mac
myenv\Scripts\activate  # On Windows
		
You should see the name of the environment printed on your command line.

### Environment Deactivation
To deactivate the environment, use the following command:

deactivate
		


## Using pyenv ***
### Installation
curl https://pyenv.run | bash


If activating an environment doesn't work:
- Add pyenv-virtualenv to your shell configuration

Open your shell configuration file in a text editor. 
The file is usually located in one of the following
locations:

nano ~/.bashrc (for Bash shell)
nano ~/.zshrc (for Zsh shell)
Add the following lines to the end of the file:

export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
		
Step 2: Restart your shell or reload the configuration

Restart your terminal or run the following command to reload
the configuration:

source ~/.bashrc


		

### Install the desired version of Python:
pyenv install x.x.

### Create a new virtual environment:
pyenv virtualenv x.x myEnv
Replace myEnv with your desired environment name

### Activate an environment:
pyenv activate <environment_name>

or

pyenv shell <environment_name>

### Deactivate an environment
pyenv deactivate

If that doesn't work do this:
pyenv shell --unset

If that doesn't work do this:
unset PYENV_ACTIVE_ENV
unset PYENV_VIRTUALENV_PROMPT
echo $PYENV_ACTIVE_ENV
source ~/.bashrc

### Listing available environments:
pyenv versions

### Setting a global environment:
pyenv global <environment_name>

### Setting a local environment:
pyenv local <environment_name>
for instance setting python 3.9 for the local env
pyenv local 3.9.10

### Removing an environment 
first deactivate it
pyenv uninstall myEnv






## Package Management
### Package Installation
To install a package, use the following command:

pip install <package_name>
		
Replace <package_name> with the name of the package you want to install.

To avoid using caches when installing packages with pip, you can use the --no-cache-dir option.

Here's an example:

pip install --no-cache-dir package_name
		
This will tell pip to not use the cache directory when installing the package.

Alternatively, you can also use the --no-binary option to force pip to install the package from source, rather than using a cached binary:

pip install --no-binary :all: package_name
		
This will ensure that pip downloads the package from the repository and builds it from source, rather than using a cached binary.

You can also use the --force-reinstall option to force pip to reinstall the package, even if it's already installed:

pip install --force-reinstall package_name


### Package Uninstallation
To uninstall a package, use the following command:

pip uninstall <package_name>
		
### Replace <package_name> with the name of the package you want to uninstall.

### Installation from requirements.txt
To install packages from a requirements.txt file, use the following command:

pip install -r requirements.txt
		
This will install all packages listed in the requirements.txt file.

### Package Upgrade
To upgrade a package to the latest version, use the following command:

pip install --upgrade <package_name>
		
Replace <package_name> with the name of the package you want to upgrade.

### Listing Installed Package
To freeze the current package versions, use the following command:

pip freeze
		
This will output a list of installed packages with their versions.

### Persisting local packages to requirements.txt
pip freeze --local > requirements.txt

### Package Search
To search for packages, use the following command:

pip search <package_name>
		
Replace <package_name> with the name of the package you want to search for.

### Package Information
To show information about a package, use the following command:

pip show <package_name>
		
### Replace <package_name> with the name of the package you want to show information about.

Package List
To list all installed packages, use the following command:

pip list
		
This will output a list of all installed packages with their versions.

### Troubleshooting
If you encounter issues with package installation, try upgrading pip using 
pip install --upgrade pip.

If you encounter issues with package uninstallation, try using 
pip uninstall --force <package_name>.

If you encounter issues with environment activation, try using s
ource myenv/bin/activate --no-site-packages (on Linux/Mac) or myenv\Scripts\activate --no-site-packages (on Windows).



### Using pipreqs
You can also use the pipreqs package to generate a 
requirements.txt file. You can install pipreqs using pip:

pip install pipreqs
		
Then, you can use the following command to generate a 
requirements.txt file:

pipreqs. --force
		
This will generate a requirements.txt file that lists all 
the packages that are required by your project.