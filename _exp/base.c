#include <Python.h>
#include <string.h>


static PyObject*
minify(PyObject* self, PyObject* args)
{
    const char* content;
    PyObject* list, uresult;

    // get args
    if (!PyArg_ParseTuple(args, "s", &content))
        return NULL;

    // minify
    list = PyUnicode_Split(PyUnicode_FromString(content), NULL, -1);
    uresult = PyUnicode_Join(PyUnicode_FromString(" "), list);

    return uresult;
}

static PyMethodDef BaseMethods[] =
{
     {"minify", minify, METH_VARARGS, "Minification method"},
     {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initbase(void)
{
     (void) Py_InitModule("base", BaseMethods);
}
