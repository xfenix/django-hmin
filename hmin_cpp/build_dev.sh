rm -rf build/
mkdir build
pushd build
    cmake ..
    make
    echo '-----------------'
    python _dev.py
popd
