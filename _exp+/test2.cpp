#include <boost/regex.hpp>

using namespace std;


string minifyhtml(string s) {
    boost::regex nowhitespace(
    "(?ix)"
    "(?>"           // Match all whitespans other than single space.
    "[^\\S ]\\s*"   // Either one [\t\r\n\f\v] and zero or more ws,
    "| \\s{2,}"     // or two or more consecutive-any-whitespace.
    ")"             // Note: The remaining regex consumes no text at all...
    "(?="           // Ensure we are not in a blacklist tag.
    "[^<]*+"        // Either zero or more non-"<" {normal*}
    "(?:"           // Begin {(special normal*)*} construct
    "<"             // or a < starting a non-blacklist tag.
    "(?!/?(?:textarea|pre|script)\\b)"
    "[^<]*+"        // more non-"<" {normal*}
    ")*+"           // Finish "unrolling-the-loop"
    "(?:"           // Begin alternation group.
    "<"             // Either a blacklist start tag.
    "(?>textarea|pre|script)\\b"
    "| \\z"         // or end of file.
    ")"             // End alternation group.
    ")"             // If we made it here, we are not in a blacklist tag.
    );

    // @todo Don't remove conditional html comments
    boost::regex nocomments("<!--(.*)-->");

    s = boost::regex_replace(s, nowhitespace, " ");
    s = boost::regex_replace(s, nocomments, "");
    return s;
}
