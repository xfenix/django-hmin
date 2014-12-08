import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.HashMap;


class Minify {
    public static String placeholder = "<@!hmin_placeholder_%s_!@>";
    public static Pattern re_multispace = Pattern.compile("\\s{2,}");
    public static Pattern re_tags = Pattern.compile(
        "(<(script|textarea|style|pre).*?>.*?</(script|textarea|style|pre)>)",
        Pattern.CASE_INSENSITIVE
    );
    public static Pattern re_comment = Pattern.compile(
        "(<!--(?!\\[if.*?\\]).*?-->)", Pattern.CASE_INSENSITIVE
    );
    public static Pattern re_placeholder = Pattern.compile(
        placeholder.replace("%s", "([0-9]+)")
    );

    public static void main(String[] args) {
        if(args.length > 0) {
            System.out.println(Minify.compress(args[0], true));
        }
    }

    public static String compress(String content, Boolean remove_comments) {
        StringBuffer out = new StringBuffer();
        String position;
        Matcher match;
        HashMap<String, String> storage = new HashMap<String, String>();

        // safe tags
        match = re_tags.matcher(content);
        while(match.find()) {
            position = Integer.toString(match.start());
            storage.put(position, match.group(0));
            match.appendReplacement(
                out, placeholder.replace("%s", position)
            );
        }
        match.appendTail(out);

        // store content
        content = out.toString();

        // clear
        content = content.replace("\n", "");
        content = content.replace("\t", "");
        content = re_multispace.matcher(content).replaceAll(" ");
        content = content.replace("> <", "><");
        if(remove_comments) {
            content = re_comment.matcher(content).replaceAll(" ");
        }

        // return tags
        out = new StringBuffer();
        match = re_placeholder.matcher(content);
        while(match.find()) {
            match.appendReplacement(out, storage.get(match.group(1)));
        }
        match.appendTail(out);

        return out.toString().trim();
    }

    public static String compress(String content) {
        return Minify.compress(content, true);
    }
}
