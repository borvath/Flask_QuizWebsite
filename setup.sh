#!/bin/bash

# Run this script using source (e.g. source setup.sh)
# If `source` is not used, the venv activate script will not apply to your current shell.
# To source it manually, run: source <envname>/bin/activate  (where <envname> is the local environment directory)

envname=pyenv
dependencies=requirements.txt

if [ -d "$envname" ]; then
    source $envname/bin/activate
    echo "Checking dependencies ... "

    if [ -f "$dependencies" ]; then
      python3 -m pip install -U -r $dependencies
    else
      echo -e "\nDependencies file, $dependencies, does not exist in the current directory."
    fi

else
  echo "Creating virtual environment with venv ... "
  python3 -m venv $envname
  if [ -d "$envname" ]; then
    echo -e "\nEnvironment created. Install path: "
    echo $(pwd)/$envname

    echo -e "\nActivating environment for current shell ... "
    source $envname/bin/activate

    echo -e "Python3 Install Path: "
    which python3

    if [ -f "$dependencies" ]; then
      echo -e "\nInstalling dependencies ... "
      python3 -m pip install -r $dependencies
    else
      echo -e "\nDependencies file, $dependencies, does not exist in the current directory."
    fi

  else
    echo -e "\nVirtual environment creation failed. (Directory $envname does not exist)"
  fi
fi
