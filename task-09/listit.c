#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    char *dirName = ".";
char *fileNames[1000];
        int fileCount = 0;
int showAll = 0;
      int oneLine = 0;
int reverseOrder = 0;
     int i, j;

  for (i = 1; i < argc; i++) {
      if (strcmp(argv[i], "-a") == 0) {
  showAll = 1;
          } else if (strcmp(argv[i], "-1") == 0) {
    oneLine = 1;
 } else if (strcmp(argv[i], "-r") == 0) {
  reverseOrder = 1;
    } else {
      dirName = argv[i];
 }
    }

     DIR *dp = opendir(dirName);
  if (dp == NULL) {
printf("Could not open directory %s\n", dirName);
     perror("Error");
   return 1;
  }

   struct dirent *entry;
while ((entry = readdir(dp)) != NULL) {
      fileNames[fileCount] = strdup(entry->d_name);
if (fileNames[fileCount] == NULL) {
    printf("Memory allocation failed\n");
    closedir(dp);
         return 1;
  }
fileCount++;
    if (fileCount >= 1000) {
  break;
 }
    }
     closedir(dp);

 if (reverseOrder) {
      for (i = fileCount - 1; i >= 0; i--) {
   if (!showAll) {
         if (fileNames[i][0] == '.') {
      continue;
   }
     }
     printf("%s", fileNames[i]);
  if (oneLine) {
printf("\n");
  } else {
     printf(" ");
 }
  }
} else {
  for (i = 0; i < fileCount; i++) {
       if (!showAll) {
    if (fileNames[i][0] == '.') {
   continue;
    }
  }
 printf("%s", fileNames[i]);
       if (oneLine) {
     printf("\n");
       } else {
printf(" ");
    }
 }
 }

 if (!oneLine) {
        printf("\n");
 }

     for (j = 0; j < fileCount; j++) {
  free(fileNames[j]);
 }

   return 0;
}
