rm -rf build/
mkdir build
pushd build
    cmake ..
    make
    echo '-----------------'
    python base.py
popd
