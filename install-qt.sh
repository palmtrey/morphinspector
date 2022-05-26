#!/bin/bash

apt-get install cmake

git clone git://code.qt.io/qt/qt5.git
cd qt5
git checkout 6.3
perl init-repository

cd ..
mkdir qt6-build
cd qt6-build
../qt5/configure -prefix /bin
cmake --build . --parallel 4
cmake --install .



