cmake_minimum_required(VERSION 2.8)
FIND_PACKAGE(PythonInterp)
FIND_PACKAGE(PythonLibs)
FIND_PACKAGE(Boost COMPONENTS python regex REQUIRED)

# ENABLE_TESTING()
INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS})
LINK_LIBRARIES(${Boost_LIBRARIES}) # Deprecated but so convenient!
# LINK_LIBRARIES(boost_regex)

PYTHON_ADD_MODULE(base base.cpp)
FILE(COPY base.py DESTINATION .)
# ADD_TEST(01-HelloWorld base.py)
