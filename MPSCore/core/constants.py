# [Copyright]
# SmartPath v1.0
# Copyright 2014-2015 Mountain Pass Solutions, Inc.
# This unpublished material is proprietary to Mountain Pass Solutions, Inc.
# [End Copyright]

kDebugFormatFile = '''
[loggers]
keys=root

[handlers]
keys=console

[formatters]
keys=default

[logger_root]
handlers=console
level=DEBUG

[handler_console]
class=logging.StreamHandler
level=DEBUG
formatter=default
args=(sys.stdout,)

[formatter_default]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=
'''
