#
# Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#

# greengrassHelloWorld.py
# Demonstrates a simple publish to a topic using Greengrass core sdk
# This lambda function will retrieve underlying platform information and send
# a hello world message along with the platform information to the topic 'hello/world'
# The function will sleep for five seconds, then repeat.  Since the function is
# long-lived it will run forever when deployed to a Greengrass core.  The handler
# will NOT be invoked in our example since the we are executing an infinite loop.
#
# This can be found on the AWS IoT Console.

import greengrasssdk
import platform
from threading import Timer
import time
from random import *

# Creating a greengrass core sdk client
client = greengrasssdk.client('iot-data')

# Retrieving platform information to send from Greengrass Core
my_platform = platform.platform()


# When deployed to a Greengrass core, this code will be executed immediately
# as a long-lived lambda function.  The code will enter the infinite while loop
# below.
# If you execute a 'test' on the Lambda Console, this test will fail by hitting the
# execution timeout of three seconds.  This is expected as this function never returns
# a result.

def greengrass_hello_world_run():
    timestamp = str(time.time())
    systolic = randint(90,125)
    diastolic = randint(59,89)
    bpm = randint(60,120)
    bpjson = '{"data_id" : "bp", "ts" : "' + timestamp + '", "systolic" : ' + str(systolic) + ',"diastolic" : ' + str(diastolic) + ',"bpm" : ' + str(bpm) + '}'

    client.publish(topic='healthcare/data', payload=bpjson)

    # Asynchronously schedule this function to be run again in 5 seconds
    Timer(15, greengrass_hello_world_run).start()


# Execute the function above
greengrass_hello_world_run()


# This is a dummy handler and will not be invoked
# Instead the code above will be executed in an infinite loop for our example
def function_handler(event, context):
    return