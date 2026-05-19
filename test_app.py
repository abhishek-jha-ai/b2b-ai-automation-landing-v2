import unittest
import json
from app import app, project_contract, execution_contract, capability_binding

class TestInitializeContracts(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_project_contract_initialization(self):
        # Initially not initialized
        self.assertFalse(project_contract.initialized)
        result = project_contract.initialize()
        self.assertTrue(project_contract.initialized)
        self.assertEqual(result["status"], "success")
        self.assertIn("Project contract initialized", result["message"])

    def test_execution_contract_initialization(self):
        # Initially not initialized
        self.assertFalse(execution_contract.initialized)
        result = execution_contract.initialize()
        self.assertTrue(execution_contract.initialized)
        self.assertEqual(result["status"], "success")
        self.assertIn("Execution contract initialized", result["message"])

    def test_capability_binding_initialize_all(self):
        # Reset states
        project_contract.initialized = False
        execution_contract.initialized = False
        result = capability_binding.initialize_all()
        self.assertTrue(project_contract.initialized)
        self.assertTrue(execution_contract.initialized)
        self.assertIn("project_contract", result)
        self.assertIn("execution_contract", result)
        self.assertEqual(result["project_contract"]["status"], "success")
        self.assertEqual(result["execution_contract"]["status"], "success")

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("project_contract", data)
        self.assertIn("execution_contract", data)
        self.assertEqual(data["project_contract"]["status"], "success")
        self.assertEqual(data["execution_contract"]["status"], "success")

if __name__ == '__main__':
    unittest.main()
