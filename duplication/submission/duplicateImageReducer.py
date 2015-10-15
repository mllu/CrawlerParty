import sys
import os
import io
import ast

# from sets import Set
# engineers = Set(['John', 'Jane', 'Jack', 'Janice'])

if __name__ == '__main__':
    def usage():
        sys.stderr.write(
            """SYNOPSIS: python %s <directory> <input_MapFile_task6> <input_MapFile_task7> <output_MapFile_task6> <output_MapFile_task7> <output_overall>\n""" % sys.argv[0])
        sys.exit(1)

    if len(sys.argv) < 3:
       usage()
    # userpath = sys.argv[1] if len(sys.argv) > 1 else usage()
    # is_exact = sys.argv[2] if len(sys.argv) > 2 else "false"
    input_task6_filename = sys.argv[1] if len(sys.argv) > 1 else "6.in"
    input_task7_filename = sys.argv[2] if len(sys.argv) > 2 else "7.in"
    output_task6_filename = sys.argv[3] if len(sys.argv) > 3 else "6.out"
    output_task7_filename = sys.argv[4] if len(sys.argv) > 4 else "7.out"
    output_overall_filename = sys.argv[5] if len(sys.argv) > 5 else "overall.out"
    input_task6 = open(input_task6_filename)
    input_task7 = open(input_task7_filename)
    output_task6 = open(output_task6_filename, "w")
    output_task7 = open(output_task7_filename, "w")
    overall_output = open(output_overall_filename, "w")

    mapDict = {}
    task6_only_mapDict = {}
    task7_only_mapDict = {}

    lineNumber = 0
    for line in input_task6:
        print line
        lineNumber += 1

        if lineNumber % 2 == 1:
            lineArray = line.strip().split(" ")
        else:
            value_list = []
            value_list.append(lineArray[1])
            value_list.append('0')

            urls = eval(line.strip())
            for url in urls:
                # print str(url)
                value_list.append(str(url))
            mapDict[lineArray[0]] = value_list

        if lineNumber > 10:
            break

    print "\n\n"

    lineNumber = 0
    for line in input_task7:
        lineNumber += 1
        if lineNumber % 2 == 1:
            lineArray = line.strip().split(" ")
        else:
            if lineArray[0] in mapDict:
                print lineArray[0]
                mapDict[lineArray[0]][1] = lineArray[1]
                unique = 0
            else:
                value_list = ['0']
                value_list.append(lineArray[1])
                mapDict[lineArray[0]] = value_list
                task7_only_mapDict[lineArray[0]] = value_list
                unique = 1

            urls = eval(line.strip())
            for url in urls:
                mapDict[lineArray[0]].append(str(url))
                if unique == 1:
                    # print str(url)
                    task7_only_mapDict[lineArray[0]].append(str(url))

        if lineNumber > 10:
            break

    print "\n\n"


    for key, value in mapDict.iteritems():
        # print key ,value
        if value[1] == '0':
            task6_only_mapDict[key] = value


    '''
    keys = sorted(mapDict.keys())
    # print keys
    # for key, value in mapDict.iteritems():
        # print key ,value
    for key in keys:
        statisticsFileOut.write(str(key) + " " + str(mapDict[key]) +"\n")
    '''

    print("task6_only_mapDict: ")
    output_task6.write("task6_only_mapDict:\n")
    for key, value in task6_only_mapDict.iteritems():
        # print (str(key) + " " + str(value))
        output_task6.write(str(key) + " " + str(value) +"\n")
    print ""
    output_task6.write("\n")
    output_task6.close()

    print("task7_only_mapDict: ")
    output_task7.write("task7_only_mapDict:\n")
    for key, value in task7_only_mapDict.iteritems():
        # print (str(key) + " " + str(value))
        output_task7.write(str(key) + " " + str(value) +"\n")
    print ""
    output_task7.write("\n")
    output_task7.close()

    print("overall_mapDict: ")
    overall_output.write("overall_mapDict:\n")
    # keys = sorted(mapDict.keys())
    # for key in keys:
    for key, value in mapDict.iteritems():
        # print (str(key) + " " + str(value))
        overall_output.write(str(key) + " " + str(value) +"\n")
    print ("")
    overall_output.write("\n")
    overall_output.close()

