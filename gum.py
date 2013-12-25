# This program is free and subject to the conditions of the MIT license.
# If you care to read that, here's a link:
# http://opensource.org/licenses/MIT

# To-Do:
# line filtering in process_table_file

#===================== IMPORTS --- SETUP --- GLOBAL VARS ======================
import os
import sys
import re
from csv import DictReader, DictWriter
from collections import *
from itertools import *
from functools import *
from operator import *

#============================ Boolean Functions ===============================

def ID(anything):
    '''This function is mostly intended as a placeholder for functions that the
    user may want to pass.
    I am considering setting this to return the passed object instead of just
    True.'''
    return True

#============================ File I/O Functions ==============================

def list_to_plain_text(inputIter, newline='\n', itemType=str):
    '''Takes a iterable, adds a new line character to the end of each of its
    members and then returns a generator of the newly created items.
    The idea is to convert some sequence that was created with no concern for
    spliting it into lines into something that will produce a text file.
    It is assumed that the only input types will be sequences of lists or
    strings, because these are the only practically reasonable types to be
    written to files.
    It is also assumed that by default the sequence will consist of strings and
    that the lines will be separated by a Unix newline character.
    This behavior can be changed by passing different newline and/or itemType
    arguments.
    '''
    return (l+itemType(newline) for l in inputIter)

def process_table_file(fName, **fmtparams):
    '''Given name of file and some formatting parameters opens the
    corresponding file and prepares it for processing.
    Returns a functor that expects some sort of procedure to run on the file.
    
    Intended as a generic wrapper for opening a file and converting it to a
    csv.DictReader object, then processing it in some way.
    It is assumed that the file being processed is a parseable table with
    values split up into columns separated by either whitespace or commas.
    The formatting parameters are left unspecified on purpose, here are some
    examples:
    - fieldnames -> define your own header for the output 
    - delimiter -> ',' or '\t'
    - dialect 
    One can also read up on them here:
    http://docs.python.org/2/library/csv.html#csv-fmt-params

    :type fName: string
    :param fName: name of file to be processed
    :type fmtparams: dict
    :param fmtparams: parameters used by DictReader to open files
    '''
    
    #first we open the file and create a DictReader object
    with open(fName, 'rU') as f:
        readIn = DictReader(f, **fmtparams)

    #then we define a function that expects some procedure and arguments
    def apply_proc(proc=None, data=[], *misc, **kwmisc):
        '''Wrapper function for other functions (the proc argument).
        If proc is not given, simply returns a list of the lines in the file as
        dictionaries of column_name:column_value.
        If proc is provided it is run on every line in the file along with
        whatever arguments that procedure requires.
        Can be equivalent to Map or Reduce paradigms depending on the specifics
        of the procedure being applied, because 'data' can either be a list
        that has new members appended to it as we loop through the file or it
        can be, for instance, a number that gets modified with every iteration
        over a line and reflects the result of some accumulation procedure.

        :type proc: function or None
        :param proc: the procedure (function) to be run through the file
        :type data: list by default, can be anything.
        :param data: specifies what kind of object the proc should modify as it
        loops through the lines of the file
        
        *misc and **kwmisc refer to (respectively) whatever positional and key word
        arguments are needed for proc.
        '''
        if not proc:
        # if no procedure is passed, simply return the DictReader object
            return readIn
        #otherwise loop over lines in readIn and apply proc to each one
        for line in readIn:
            data = proc(line, data, *misc, **kwmisc)
        return data

    #return this function
    return apply_proc

def proc_dir(dirName, proc, filterfunc=None, data=[], *misc, **kwmisc):
    '''This function applies a procedure 'proc' to all the files in a directory
    that satisfy the conditions specified in 'filterfunc'.
    The latter is by default None, which returns all files in the directory.
    Another default is that this function is basically the functional
    programming "Map" function applied to all relevant files.
    This behavior can be altered, howerver, by changing the 'data' argument and
    making the corresponding changes in the procedure being passed.

    :type dirName: string
    :param dirName: name of directory
    :type proc: function that takes data as an argument and produces something
    of the same type as data
    :param proc: name of directory
    :type filterfunc: function from strings (file names) to truth values
    :param filterfunc: filtering criteria for file names
    :type data: List by default, but can be anything compatible with proc
    :param data: whatever data structure we want to produce as a result of
    processing a directory
    :param *misc: any positional args needed for proc
    :param **kwmisc: any keyword args needed for proc
    '''
    unfiltered = iter(os.listdir(dirName))
    for fName in ifilter(filterfunc, unfiltered):
        data = proc(os.path.join(dirName, fName), data, *misc, **kwmisc)
    return data

def write_to_csv(fName, data, header, **kwargs):
    '''Writes data to file specified by filename. 
    :type fName: string
    :param fName: name of the file to be created
    :type data: list
    :param data: list of dictionaries with no keys absent in the header list
    :type header: list
    :param header: list of columns to appear in the output
    :type **kwargs: dict
    :param **kwargs: some parameters to be passed to DictWriter.
    For instance, restvals specifies what to set empty cells to by default.
    '''
    with open(fName, 'w') as f:
        output = DictWriter(f, header, **kwargs)
        output.writeheader()
        output.writerows(data)

#============================ Data Manipulation Functions =====================

def find_something(smthng, string, All=False):
    '''I'm not sure I should keep this'''
    regex = re.compile(smthng)
    if All:
        return regex.findall(string)
    return regex.findall(string)[0]

def subset_dict(srcDict, relevants, replace=False, exclude=False):
    '''Given some keys and a dictionary returns a dictionary with only
    specified keys. Assumes the keys are in fact present and will raise an
    error if this is not the case'''
    '''Think about ways to make chains of maps: A > B + B > C turns into A >
    C'''
    if replace:
        return dict((relevants[x], srcDict[x]) for x in relevants)
    if exclude:
        try:
            return dict((x, srcDict[x]) for x in srcDict if x not in relevants)
        except Exception as e:
            print 'Unable to process this: ', srcDict
            raise
    try:
        return dict((x, srcDict[x]) for x in relevants)
    except Exception as e:
        print 'Unable to process this: ', srcDict
        raise

#================================= __MAIN__ ===================================
def main():
    pass


#------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

