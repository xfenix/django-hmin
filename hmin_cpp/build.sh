mkdir build
pushd build
    cmake ..
    make
    mv base.so ../base.so
popd
rm -rf build/
