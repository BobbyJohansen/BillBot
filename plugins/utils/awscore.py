import os
from os.path import expanduser
from boto.exception import *
import glob

###########################
### AWS GENERAL HELPERS ###
###########################

def getConnection(connectClass):
    """
    Gets a connection to AWS using the connectClass
    If auth isn't set up, prompts user for authentication
    :param connectClass: Class to connect with
    :return: Live connection to connectionClass
    """
    conn = 0
    # Loop until the connection is established
    while type(conn) == int:
        try:
            conn = connectClass()
        # This will happen if the auth info is invalid or missing
        except NoAuthHandlerFound, e:
            print "Could not connect to AWS with current auth info..."
            print e.message
            homeDir = expanduser("~")
            os.chdir(homeDir)
            createAwsAuth()
        # this should never happen
        except:
            print "Could not establish connection with AWS..."
            exit(-1)
    return conn

# Create or update AWS Auth file
def createAwsAuth():
    """
    Creates an auth file for AWS
    :return: None
    """
    # Cross platform method of finding home
    homeDir = expanduser("~")
    os.chdir(homeDir)

    def writeAuth():
        fs = open("credentials", 'w')
        fs.write("[default]\n")
        fs.write("aws_access_key_id="+str(raw_input("Enter aws_access_key:"))+"\n")
        fs.write("aws_secret_access_key="+str(raw_input("Enter aws_secret_access_key:"))+"\n")
        fs.close()

    # Check if there is a .aws folder in home
    if len(glob.glob(".aws")) == 0:
        # Create one...
        try:
            os.mkdir(".aws")
            print "Created .aws directory in: " + homeDir
        except:
            print "Could not create .aws directory in:" + homeDir
            exit(-1)

    os.chdir(".aws")
    # Check if the credentials file exists
    if len(glob.glob("credentials")) == 0:
        print "Creating new credentials file..."
        writeAuth()
    else:
        print "You already have a credentials file..."
        # Update it?
        if raw_input("Would you like to update your credentials? (y/n)").lower()[0] == 'y':
            writeAuth()

