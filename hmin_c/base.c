#include <sys/types.h>
#include <regex.h>
#include "dict.h"


int main(int argc, char **argv) {
    // hashtable_t *hashtable = ht_create( DICT_MAX_SIZE );
    // ht_set( hashtable, "key1", "inky" );
    // printf( "%s\n", ht_get( hashtable, "key1" ) );
    // return 0;

    int i, res, len;
    char result[BUFSIZ];
    regex_t preg;
    regmatch_t pmatch[10];
    char* src = argv[1];
    const char* pattern = "<script>(.*?)</script>";

    regcomp(&preg, pattern, REG_EXTENDED);

    res = regexec(&preg, src, 10, pmatch, REG_NOTBOL);

    if(res == REG_NOMATCH) {
        printf("NO match\n");
        exit(0);
    }

    for (i = 0; pmatch[i].rm_so != -1; i++) {
        len = pmatch[i].rm_eo - pmatch[i].rm_so;
        memcpy(result, src + pmatch[i].rm_so, len);
        result[len] = 0;
        printf("num %d: '%s'\n", i, result);
    }

    regfree(&preg);
    /*
   int i = 0;
   int res;
   int len;
   char result[BUFSIZ];
   char err_buf[BUFSIZ];
   char* src = argv[1];

   const char* pattern = "\\<[^,;]+\\>";
   regex_t preg;

   regmatch_t pmatch[10];

   if( (res = regcomp(&preg, pattern, REG_EXTENDED)) != 0)
   {
      regerror(res, &preg, err_buf, BUFSIZ);
      printf("regcomp: %s\n", err_buf);
      exit(res);
   }

   res = regexec(&preg, src, 10, pmatch, REG_NOTBOL);
   //~ res = regexec(&preg, src, 10, pmatch, 0);
   //~ res = regexec(&preg, src, 10, pmatch, REG_NOTEOL);
   if(res == REG_NOMATCH)
   {
      printf("NO match\n");
      exit(0);
   }
   for (i = 0; pmatch[i].rm_so != -1; i++)
   {
      len = pmatch[i].rm_eo - pmatch[i].rm_so;
      memcpy(result, src + pmatch[i].rm_so, len);
      result[len] = 0;
      printf("num %d: '%s'\n", i, result);
   }
   regfree(&preg);
   return 0;
   */
}
