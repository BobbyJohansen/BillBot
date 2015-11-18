import os
from awscore import getConnection
from boto.dynamodb2.layer1 import DynamoDBConnection

########################
### DYNAMODB HELPERS ###
########################

def getDynamoEnvironment():
    """
    Searches for environment name in environment variables, falls back to asking user
    :return: EnvironmentName as str
    """
    env = ""
    if "ENV.NAME" in os.environ.keys():
        print "Pulling prefix from env.name..."
        env = os.environ["ENV.NAME"]
    elif "ENV_PART" in os.environ.keys():
        print "Pulling prefix from env_part"
        env = os.environ["ENV_PART"]
    else:
        print "Environment does not specify table prefix..."
        print "Cannot continue...."
        exit(-1)

    return env

#Gets a live connection to Dynamodb
def getDynamodbConnection():
    """
    Uses getConnection to spawn a DynamoDB connection
    :return: Returns a live connection to Dynamo
    """
    return getConnection(DynamoDBConnection)

# Build a list of available tables on the connection
def buildDynamoTableList(connection):
    """
    Builds a list of tables in the current region for Dynamo
    :param connection: Live connection to use to query tables
    :return: [ table1, table2, table3 ... ]
    """
    retList = []
    t1 = connection.list_tables(limit=100)
    t2 = t1
    while len(t2["TableNames"]) > 0:
        retList += t1["TableNames"]
        t2 = connection.list_tables(t1["TableNames"][-1], limit=100)
        t1 = t2
    # Quick gross way to get rid of duplicates
    return list(set(retList))
