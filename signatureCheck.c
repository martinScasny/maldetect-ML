// #include "Winnt.h"
#include "stdint.h"
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <tchar.h>

// #include "Memoryapi.h"

#define BUFFSIZE 1024

int main()
{
  char *filename = "sample";

  OFSTRUCT buffer = {0};
  HANDLE hFile = OpenFile(filename, &buffer, OF_READ);
  HANDLE hMap;
  LPVOID lpBasePtr;
  LARGE_INTEGER liFileSize;

  if (!GetFileSizeEx(hFile, &liFileSize)) {
      fprintf(stderr, "GetFileSize failed with error %d\n", GetLastError());
      CloseHandle(hFile);
      return 1;
  }

  if (liFileSize.QuadPart == 0) {
      fprintf(stderr, "File is empty\n");
      CloseHandle(hFile);
      return 1;
  }

  hMap = CreateFileMapping(
      hFile,
      NULL,                          // Mapping attributes
      PAGE_READONLY,                 // Protection flags
      0,                             // MaximumSizeHigh
      0,                             // MaximumSizeLow
      NULL);                         // Name
  if (hMap == 0) {
      fprintf(stderr, "CreateFileMapping failed with error %d\n", GetLastError());
      CloseHandle(hFile);
      return 1;
  }

  lpBasePtr = MapViewOfFile(
      hMap,
      FILE_MAP_READ,         // dwDesiredAccess
      0,                     // dwFileOffsetHigh
      0,                     // dwFileOffsetLow
      0);                    // dwNumberOfBytesToMap
  if (lpBasePtr == NULL) {
      fprintf(stderr, "MapViewOfFile failed with error %d\n", GetLastError());
      CloseHandle(hMap);
      CloseHandle(hFile);
      return 1;
  }

  // Display file content as ASCII charaters
  struct _IMAGE_DOS_HEADER *dosHeaderPtr = (struct _IMAGE_DOS_HEADER *)lpBasePtr;
  struct _IMAGE_NT_HEADERS *ntHeaderPtr = (struct _IMAGE_NT_HEADERS *)(dosHeaderPtr + dosHeaderPtr->e_lfanew);
  struct _IMAGE_OPTIONAL_HEADER *optHeaderPtr = (struct _IMAGE_OPTIONAL_HEADER *)(ntHeaderPtr + 1);
  struct _DATA_DIRECTORY *dataDirectoryPtr = (struct _DATA_DIRECTORY *)(optHeaderPtr + 5);
  struct _IMAGE_DIRECTORY_ENTRY *aCertTable = (struct _IMAGE_DIRECTORY_ENTRY *)(dataDirectoryPtr);
  DWORD sizeCertTable = (((ntHeaderPtr->OptionalHeader).DataDirectory)[5]).Size;
  UnmapViewOfFile(lpBasePtr);
  CloseHandle(hMap);
  CloseHandle(hFile);

  printf("\nDone\n");

  return 0;
}

  