import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.HashMap;


class Minify {
    public static String placeholder = "<@!hmin_placeholder_%s_!@>";
    public static Pattern re_multispace = Pattern.compile("\\s{2,}");
    public static Pattern re_tags = Pattern.compile(
        "(<(script|textarea|style|pre).*?>.*?</(script|textarea|style|pre)>)"
    );
    public static Pattern re_comment = Pattern.compile(
        "<!--(?!\\[if.*?\\]).*?-->"
    );
    public static Pattern re_placeholder = Pattern.compile(
        placeholder.replace("%s", "([0-9]+)")
    );

    public static void main(String[] args) {
        if(args.length > 0) {
            String content = args[0];
            Matcher match;
            HashMap<String, String> storage = new HashMap<String, String>();

            // safe tags
            match = re_tags.matcher(content);
            StringBuffer out = new StringBuffer();
            while(match.find()) {
                storage.put(Integer.toString(match.start()), match.group(0));
                match.appendReplacement(out, placeholder.replace("%s", "1"));
            }

            // clear
            content = content.replace("\n", "");
            content = re_multispace.matcher(content).replaceAll(" ");
            content = content.replace("> <", "><");

            // return tags


            System.out.println(out);
        }
    }
}
