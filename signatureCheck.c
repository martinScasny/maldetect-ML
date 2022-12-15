#include "Winnt.h"
#include "stdint.h"
#include <stdio.h>
#include <stdlib.h>

int main()
{
  FILE *fp;
  char *filename = "sample";
  const char *dosHeader = NULL;
  int i;
  int data[10];
  

  fp = fopen(filename, "rb");
  if (fp == NULL) {
    printf("File not found\n");
    return 1;
  }
  dosHeader = mmap(0, size, PROT_READ, MAP_PRIVATE, fp, 0);
  struct _IMAGE_DOS_HEADER *dosHeaderPtr = (struct _IMAGE_DOS_HEADER *)dosHeader;
  struct _IMAGE_NT_HEADERS *ntHeaderPtr = (struct _IMAGE_NT_HEADERS *)(dosHeaderPtr + dosHeaderPtr->e_lfanew);
  struct _IMAGE_OPTIONAL_HEADER *optHeaderPtr = (struct _IMAGE_OPTIONAL_HEADER *)(ntHeaderPtr + 1);
  struct _DATA_DIRECTORY *dataDirectoryPtr = (struct _DATA_DIRECTORY *)(optHeaderPtr + 5);
  struct _IMAGE_DIRECTORY_ENTRY *aCertTable = (struct _IMAGE_DIRECTORY_ENTRY *)(dataDirectoryPtr + 1);
  DWORD sizeCertTable = (DWORD)(aCertTable[0].Size);

  for (i = 0; i < sizeCertTable; i++) {
    
  }
  
  fclose(fp);

  return 0;
}

  