#!/usr/bin/env python
import os
import sys
import datetime
import subprocess
import re
from collections import deque




# this function takes a date as string and a list of filepaths and returns
# a new list containing the paths of files last modified before the given date
def beforedate(date, flist):
    newlist = []
    if len(date) == 8:  # if date is given in the form YYYYMMDD
        if re.match("^\d{8}$", date):
            for file in flist:
                modtime = os.path.getmtime(file)  # get modification time of the file
                mtime = datetime.datetime.fromtimestamp(modtime).strftime('%Y%m%d')
                mtime = int(mtime)
                date = int(date)
                if (mtime <= date):  # check if modfication time is before the date
                    newlist.append(file)
        else:
            newlist = []
            print("Wrong date format!")
    elif len(date) == 15:  # if date is given in the form YYYYMMDDTHHMMSS
        if re.match("^\d{8}T\d{6}$", date):
            for file in flist:
                modtime2 = os.path.getmtime(file)
                mtime2 = datetime.datetime.fromtimestamp(modtime2).strftime('%Y%m%dT%H%M%S')
                a, b = mtime2.split("T")  # split the mod. date to YYYYMMDD and HHMMSS
                a = int(a)
                b = int(b)
                c, d = date.split("T")  # split given date to YYYYMMDD and HHMMSS
                c = int(c)
                d = int(d)
                if (a < c):  # first check according to day of modification
                    newlist.append(file)
                elif (a == c):  # if it is modified in the given date check according to hour and seconds
                    if (b <= d):
                        newlist.append(file)
        else:
            newlist = []
            print("Wrong date format")

    else:
        newlist = []
        print("Wrong date format")
    return newlist


# this function takes a date as string and a list of filepaths and returns
# a new list containing the paths of files last modified after the given date
# the way it is impemented is similar with the beforedate function
def afterdate(date, flist):
    newlist = []
    if len(date) == 8:
        if re.match("^\d{8}$", date):
            for file in flist:
                modtime = os.path.getmtime(file)
                mtime = datetime.datetime.fromtimestamp(modtime).strftime('%Y%m%d')
                mtime = int(mtime)
                date = int(date)
                if (mtime >= date):
                    newlist.append(file)
        else:
            newlist = []
            print("Wrong date format")
    elif len(date) == 15:
        if re.match("^\d{8}T\d{6}$", date):
            for file in flist:
                modtime2 = os.path.getmtime(file)
                mtime2 = datetime.datetime.fromtimestamp(modtime2).strftime('%Y%m%dT%H%M%S')
                a, b = mtime2.split("T")
                a = int(a)
                b = int(b)
                c, d = date.split("T")
                c = int(c)
                d = int(d)
                if (a > c):
                    newlist.append(file)
                elif (a == c):
                    if (b >= d):
                        newlist.append(file)
        else:
            newlist = []
            print("Wrong date format")
    else:
        newlist = []
        print("Wrong date format")
    return newlist


# this funciton take a size as string,and a listof filepaths and returns a new list containing
# the paths of files whose sizes are bigger than the given size
def bigger(size, flist):
    newlist = []
    if isinstance(size, str):
        s = size[-1:]

        # check if size is in true format
        if (re.match("^\d+K$", size)):  # if size is given in kilobytes(ex:size="3K")
            a, b = size.split("K")  # take the number before the letter and cast it to int
            a = int(a)
            a = a * 1024  # multiply with 1024 since getsize function returns in bytes
        elif (re.match("^\d+M$", size)):  # if size is given in megabytes(ex:size="5M")
            a, b = size.split("M")
            a = int(a)
            a = a * 1024 * 1024
        elif (re.match("^\d+G$", size)):  # if size is given in gigabytes(ex:size="5G")
            a, b = size.split("G")
            a = int(a)
            a = a * 1024 * 1024 * 1024
        elif (re.match("^\d+$", size)):
            a = int(size)  # if size is given in bytes (no letter in given size) ,cast size to int


        else:
            print("Wrong size format!")
            flist = []

            # variable "a" records the given size as integer in bytes

        for file in flist:  # here we determine every file having size bigger than "a"

            filesize = os.path.getsize(file)
            if (filesize >= a):
                newlist.append(file)

    return newlist


