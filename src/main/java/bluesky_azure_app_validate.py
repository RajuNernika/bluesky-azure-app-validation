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
    # Resource names
    resource_group_name = "bluesky-rg"
    application_gateway_name = "bluesky-appgw"
    load_balancer_name = "bluesky-lb"
    backend_pool_names = ["bluesky-appgwbe", "bluesky-imagebe"]
    health_probe_name = "bluesky-hp"
    lb_backend_pool_name = "bluesky-be"

    def testcase_check_application_gateway_name(self, test_object, credentials, subscriptionId):
        logging.info("Testcase testcase_check_application_gateway_name started")
        testcase_description = "Verify that bluesky-appgw Application Gateway exists"
        expected_result = "Application Gateway should exist with correct configuration"
        try:
            test_object.update_pre_result(testcase_description, expected_result)
            try:
                client = NetworkManagementClient(credentials, subscriptionId)
                app_gateway = client.application_gateways.get(self.resource_group_name, self.application_gateway_name)

                if app_gateway.name == self.application_gateway_name:
                    return test_object.update_result(1, expected_result,
                        "Application Gateway found: " + app_gateway.name, "Congrats!", " ")
                else:
                    return test_object.update_result(0, expected_result,
                        "Application Gateway name mismatch", "Check resource configuration", "https://docs.microsoft.com/...")
            except Exception as e:
                logging.error("Exception: %s", str(e))
                return test_object.update_result(0, expected_result,
                    "Application Gateway not found", "Please create the resource", "https://docs.microsoft.com/...")
        except Exception as e:
            logging.error("Internal Server error: %s", str(e))
            return test_object.update_result(-1, expected_result,
                "Internal Server error", "Please check with Admin", "")

        logging.info("Testcase testcase_check_application_gateway_name Ended")

    def testcase_check_application_gateway_size(self, test_object, credentials, subscriptionId):
        logging.info("Testcase testcase_check_application_gateway_size started")
        testcase_description = "Verify that Application Gateway has Standard_v2 SKU"
        expected_result = "Application Gateway should have Standard_v2 SKU"
        try:
            test_object.update_pre_result(testcase_description, expected_result)
            try:
                client = NetworkManagementClient(credentials, subscriptionId)
                app_gateway = client.application_gateways.get(self.resource_group_name, self.application_gateway_name)

                if app_gateway.sku.name == "Standard_v2":
                    return test_object.update_result(1, expected_result,
                        "Application Gateway SKU is Standard_v2", "Congrats!", " ")
                else:
                    return test_object.update_result(0, expected_result,
                        "Application Gateway SKU mismatch", "Check SKU configuration", "https://docs.microsoft.com/...")
            except Exception as e:
                logging.error("Exception: %s", str(e))
                return test_object.update_result(0, expected_result,
                    "Application Gateway not found", "Please create the resource", "https://docs.microsoft.com/...")
        except Exception as e:
            logging.error("Internal Server error: %s", str(e))
            return test_object.update_result(-1, expected_result,
                "Internal Server error", "Please check with Admin", "")

        logging.info("Testcase testcase_check_application_gateway_size Ended")

    def testcase_check_backend_pools(self, test_object, credentials, subscriptionId):
        logging.info("Testcase testcase_check_backend_pools started")
        testcase_description = "Verify backend pools bluesky-appgwbe, bluesky-imagebe exist"
        expected_result = "Backend pools should exist"
        try:
            test_object.update_pre_result(testcase_description, expected_result)
            try:
                client = NetworkManagementClient(credentials, subscriptionId)
                app_gateway = client.application_gateways.get(self.resource_group_name, self.application_gateway_name)

                backend_pool_names = [pool.name for pool in app_gateway.backend_address_pools]
                if all(name in backend_pool_names for name in self.backend_pool_names):
                    return test_object.update_result(1, expected_result,
                        "All backend pools found", "Congrats!", " ")
                else:
                    return test_object.update_result(0, expected_result,
                        "Some backend pools are missing", "Check backend pool configuration", "https://docs.microsoft.com/...")
            except Exception as e:
                logging.error("Exception: %s", str(e))
                return test_object.update_result(0, expected_result,
                    "Application Gateway not found", "Please create the resource", "https://docs.microsoft.com/...")
        except Exception as e:
            logging.error("Internal Server error: %s", str(e))
            return test_object.update_result(-1, expected_result,
                "Internal Server error", "Please check with Admin", "")

        logging.info("Testcase testcase_check_backend_pools Ended")

    def testcase_check_load_balancer_name(self, test_object, credentials, subscriptionId):
        logging.info("Testcase testcase_check_load_balancer_name started")
        testcase_description = "Verify that bluesky-lb Load Balancer exists"
        expected_result = "Load Balancer should exist with correct configuration"
        try:
            test_object.update_pre_result(testcase_description, expected_result)
            try:
                client = NetworkManagementClient(credentials, subscriptionId)
                load_balancer = client.load_balancers.get(self.resource_group_name, self.load_balancer_name)

                if load_balancer.name == self.load_balancer_name:
                    return test_object.update_result(1, expected_result,
                        "Load Balancer found: " + load_balancer.name, "Congrats!", " ")
                else:
                    return test_object.update_result(0, expected_result,
                        "Load Balancer name mismatch", "Check resource configuration", "https://docs.microsoft.com/...")
            except Exception as e:
                logging.error("Exception: %s", str(e))
                return test_object.update_result(0, expected_result,
                    "Load Balancer not found", "Please create the resource", "https://docs.microsoft.com/...")
        except Exception as e:
            logging.error("Internal Server error: %s", str(e))
            return test_object.update_result(-1, expected_result,
                "Internal Server error", "Please check with Admin", "")

        logging.info("Testcase testcase_check_load_balancer_name Ended")

    def testcase_check_load_balancer_backend_pool(self, test_object, credentials, subscriptionId):
        logging.info("Testcase testcase_check_load_balancer_backend_pool started")
        testcase_description = "Verify backend pool bluesky-be exists"
        expected_result = "Backend pool should exist"
        try:
            test_object.update_pre_result(testcase_description, expected_result)
            try:
                client = NetworkManagementClient(credentials, subscriptionId)
                load_balancer = client.load_balancers.get(self.resource_group_name, self.load_balancer_name)

                backend_pool_names = [pool.name for pool in load_balancer.backend_address_pools]
                if self.lb_backend_pool_name in backend_pool_names:
                    return test_object.update_result(1, expected_result,
                        "Backend pool found: " + self.lb_backend_pool_name, "Congrats!", " ")
                else:
                    return test_object.update_result(0, expected_result,
                        "Backend pool not found", "Check backend pool configuration", "https://docs.microsoft.com/...")
            except Exception as e:
                logging.error("Exception: %s", str(e))
                return test_object.update_result(0, expected_result,
                    "Load Balancer not found", "Please create the resource", "https://docs.microsoft.com/...")
        except Exception as e:
            logging.error("Internal Server error: %s", str(e))
            return test_object.update_result(-1, expected_result,
                "Internal Server error", "Please check with Admin", "")

        logging.info("Testcase testcase_check_load_balancer_backend_pool Ended")

    def testcase_check_health_probe(self, test_object, credentials, subscriptionId):
        logging.info("Testcase testcase_check_health_probe started")
        testcase_description = "Verify health probe bluesky-hp is configured"
        expected_result = "Health probe should be configured"
        try:
            test_object.update_pre_result(testcase_description, expected_result)
            try:
                client = NetworkManagementClient(credentials, subscriptionId)
                app_gateway = client.application_gateways.get(self.resource_group_name, self.application_gateway_name)

                probe_names = [probe.name for probe in app_gateway.probes]
                if self.health_probe_name in probe_names:
                    return test_object.update_result(1, expected_result,
                        "Health probe found: " + self.health_probe_name, "Congrats!", " ")
                else:
                    return test_object.update_result(0, expected_result,
                        "Health probe not found", "Check health probe configuration", "https://docs.microsoft.com/...")
            except Exception as e:
                logging.error("Exception: %s", str(e))
                return test_object.update_result(0, expected_result,
                    "Application Gateway not found", "Please create the resource", "https://docs.microsoft.com/...")
        except Exception as e:
            logging.error("Internal Server error: %s", str(e))
            return test_object.update_result(-1, expected_result,
                "Internal Server error", "Please check with Admin", "")

        logging.info("Testcase testcase_check_health_probe Ended")

def start_tests(credentials, subscriptionId, args):
    logging.info("Started test execution")

    if "result_output" not in sys.modules:
        importlib.import_module("result_output")
    else:
        importlib.reload(sys.modules["result_output"])

    challenge_testcases = BlueskyAzureAppActivity()
    logging.info("Activity object created")
    result = ResultOutput(args, challenge_testcases)
    logging.info("Result output object created")

    # Execute all testcases
    challenge_testcases.testcase_check_application_gateway_name(result, credentials, subscriptionId)
    challenge_testcases.testcase_check_application_gateway_size(result, credentials, subscriptionId)
    challenge_testcases.testcase_check_backend_pools(result, credentials, subscriptionId)
    challenge_testcases.testcase_check_load_balancer_name(result, credentials, subscriptionId)
    challenge_testcases.testcase_check_load_balancer_backend_pool(result, credentials, subscriptionId)
    challenge_testcases.testcase_check_health_probe(result, credentials, subscriptionId)

    logging.info("Completed testcase executions")
    print(result.result_final())
    return result.result_final()