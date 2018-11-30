#!/bin/bash

TWINE_USERNAME=nearbydelta

extract_version()
{
    LIB_VER=$(cat setup.py | grep "version=" | cut -d\' -f2 | cut -d- -f1)
    LIB_VER_MAJOR=$(echo $LIB_VER | cut -d. -f1)
    LIB_VER_MINOR=$(echo $LIB_VER | cut -d. -f2)
    LIB_VER_INCRM=$(echo $LIB_VER | cut -d. -f3)
    LIB_VER_CURRENT=$LIB_VER_MAJOR.$LIB_VER_MINOR.$LIB_VER_INCRM
}

add_incremental_ver()
{
    LIB_VER_NEXT=$LIB_VER_MAJOR.$LIB_VER_MINOR.$(($LIB_VER_INCRM + 1))
}

add_minor_ver()
{
    LIB_VER_NEXT=$LIB_VER_MAJOR.$(($LIB_VER_MINOR + 1)).0
}

set_version()
{
    cat setup.py | sed -e "s/version=\s*'.*'/version='$1'/g" > setup.py.new
    rm setup.py
    mv setup.py.new setup.py
    git add setup.py

    cat doc_source/conf.py | sed -e "s/release\s*=\s*'.*'/release = '$1'/g" > doc_source/conf.new
    rm doc_source/conf.py
    mv doc_source/conf.new doc_source/conf.py
    git add doc_source/conf.py
}

ask_proceed()
{
    read -p "Proceed $1 [Y/n/p]? " YN
    if [ "${YN,,}" = "n" ]; then
        exit 0
    fi
}

pip_upgrade()
{
    read -p "Require superuser privileges?" SUDO
    if [ "${SUDO,,}" = "y" ]; then
        sudo -H pip3 install --upgrade sphinx sphinx_rtd_theme twine pytest pypandoc
    else
        pip3 install --upgrade sphinx sphinx_rtd_theme twine pytest pypandoc
    fi
}

ask_proceed "PIP upgrade"
if [ "${YN,,}" != "p" ]; then
    pip_upgrade
fi

ask_proceed "Test"
if [ "${YN,,}" != "p" ]; then
    python3 -m pytest tests/dictionary_test.py
    python3 -m pytest tests/extension_core_spec.py
    python3 -m pytest tests/proc_core_spec.py
    python3 -m pytest tests/type_core_spec.py
fi

extract_version
echo $LIB_VER_CURRENT

ask_proceed "Set Current Version"
if [ "${YN,,}" != "p" ]; then
    set_version $LIB_VER_CURRENT
fi

ask_proceed "Build document"
if [ "${YN,,}" != "p" ]; then
    mv docs/.nojekyll ./
    mv docs/index.html ./
    make clean
    make html
    mv ./.nojekyll docs/
    mv ./index.html docs/
fi

ask_proceed "Build package"
if [ "${YN,,}" != "p" ]; then
    rm -r dist/
    python3 setup.py bdist_wheel

    git add .
    git commit -m "Release: v$LIB_VER_CURRENT"
    git tag v$LIB_VER_CURRENT
fi

ask_proceed "Upload package"
if [ "${YN,,}" != "p" ]; then
    twine upload dist/koalanlp-*.whl
fi

ask_proceed "Set Next"
if [ "${YN,,}" != "p" ]; then
    add_incremental_ver
    set_version "$LIB_VER_NEXT-SNAPSHOT"
fi

ask_proceed "Commit"
if [ "${YN,,}" != "p" ]; then
    git add .
    git commit -m "Initial commit for v$LIB_VER_NEXT"
    git tag v$LIB_VER_NEXT
    git push --all
fi