# this funciton take a size as string,and a listof filepaths and returns a new list containing
# the paths of files whose sizes are smaller than the given size
# the way of implementation is similar to function "bigger"
def smaller(size, flist):
    newlist = []
    if isinstance(size, str):
        s = size[-1:]

        if (re.match("^\d+K$", size)):
            a, b = size.split("K")
            a = int(a)
            a = a * 1024
        elif (re.match("^\d+M$", size)):
            a, b = size.split("M")
            a = int(a)
            a = a * 1024 * 1024
        elif (re.match("^\d+G$", size)):
            a, b = size.split("G")
            a = int(a)
            a = a * 1024 * 1024 * 1024
        elif (re.match("^\d+$", size)):
            a = int(size)
        else:
            print("Wrong size format!")
            flist = []

        for file in flist:
            st = os.stat(file)
            filesize = st.st_size
            if (filesize <= a):
                newlist.append(file)

    return newlist


# given a list of paths of files ,this function uses os command to delete these files
def deletefiles(flist):
    newlist = []
    for file in flist:
        command = "rm " + "\"" + file + "\""  # use command "rm [filepath]"
        os.system(command)
    return newlist


# given a name (zipfile) and a list of file paths ,this function packs those files in zipfile
# with the given name
def zip(zipfile, flist):
    if (zipfile.endswith(".zip")):  # check if given name is appropriate for a zip file
        command = "zip " + zipfile  # use command "zip [zip file name] [file list]"
        for file in flist:
            command += " " + "\"" + file + "\""

        os.system(command)
    else:
        print("Invalid zip file name!It should end with .zip")
        flist = []
    return flist


# given a list of filepaths,this function returns a new list of paths of files.
# new list contains the files whose names are same in duplicate sets seperated by "-----"
# the list is sorted with respect to file names

def duplname(flist):
    namelist = []  # stores the duplicate sets
    uniquenam = 0  # stores the number of unique named files
    flist = sorted(flist, key=lambda g: g.split("/")[-1])  # sort filepaths with respect to file names

    for i in range(len(flist) - 1):  # checks if the next file has the same name
        # if it doesn't, seperates them with "-----"
        currf = flist[i]
        curr = currf.split("/")[-1]
        next = flist[i + 1].split("/")[-1]
        namelist.append(currf)
        if curr != next:
            uniquenam += 1
            namelist.append("-----")

    if len(flist) != 0:
        uniquenam += 1

        namelist.append(flist[-1])  # add the last element since it is excluded in for loop above


    return (namelist, uniquenam)  # return a tuple containing the filepaths and no of unique named files





# given a list of filepaths,this function returns a new list of paths of files.
# new list contains the files whose contents are same in duplicate sets seperated by "-----"
# every set is sorted with respect to filenames


def duplcont(flist):
    namelist = []  # stores duplicate content files
    written = []  # stores the list places of the files which are already appended to namelist
    shasums = []  # stores shasums of files
    uniqno = 0  # number of unique content files in flist
    uniqsize = 0  # total size of the files with unique content

    for i in range(len(flist)):  # this loop stores shasums of files in flist in the list "shasums"
        com = "shasum " + "\"" + flist[i] + "\" "
        out = subprocess.check_output(com, shell=True)  # use command "shasum [file]
        out = str(out)
        shas = out.split(" ")  # since output is in the form [shasum][filepath]
        shasums.append(shas[0])

    for i in range(len(flist)):  # for every file check the other files to find the ones with same content
        if (i not in written):
            uniqno += 1
            current = flist[i]  # current is the file to be considered in this step of for loop
            uniqsize += os.path.getsize(current)
            duplset = []  # duplicate set of the current file
            duplset.append(current)

            for j in range(len(flist)):  # search through files to find duplicate content
                if (i != j):

                    if (shasums[i] == shasums[j]):  # check if shasums of fist[i] and flist[j] are equal
                        duplset.append(flist[j])
                        written.append(j)

            duplset = sorted(duplset, key=lambda g: g.split("/")[-1])  # so that we get each duplicate set sorted
            namelist.append("-----")
            namelist.extend(duplset)

    return (namelist, uniqno, uniqsize)




def match(flist, reg):  # given a list of filepaths and a regex pattern,returns a new list of paths of files
    # whose names match the given pattern
    newlist = []
    for file in flist:
        if (re.match(reg, file.split("/")[-1])):
            newlist.append(file)

    return newlist


#                                          THE MAIN PART OF PROGRAM

check = False  # is true if we found a directory in the sys.argv
valid = True  # is true if arguments are in valid form
dirbegin = 0  # points the place of the first directory in the list sys.argv

