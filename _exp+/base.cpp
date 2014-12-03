#include <boost/regex.hpp>
#include <boost/python.hpp>
#include <boost/algorithm/string.hpp>


using namespace std;
using namespace boost::algorithm;


string minify(string content)
{
    // simple placeholder
    string placeholder = "<@!hmin_placeholder_%s_!@>";
    // build regexes
    boost::regex multispace("\\s{2,}");
    boost::regex re_placeholder(
        replace_all_copy(placeholder, "%s", "([0-9]+)")
    );
    boost::regex replaced_tag("
        (<(script|textarea|style|pre).*?>.*?</(script|textarea|style|pre)>)
    ");

    // clear
    content = boost::regex_replace(content, multispace, " ");
    replace_all(content, "\n", "");
    replace_all(content, "> <", "><");
    trim(content);

    return content;
}


BOOST_PYTHON_MODULE(base)
{
    using namespace boost::python;
    def("minify", minify);
}
