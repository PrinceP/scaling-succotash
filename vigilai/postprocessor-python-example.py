import os
import sys
import socket
import signal
import logging
import logging.handlers
import configparser

import requests
import json

# Add the nxai-utilities python utilities
if getattr(sys, "frozen", False):
    script_location = os.path.dirname(sys.executable)
elif __file__:
    script_location = os.path.dirname(__file__)
sys.path.append(os.path.join(script_location, "../nxai-utilities/python-utilities"))
import communication_utils


CONFIG_FILE = os.path.join(script_location, "..", "etc", "plugin.example.ini")

# Set up logging
LOG_FILE = os.path.join(script_location, "..", "etc", "plugin.example.log")

# Initialize plugin and logging, script makes use of INFO and DEBUG levels
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - example - %(message)s",
    filename=LOG_FILE,
    filemode="w",
)

# The name of the postprocessor.
# This is used to match the definition of the postprocessor with routing.
Postprocessor_Name = "Python-Example-Postprocessor"

# The socket this postprocessor will listen on.
# This is always given as the first argument when the process is started
# But it can be manually defined as well, as long as it is the same as the socket path in the runtime settings
Postprocessor_Socket_Path = "/tmp/python-example-postprocessor.sock"

# Data Types
# 1:  //FLOAT
# 2:  //UINT8
# 3:  //INT8
# 4:  //UINT16
# 5:  //INT16
# 6:  //INT32
# 7:  //INT64
# 8:  //STRING
# 9:  //BOOL
# 11: //DOUBLE
# 12: //UINT32
# 13: //UINT64


def config():
    logger.info("Reading configuration from:" + CONFIG_FILE)

    try:
        configuration = configparser.ConfigParser()
        configuration.read(CONFIG_FILE)

        configured_log_level = configuration.get(
            "common", "debug_level", fallback="INFO"
        )
        set_log_level(configured_log_level)

        for section in configuration.sections():
            logger.info("config section: " + section)
            for key in configuration[section]:
                logger.info("config key: " + key + " = " + configuration[section][key])

    except Exception as e:
        logger.error(e, exc_info=True)

    logger.debug("Read configuration done")


def set_log_level(level):
    try:
        logger.setLevel(level)
    except Exception as e:
        logger.error(e, exc_info=True)


def signal_handler(sig, _):
    logger.info("Received interrupt signal: " + str(sig))
    sys.exit(0)


def main():
    # Start socket listener to receive messages from NXAI runtime
    server = communication_utils.startUnixSocketServer(Postprocessor_Socket_Path)

    # Wait for messages in a loop
    while True:
        # Wait for input message from runtime
        logger.debug("Waiting for input message")

        try:
            input_message, connection = communication_utils.waitForSocketMessage(server)
            logger.debug("Received input message")
        except socket.timeout:
            # Request timed out. Continue waiting
            continue

        # Parse input message
        input_object = communication_utils.parseInferenceResults(input_message)

        # Use pformat to format the deep object
        # formatted_unpacked_object = pformat(input_object)
        # logging.debug(f'Unpacked:\n\n{formatted_unpacked_object}\n\n')

        # Add extra bbox
        if "BBoxes_xyxy" not in input_object:
            input_object["BBoxes_xyxy"] = {}
        #input_object["BBoxes_xyxy"]["test"] = [100.0, 100.0, 200.0, 200.0]

        logger.info("Sending a request to server")
        # URL of the Flask server
        url = 'http://127.0.0.1:5000/add_message'
        if not isinstance(input_object, bytes):
            logger.info(input_object)
            modified_input_object = {}
            modified_input_object['Timestamp'] = input_object['Timestamp']
            modified_input_object['BBoxes_xyxy'] = input_object['BBoxes_xyxy']
            modified_input_object['DeviceName'] = input_object['DeviceName']
            modified_input_object['Width'] = input_object['Width']
            modified_input_object['Height'] = input_object['Height']

            json_data = json.dumps(modified_input_object)
            headers = {'Content-Type': 'application/json'}
            logger.info(json_data)
            try:
                response = requests.post(url, data=json_data, headers=headers)
            except:
                logger.info("Not sent")
            logger.info("Sent")
        else:
            logger.info("Byte data")

        # Write object back to string
        output_message = communication_utils.writeInferenceResults(input_object)

        # Send message back to runtime
        communication_utils.sendMessageOverConnection(connection, output_message)


if __name__ == "__main__":
    ## initialize the logger
    logger = logging.getLogger(__name__)

    ## read configuration file if it's available
    config()

    logger.info("Initializing example plugin")
    logger.debug("Input parameters: " + str(sys.argv))

    # Parse input arguments
    if len(sys.argv) > 1:
        Postprocessor_Socket_Path = sys.argv[1]
    # Handle interrupt signals
    signal.signal(signal.SIGINT, signal_handler)
    # Start program
    try:
        main()
    except Exception as e:
        logger.error(e, exc_info=True)
