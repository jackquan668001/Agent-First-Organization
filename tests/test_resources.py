import json
import os
import pytest

from tests.utils_workers import MCWorkerOrchestrator, MsgWorkerOrchestrator
from tests.utils_shopify_tools import ShopifyToolOrchestrator


@pytest.mark.parametrize(
    "orchestrator_cls, config_file_name, test_cases_file_name",
    [
        (
            MCWorkerOrchestrator,
            "mc_worker_taskgraph.json",
            "mc_worker_testcases.json",
        ),
        (
            MsgWorkerOrchestrator,
            "message_worker_taskgraph.json",
            "message_worker_testcases.json",
        ),
        (
            ShopifyToolOrchestrator,
            "shopify_tools_taskgraph.json",
            "shopify_tools_testcases.json",
        ),
    ],
)
def test_resources(orchestrator_cls, config_file_name, test_cases_file_name):
    test_resources_instance = orchestrator_cls(os.path.join(os.path.dirname(__file__), "data", config_file_name))
    with open(os.path.join(os.path.dirname(__file__), "data", test_cases_file_name), "r") as f:
        test_cases = json.load(f)
    for i, test_case in enumerate(test_cases):
        try:
            test_resources_instance.run_single_test(test_case)
        except Exception as _:
            pytest.fail(f"Test case {i} failed for {orchestrator_cls.__name__} from {test_cases_file_name}", pytrace=True)


