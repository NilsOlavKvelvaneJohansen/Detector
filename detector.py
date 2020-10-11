# coding=utf-8
import hashlib
import json
import os
import sys
from os.path import normpath



def main():
    path = normpath(str(sys.argv[1]).encode('unicode_escape'))
    path = path.decode("utf8")
    #makes a set where all the diiferent hash values will be stored.
    hashSet = set()
    myDict = hashFilesInDir(path, hashSet)
    printDuplicates(myDict, hashSet)
    with open('filesInFolder.json', 'w') as fp:
        json.dump(myDict, fp)


def hashFile(fn):
    f = open(fn, 'r', encoding = "ISO-8859-1")
    h = hashlib.sha256(f.read().encode('utf'))
    f.close()
    return h.hexdigest()

def hashFilesInDir(directoryPath, hashSet, subDirName=""):
    dictionaryHash = {}
    #For each file in folder
    for fileName in os.listdir(directoryPath):
        filePath = normpath(directoryPath + "/" + fileName)
        fileName = subDirName + fileName
        #Calls hashFilesInDir, on subdirectory
        if os.path.isdir(filePath):
            dictionaryHash = appendDict(dictionaryHash, hashFilesInDir(filePath, hashSet, (fileName + "/")))

        elif(os.path.isfile(filePath)):
            fileHash = hashFile(filePath)
            hashSet.add(fileHash)

            if fileHash in dictionaryHash:
                dictionaryHash.get(fileHash).append(fileName)

            else:
                lst = list()
                lst.append(fileName)
                dictionaryHash[fileHash] = lst

            if fileName in dictionaryHash:
                dictionaryHash.get(fileName).append(fileHash)

            else:
                lst = list()
                lst.append(fileHash)
                dictionaryHash[fileName] = lst

    return dictionaryHash

def appendDict(firstDict, secondDict):
    for key in firstDict:
        if (key in secondDict):
            for items in firstDict.get(key):
                secondDict.get(key).append(items)
        else:
            secondDict[key] = firstDict.get(key)
    return secondDict


def printDuplicates(filesDict, hashSet):
    duplicates = list()

    for hash in hashSet:
        if(len(filesDict.get(hash)) > 1):
            duplicates.append(filesDict.get(hash))

    if(len(duplicates) == 1):
        print("Found " + str(len(duplicates)) + " duplicate.\n")
    else:
        print("Found " + str(len(duplicates)) + " duplicates.\n")
    for duplicate in duplicates:
        for file in duplicate:
            print(file)
        print("\n")


if __name__ == '__main__':
    main()
