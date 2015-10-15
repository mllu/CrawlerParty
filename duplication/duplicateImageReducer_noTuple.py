import sys
import os
import io
import ast

if __name__ == '__main__':
    def usage():
        sys.stderr.write(
            """SYNOPSIS: python %s <directory> <mapFile_task6> <duplicateStatOutput> \n""" % sys.argv[0])
        sys.exit(1)


    # userpath = sys.argv[1] if len(sys.argv) > 1 else usage()
    # is_exact = sys.argv[2] if len(sys.argv) > 2 else "false"
    mapFilename1 = sys.argv[1] if len(sys.argv) > 1 else "mapFlie1"
    mapFilename2 = sys.argv[2] if len(sys.argv) > 2 else "mapFlie2"
    statisticsFile = sys.argv[3] if len(sys.argv) > 3 else "duplicateImageReducer.out"
    mapFile1 = open(mapFilename1)
    mapFile2 = open(mapFilename2)
    statisticsFileOut = open(statisticsFile, "w")

    mapDict = {}
    task6_only_mapDict = {}
    task7_only_mapDict = {}

    # with open(inputFile1) as f:
    lineNumber = 0
    for line in mapFile1:
       lineNumber += 1
       if lineNumber % 2 == 1:
           lineArray = line.strip().split(" ")
       else:
           mapDict[lineArray[0]] = (lineArray[1], ast.literal_eval(line.strip()))
    
    '''
    for line in mapFile1:
        url = line.strip().split()
        # print url
        count_list = []
        count_list.append(url[1])
        mapDict[url[0]] = count_list
    '''

    
    lineNumber = 0
    for line in mapFile2:
        lineNumber += 1
        if lineNumber % 2 == 1:
            lineArray = line.strip().split(" ")
        else:
            if lineArray[0] in mapDict:
                mapDict[lineArray[0]][1] = lineArray[1]
                mapDict[lineArray[0]].append(lineArray[1], ast.literal_eval(line.strip()))
            else:
                mapDict[lineArray[0]] = ('0', lineArray[1], ast.literal_eval(line.strip()))
                task7_only_mapDict[lineArray[0]] = ('0', lineArray[1], ast.literal_eval(line.strip()))
        '''
        url = line.strip().split()
        # print url
        if url[0] in mapDict:
            mapDict[url[0]].append(url[1])
        else:
            count_list = ['0']
            count_list.append(url[1])
            mapDict[url[0]] = count_list
            task7_only_mapDict[url[0]] = count_list
        '''

    
    for key, value in mapDict.iteritems():
        # print key ,value
        # if len(value) == 1:
        if value[1] == '0':
            task6_only_mapDict[lineArray[0]] = ('0', lineArray[1], ast.literal_eval(line.strip()))
            # task6_only_mapDict[key] = value
            # mapDict[key].append('0')

    '''
    keys = sorted(mapDict.keys())
    # print keys
    # for key, value in mapDict.iteritems():
        # print key ,value
    for key in keys:
        statisticsFileOut.write(str(key) + " " + str(mapDict[key]) +"\n")
    '''

    print("task6_only_mapDict: ")
    statisticsFileOut.write("task6_only_mapDict:\n")
    # statisticsFileOut.write(str(task6_only_mapDict) + "\n")
    keys = sorted(task6_only_mapDict.keys())
    for key in keys:
        print (str(key) + " " + str(task6_only_mapDict[key]))
        statisticsFileOut.write(str(key) + " " + str(task6_only_mapDict[key]) +"\n")
    print ""
    statisticsFileOut.write("\n")


    print("task7_only_mapDict: ")
    statisticsFileOut.write("task7_only_mapDict:\n")
    keys = sorted(task7_only_mapDict.keys())
    for key in keys:
        print (str(key) + " " + str(task7_only_mapDict[key]))
        statisticsFileOut.write(str(key) + " " + str(task7_only_mapDict[key]) +"\n")
    print ""
    statisticsFileOut.write("\n")

    print("overall_mapDict: ")
    statisticsFileOut.write("overall_mapDict:\n")
    keys = sorted(mapDict.keys())
    for key in keys:
        print (str(key) + " " + str(mapDict[key]))
        statisticsFileOut.write(str(key) + " " + str(mapDict[key]) +"\n")
    print ""
    statisticsFileOut.write("\n")


    statisticsFileOut.close()

