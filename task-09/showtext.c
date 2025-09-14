#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
char *filename = NULL;
int lineNumbers = 0;
 int squeezeEmpty = 0;
int showEndMarker = 0;

for (int i = 1; i < argc; i++)
{
  if (strcmp(argv[i], "-n") == 0)
    lineNumbers = 1;
  else if (strcmp(argv[i], "-s") == 0)
    squeezeEmpty = 1;
  else if (strcmp(argv[i], "-e") == 0)
    showEndMarker = 1;
  else
    filename = argv[i];
}

if (filename == NULL)
{
  fprintf(stderr, "Error: No input file\n");
  return 1;
}

FILE *file = fopen(filename, "r");
if (file == NULL)
{
  perror("Failed to open file");
  return 1;
}

char buffer[1024];
int currentLine = 0;
int lastWasBlank = 0;

while (fgets(buffer, sizeof(buffer), file))
{
  int isBlank = (strcmp(buffer, "\n") == 0);

  if (squeezeEmpty && isBlank && lastWasBlank)
    continue;

  lastWasBlank = isBlank;

  currentLine++;

  if (lineNumbers)
    printf("%6d  ", currentLine);

  size_t len = strlen(buffer);
  if (showEndMarker && len > 0 && buffer[len - 1] == '\n')
  {
    buffer[len - 1] = '\0';
    printf("%s$\n", buffer);
  }
  else
  {
    printf("%s", buffer);
  }
}

fclose(file);
return 0;
}