for i in range(len(sys.argv)):  # this loop checks if arguments are in valid form

    if check and os.path.isdir(sys.argv[i]) == False:  # if we found a directory path in the previous arguments
        # and now we found an argument which is not a directory path
        # the arguments are not in the form:filelist[options]{dirlist]
        valid = False

    if os.path.isdir(sys.argv[i]):
        if not check:
            dirbegin = i  # point the place of the first directory path argument
        check = True  # indicate we found a directory path in arguments

if not valid:
    print("Give arguments in the form : filelist [options][directorylist]")

if valid:
    cwd = os.getcwd()  # cwd stores current directory
    qlist = deque()  # qlist stores directory paths given in sys.argv

    if dirbegin != 0:  # dirbegin=0 indicates no directory path in arguments.Hence we use current directory
        for i in range(dirbegin, len(sys.argv)):
            qlist.append(sys.argv[i])  # if dirbegin!=0 ,we store directory paths in qlist
    else:
        qlist.append(cwd)

    visitedsize = 0  # total size of traversed files
    visited = 0  # number of visited files

    filelist = []  # stores all files under the given directories

    # directory traversal
    while qlist:
        currentdir = qlist.popleft()
        dircontents = os.listdir(currentdir)
        for name in dircontents:
            currentitem = currentdir + "/" + name
            if os.path.isdir(currentitem):
                qlist.append(currentitem)
            else:
                st = os.stat(currentitem)
                visitedsize += st.st_size
                visited += 1
                filelist.append(currentitem)

    length = len(sys.argv)
    filepath = sys.argv[length - 1]

    sta = False  # true if -stats option is used
    dupln = False  # true if -duplname option is used
    duplc = False  # true if -duplcont option is used
    zipp=False
    delet=False
    for i in range(1, length):  # search through the arguments and update filelist according to options,
        # using the functions defined above
        currarg = sys.argv[i]
        if (currarg == "-before"):
            filelist = beforedate(sys.argv[i + 1], filelist)
            i += 1
        elif (currarg == "-after"):
            filelist = afterdate(sys.argv[i + 1], filelist)
            i += 1
        elif (currarg == "-match"):
            filelist = match(filelist, sys.argv[i + 1])
            i += 1
        elif (currarg == "-bigger"):
            filelist = bigger(sys.argv[i + 1], filelist)
            i += 1
        elif (currarg == "-smaller"):
            filelist = smaller(sys.argv[i + 1], filelist)
            i += 1
        elif (currarg == "-delete"):
            delet=True
            if zipp or dupln or duplc:
                filelist=[]
                print("Delete option is not allowed with zip or duplcont or duplname.Files are not deleted")
            else:
                deletefiles(filelist)
        elif (currarg == "-zip"):
            zipp=True
            if delet:
                filelist=[]
                print("Files are deleted.Zip option is ignored.Both delete and zip options are not allowed")
            else:
                zip(sys.argv[i + 1], filelist)
                i += 1
        elif (currarg == "-duplcont"):
            if delet:
                filelist=[]
                print("Files are deleted.Duplcont option is ignored.Both duplcont and delete options are not allowed")
            else:
                duplc = True

        elif (currarg == "-duplname"):
            if delet:
                filelist=[]
                print("Files are deleted.Duplname option is ignored.Both duplname and delete options are not allowed")
            else:
                dupln = True
        elif (currarg == "-stats"):
            sta = True
        elif (currarg == "-nofilelist"):
            filelist = []

    uniquename = 0  # no of files with unique names
    nouniq = 0  # no of files with unique contents
    sizeuniq = 0  # total size of files with unique content

    if (duplc):  # after the other options are executed;if duplcont option is in arguments,group filepaths
        # according to contents
        tup = duplcont(filelist)
        filelist = tup[0]
        nouniq = tup[1]
        sizeuniq = tup[2]

    elif (dupln):
        tup2 = duplname(filelist)
        filelist = tup2[0]
        uniquename = tup2[1]

    for f in filelist:
        print(f)  # print file list

    if (sta):  # if -stats option is used ,print statistics of traversal

        print("----------------")
        print("Total size of files visited:" + str(visitedsize))
        print("Total number of files visited:" + str(visited))
        listed = 0
        listedsize = 0
        for file in filelist:
            if (file != "-----"):
                listed += 1
                listedsize += os.path.getsize(file)

        print("Total size of files listed:" + str(listedsize))
        print("Total number of files listed:" + str(listed))

        if (dupln):  # if both -stats and duplname options are used
            print("Total number of files with unique names:" + str(uniquename))



        elif (duplc):  # if both -stats and -duplcon options are used
            print("Total number of unique files:" + str(nouniq))
            print("Total size of unique files:" + str(sizeuniq))



