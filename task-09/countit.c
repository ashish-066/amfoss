#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
char *filename = NULL;
int countlines = 0;
 int countwords = 0;
int countletters = 0;

for (int i = 1; i < argc; i++)
{
 if (strcmp(argv[i], "-l") == 0)
   countlines = 1;
 else if (strcmp(argv[i], "-w") == 0)
   countwords = 1;
 else if (strcmp(argv[i], "-c") == 0)
   countletters = 1;
 else
   filename = argv[i];
}

if (filename == NULL)
{
 fprintf(stderr, "No input file provided.\n");
 return 1;
}

FILE *file = fopen(filename, "r");
if (file == NULL)
{
 perror("Error opening file");
 return 1;
}

char line[1024];
int linecount = 0;
int wordcount = 0;
int lettercount = 0;

while (fgets(line, sizeof(line), file))
{
 linecount++;

 int inword = 0;

 for (int i = 0; line[i] != '\0'; i++)
 {
  if (isalpha(line[i]))
  {
   lettercount++;
   if (!inword)
   {
    wordcount++;
    inword = 1;
   }
  }
  else
  {
   inword = 0;
  }
 }
}

if (countlines)
 printf("%d\n", linecount);
if (countwords)
 printf("%d\n", wordcount);
if (countletters)
 printf("%d\n", lettercount);

fclose(file);
return 0;
}
