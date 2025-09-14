#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
int numberlines = 0;
   int invertmatch = 0;
int countflag = 0;
char *pattern = NULL;
   char *filename = NULL;

for (int i = 1; i < argc; i++) {
   if (strcmp(argv[i], "-n") == 0) {
numberlines = 1;
  } else if (strcmp(argv[i], "-v") == 0) {
invertmatch = 1;
  } else if (strcmp(argv[i], "-c") == 0) {
countflag = 1;
 } else if (pattern == NULL) {
 pattern = argv[i];
 } else {
filename = argv[i];
 }
}

if (pattern == NULL || filename == NULL) {
 fprintf(stderr, "Usage: %s [options] pattern file\n", argv[0]);
return 1;
}

FILE *file = fopen(filename, "r");
if (file == NULL) {
 perror("Error opening file");
 return 1;
}

char line[1024];
int linenum = 0;
int matchcount = 0;

while (fgets(line, sizeof(line), file)) {
 linenum++;
 int match = (strstr(line, pattern) != NULL);
 if (invertmatch)
   match = !match;
 if (match) {
  matchcount++;
  if (!countflag) {
    if (numberlines)
      printf("%d:%s", linenum, line);
    else
      printf("%s", line);
  }
 }
}

if (countflag) {
  printf("%d\n", matchcount);
}

fclose(file);
return 0;
}
