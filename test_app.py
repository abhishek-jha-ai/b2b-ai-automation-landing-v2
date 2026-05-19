import unittest
import json
from app import app, project_contract, execution_contract, capability_binding, telemetry_service, telemetry_capability_binding

class TestInitializeContracts(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_project_contract_initialization(self):
        # Initially not initialized
        project_contract.initialized = False
        self.assertFalse(project_contract.initialized)
        result = project_contract.initialize()
        self.assertTrue(project_contract.initialized)
        self.assertEqual(result["status"], "success")
        self.assertIn("Project contract initialized", result["message"])

    def test_execution_contract_initialization(self):
        # Initially not initialized
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
        self.assertIn("project_contract", data)
        self.assertIn("execution_contract", data)
        self.assertEqual(data["project_contract"]["status"], "success")
        self.assertEqual(data["execution_contract"]["status"], "success")

    def test_telemetry_service_initialization(self):
        telemetry_service.baselines_initialized = False
        telemetry_service.observability_initialized = False
        result = telemetry_service.initialize_telemetry()
        self.assertTrue(result["telemetry"]["baselines"])
        self.assertTrue(result["telemetry"]["observability"])
        self.assertEqual(result["status"], "success")
        self.assertIn("Telemetry baselines and observability initialized", result["message"])

    def test_telemetry_capability_binding(self):
        telemetry_service.baselines_initialized = False
        telemetry_service.observability_initialized = False
        result = telemetry_capability_binding.initialize()
        self.assertTrue(result["telemetry"]["baselines"])
        self.assertTrue(result["telemetry"]["observability"])
        self.assertEqual(result["status"], "success")
        self.assertIn("Telemetry baselines and observability initialized", result["message"])

    def test_telemetry_init_route(self):
        telemetry_service.baselines_initialized = False
        telemetry_service.observability_initialized = False
        response = self.app.post('/telemetry/init')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertIn("telemetry", data)
        self.assertTrue(data["telemetry"]["baselines"])
        self.assertTrue(data["telemetry"]["observability"])
        self.assertIn("Telemetry baselines and observability initialized", data["message"])

if __name__ == '__main__':
    unittest.main()
