import sys, importlib, json
from result_output import *
import logging
import datetime
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.cosmosdb import CosmosDBManagementClient
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.mgmt.privatedns import PrivateDnsManagementClient

class BlueskyAzureAppActivity():
    # Resource names - customize based on assessment
    resource_group_name = "bluesky-rg"
    application_gateway_name = "bluesky-appgw"

    def testcase_check_application_gateway_name(self, test_object, credentials, subscriptionId):
        logging.info("Testcase testcase_check_application_gateway_name started")
        testcase_description = "Verify that bluesky-appgw Application Gateway exists"
        expected_result = "Application Gateway should exist with correct configuration"
        try:
            test_object.update_pre_result(testcase_description, expected_result)
            try:
                client = NetworkManagementClient(credentials, subscriptionId)
                gateway = client.application_gateways.get(self.resource_group_name, self.application_gateway_name)

                if gateway.name == self.application_gateway_name:
                    return test_object.update_result(1, expected_result,
                        "Application Gateway found: " + gateway.name, "Congrats!", " ")
                else:
                    return test_object.update_result(0, expected_result,
                        "Application Gateway name mismatch", "Check resource configuration", "https://docs.microsoft.com/...")
            except Exception as e:
                logging.error("Exception occurred: %s", str(e))
                return test_object.update_result(0, expected_result,
                    "Resource not found", "Please create the Application Gateway", "https://docs.microsoft.com/...")
        except Exception as e:
            logging.error("Internal Server error: %s", str(e))
            return test_object.update_result(-1, expected_result,
                "Internal Server error", "Please check with Admin", "")
            test_object.eval_message["testcase_check_application_gateway_name"] = str(e)

        logging.info("Testcase testcase_check_application_gateway_name Ended")

def start_tests(credentials, subscriptionId, args):
    logging.info("Started test execution")

    if "result_output" not in sys.modules:
        importlib.import_module("result_output")
    else:
        importlib.reload(sys.modules["result_output"])

    challenge_testcases = BlueskyAzureAppActivity()
    logging.info("BlueskyAzureAppActivity object created")
    result = ResultOutput(args, challenge_testcases)
    logging.info("Result output object created")

    # Execute all testcases
    challenge_testcases.testcase_check_application_gateway_name(result, credentials, subscriptionId)

    logging.info("Completed testcase executions")
    print(result.result_final())
    return result.result_final()