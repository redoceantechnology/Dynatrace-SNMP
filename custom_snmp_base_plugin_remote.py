#from dtmon.dtmonitoringsnmp import DTSNMPMonitoring

import random
import json
import logging
import requests
import re
import socket
import _thread
import time
from requests.auth import HTTPBasicAuth
#from pysnmp.hlapi import *

import ruxit.api.selectors
from ruxit.api.base_plugin import RemoteBasePlugin
from ruxit.api.data import PluginMeasurement, PluginProperty, MEAttribute
from ruxit.api.exceptions import AuthException, ConfigException
from ruxit.api.events import Event, EventMetadata

logger = logging.getLogger(__name__)

class CustomSnmpBasePluginRemote(RemoteBasePlugin):
    def query(self, **kwargs):
        config = kwargs["config"]
        hostname = config["hostname"]
        group_name = config["group"]
        device_type = config["device_type"]
        snmp_version = config["snmp_version"]
        snmp_user = config["snmp_user"]
        auth_protocol = config["auth_protocol"]
        auth_key = config["auth_key"]
        priv_protocol = config["priv_protocol"]
        priv_key = config["priv_key"]
        
        debug_logging = config["debug"]
        if debug_logging:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.WARNING)

        # Temp
        logger.info("hostname - {}".format(hostname))
        logger.info("group_name - {}".format(group_name))
        logger.info("device_type - {}".format(device_type))
        logger.info("snmp_version - {}".format(snmp_version))
        logger.info("snmp_user - {}".format(snmp_user))
        logger.info("auth_protocol - {}".format(auth_protocol))
        logger.info("auth_key - {}".format(auth_key))
        logger.info("priv_protocol - {}".format(priv_protocol))
        logger.info("priv_key - {}".format(priv_key))
        
        # Default port
        port = 161
        
        # If entered as 127.0.0.1:1234, extract the ip and the port
        split_host = hostname.split(":")
        if len(split_host) > 1:
            hostname = split_host[0]
            port = split_host[1]

        # Create the group/device entities in Dynatrace
        g1_name = "{0} - {1}".format(device_type, group_name)
        g1 = self.topology_builder.create_group(g1_name, g1_name)
        e1_name = "{0} - {1}".format(device_type, hostname)
        e1 = g1.create_element(e1_name, e1_name)
        
        # Poll the requested device for IF-MIB
            #cpu_utilisation, memory_utilisation, disk_utilisation
        # Poll the requested device for Host-Resource-MIB
            #incoming_traffic, outgoing_traffic, inbound_error_rate, outbound_error_rate, inbound_loss_rate, outbound_loss_rate

        # Test Plugin
        data = {}
        data['cpu_utilisation'] = random.randint(0,101)
        data['memory_utilisation'] = random.randint(0,101)
        data['disk_utilisation'] = random.randint(0,101)
        data['incoming_traffic'] = random.randint(0,100001)
        data['outgoing_traffic'] = random.randint(0,100001)
        data['inbound_error_rate'] = random.randint(0,101)
        data['outbound_error_rate'] = random.randint(0,101)
        data['inbound_loss_rate'] = random.randint(0,101)
        data['outbound_loss_rate'] = random.randint(0,101)

        # TODO handle dimensions - see official extension code
        #e1.absolute(key = metric["name"], value = split["result"], dimensions = split["dimensions"])

        for key,value in data.items():
            e1.absolute(key=key, value=value)
    