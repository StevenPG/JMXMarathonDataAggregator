"""
commandlineargumentshandler.py
Author: Steven Gantz
Date: 11/22/2016

This class specifically handles inputs (assuming they are formatted correctly)
and leaves them available for retrieval by other parts of the application. This
allows the removal of generic "sys.argv[i]" calls in favor of specific names.
"""

class CommandLineArgumentsHandler:
    """ Command line arguments object for easy reading """
    
    def __init__(self, args):
        """ Constructor builds the whole object """
        self.totalArgs = len(args)
        self.marathonURL = args[1]
        self.appid = args[2]
        self.totalports = args[3]

    def __str__(self):
        """ Python toString command for easy debugging """
        return "CLA obj [" + self.marathonURL + ", " + self.appid + ", " + str(self.totalports) + "]"
