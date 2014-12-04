#include <boost/regex.hpp>
#include <boost/python.hpp>
#include <boost/algorithm/string.hpp>


using namespace std;
using namespace boost::algorithm;

// dict type 
typedef map<string, string> dict;

// simple placeholder
string placeholder = "<@!hmin_placeholder_%s_!@>";
// tags container
dict tag_holder;
// build regexes
boost::regex multispace("\\s{2,}");
boost::regex re_placeholder(
    replace_all_copy(placeholder, "%s", "([0-9]+)")
);
boost::regex re_danger_tags(
    "(<(script|textarea|style|pre).*?>.*?</(script|textarea|style|pre)>)"
);

// helper functions
string tag_replace(boost::smatch const &what) {
    string position = boost::lexical_cast<std::string>(what.position(1));
    tag_holder[position] = what.str();
    return replace_all_copy(placeholder, "%s", position);
}

string tag_return(boost::smatch const &what) {
    return tag_holder[what[1]];
}

// minification
string minify(string content)
{
    // replace danger tags
    string clear_content = boost::regex_replace(
        content, re_danger_tags, tag_replace
    );

    // clear
    clear_content = boost::regex_replace(clear_content, multispace, " ");
    replace_all(clear_content, "\n", "");
    replace_all(clear_content, "> <", "><");
    trim(clear_content);

    // return tags back
    clear_content = boost::regex_replace(
        clear_content, re_placeholder, tag_return
    );

    return clear_content;
}


BOOST_PYTHON_MODULE(base)
{
    using namespace boost::python;
    def("minify", minify);
}
