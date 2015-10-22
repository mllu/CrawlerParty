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
    statisticsFile = sys.argv[3] if len(sys.argv) > 3 else "overall.out"
    task6_file = sys.argv[3] if len(sys.argv) > 4 else "task6.out"
    task7_file = sys.argv[3] if len(sys.argv) > 5 else "task7.out"
    mapFile1 = open(mapFilename1)
    mapFile2 = open(mapFilename2)
    statisticsFileOut = open(statisticsFile, "w")
    task6 = open(task6_file, "w")
    task7 = open(task7_file, "w")

    mapDict = {}
    task6_only_mapDict = {}
    task7_only_mapDict = {}

    lineNumber = 1
    url = ""
    for line in mapFile1:
        # url = [x.strip() for x in line.split(',')]
        # print url
        # if lineNumber % 2 == 1:
        digest_info = line.strip().split(' ')
        # print digest_info
        count_list = []
        count_list.append(digest_info[1])
        count_list.append('0')
        # else:
        # urls = line.strip().split(',')
        urls = digest_info[2].split(',')
        for url in urls:
            count_list.append(url)
            # print url
        # print 

        mapDict[digest_info[0]] = count_list

        lineNumber += 1
        # if lineNumber > 6:
            # break
    
    lineNumber = 1
    for line in mapFile2:
        digest_info = line.strip().split()
        # print digest_info
        # url[0] as key
        # same digest in task6MapFile
        if digest_info[0] in mapDict:
            mapDict[digest_info[0]][1] = digest_info[1]
        else:
            count_list = ['0']
            count_list.append(digest_info[1])
            mapDict[digest_info[0]] = count_list
            task7_only_mapDict[digest_info[0]] = count_list

        try:
            urls = digest_info[2].split(',')
            for url in urls:
                # print digest_info[0]
                if digest_info[0] in task7_only_mapDict:
                    task7_only_mapDict[digest_info[0]].append(url)
        except:
            continue
        print 

    for key, value in mapDict.iteritems():
        # print key ,value

        if value[1] == '0':
        # if len(value) == 1:
            task6_only_mapDict[key] = value
            print key ,value

            # mapDict[key].append('0')

    keys = sorted(mapDict.keys())
    # print keys
    # for key, value in mapDict.iteritems():
        # print key ,value
    for key in keys:
        statisticsFileOut.write(str(key) + " " + str(mapDict[key]) +"\n")


    print("task6_only_mapDict: ")
    task6.write("task6_only_mapDict:\n")
    # statisticsFileOut.write(str(task6_only_mapDict) + "\n")
    keys = sorted(task6_only_mapDict.keys())
    for key in keys:
        print (str(key) + " " + str(task6_only_mapDict[key]))
        task6.write(str(key) + " " + str(task6_only_mapDict[key]) +"\n")
    print ""
    task6.write("\n")
    task6.close()


    print("task7_only_mapDict: ")
    task7.write("task7_only_mapDict:\n")
    keys = sorted(task7_only_mapDict.keys())
    for key in keys:
        print (str(key) + " " + str(task7_only_mapDict[key]))
        task7.write(str(key) + " " + str(task7_only_mapDict[key]) +"\n")
    print ""
    task7.write("\n")
    task7.close()


    print("overall_mapDict: ")
    statisticsFileOut.write("overall_mapDict:\n")
    keys = sorted(mapDict.keys())
    for key in keys:
        print (str(key) + " " + str(mapDict[key]))
        statisticsFileOut.write(str(key) + " " + str(mapDict[key]) +"\n")
    print ""
    statisticsFileOut.write("\n")
    statisticsFileOut.close()

