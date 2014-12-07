mkdir build
pushd build
    cmake ..
    make
    mv base.so ../../hmin/
popd
#rm -rf build/
