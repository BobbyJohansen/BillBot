import logging

config = {
    # Your slask API token
    'token': 'xoxb-11487746099-AcIIU6H5t6U6o9MtO6mlaLqc',

    # The log level. Valid options are logging.{DEBUG, INFO, WARNING, ERROR, CRITICAL})
    'loglevel': logging.DEBUG,

    # The log file to write to. By default writes to whatever the pwd is, you probably want
    # to change that. The log goes to stderr unless you uncomment this
    'logfile': 'slask.log'

    # The log file format. This is the default; you can uncomment this line to change it if you want
    # "logformat": '%(asctime)s:%(levelname)s:%(message)s',
}
