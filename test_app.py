import unittest
import json
from app import app, project_contract, execution_contract, capability_binding, deployment_profile_service

class TestInitializeContracts(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_project_contract_initialization(self):
        # Reset state
        project_contract.initialized = False
        self.assertFalse(project_contract.initialized)
        result = project_contract.initialize()
        self.assertTrue(project_contract.initialized)
        self.assertEqual(result["status"], "success")
        self.assertIn("Project contract initialized", result["message"])

    def test_execution_contract_initialization(self):
        # Reset state
        execution_contract.initialized = False
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
        self.assertIn("status", data)
        self.assertIn("message", data)
        self.assertEqual(data["status"], "ok")

    def test_initialize_deployment_profile_route(self):
        # Test the /initialize-deployment-profile route
        response = self.app.get('/initialize-deployment-profile')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Check contracts
        self.assertIn("project_contract", data)
        self.assertIn("execution_contract", data)
        self.assertEqual(data["project_contract"]["status"], "success")
        self.assertEqual(data["execution_contract"]["status"], "success")
        # Check deployment profile
        self.assertIn("deployment_profile", data)
        profile = data["deployment_profile"]
        self.assertEqual(profile["status"], "initialized")
        self.assertEqual(profile["alignment"], "preview")

    def test_deployment_profile_service_initialization(self):
        # Reset contracts
        project_contract.initialized = False
        execution_contract.initialized = False
        # Clear repository
        deployment_profile_service.repository._profile_data = {}
        result = deployment_profile_service.initialize_profile()
        self.assertIn("project_contract", result)
        self.assertIn("execution_contract", result)
        self.assertIn("deployment_profile", result)
        self.assertEqual(result["deployment_profile"]["status"], "initialized")
        self.assertEqual(result["deployment_profile"]["alignment"], "preview")
        # Ensure repository stores the profile
        stored = deployment_profile_service.repository.get_profile("genesis-profile")
        self.assertIsNotNone(stored)
        self.assertEqual(stored["status"], "initialized")
        self.assertEqual(stored["alignment"], "preview")

if __name__ == '__main__':
    unittest.main()
