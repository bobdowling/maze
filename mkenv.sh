#!/usr/bin/bash -e
# mkenv.sh - If you change the name, change the "git add" line too.

mkdir src
mkdir tst

cat > .gitignore <<EOF1
env
__pycache__
.mypy_cache
EOF1

cat > requirements.txt <<EOF2
black
mypy
pydantic
EOF2

git init --initial-branch main
git add .gitignore requirements.txt mkenv.sh
git commit --message "Initial set-up."
python -m venv env

source env/bin/activate
pip install --require-virtualenv --upgrade pip
pip install --require-virtualenv --upgrade --requirement requirements.txt
