import unittest
from  eosfactory import *

Logger.verbosity = [Verbosity.INFO, Verbosity.OUT, Verbosity.DEBUG]
_ = Logger()

CONTRACT_WORKSPACE = "_wslqwjvacdyugodewiyd"

class Test(unittest.TestCase):

    def run(self, result=None):
        super().run(result)


    @classmethod
    def setUpClass(cls):
        _.SCENARIO('''
        Create a contract from template, then build and deploy it.
        Also, execute simple actions, debug buffer and authority mismatch detection.
        ''')
        reset()
        create_wallet()
        get_wallet().import_key("5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3")
        exit()
        create_master_account("account_master")

        _.COMMENT('''
        Create test accounts:
        ''')
        create_account("account_alice", account_master)
        create_account("account_carol", account_master)


    def setUp(self):
        pass


    def test_01(self):
        _.COMMENT('''
        Create, build and deploy the contract:
        ''')
        create_account("account_host", account_master)
        contract = Contract(account_host, contract_workspace_from_template(
            CONTRACT_WORKSPACE, template="01_hello_world", remove_existing=True))
        contract.build()
        contract.deploy()

        _.COMMENT('''
        Test an action for Alice, including the debug buffer:
        ''')
        account_host.push_action(
            "hi", {"user":account_alice}, account_alice)
        self.assertTrue("account_alice" in account_host.debug_buffer)

        _.COMMENT('''
        Test an action for Carol, including the debug buffer:
        ''')
        account_host.push_action(
            "hi", {"user":account_carol}, account_carol)
        self.assertTrue("account_carol" in account_host.debug_buffer)

        _.COMMENT('''
        WARNING: This action should fail due to authority mismatch!
        ''')
        set_is_testing_errors(True)
        action = account_host.push_action(
            "hi", {"user":account_carol})
        set_is_testing_errors(False)
        self.assertTrue(account_host.action.error)

        contract.delete()


    def tearDown(self):
        pass


    @classmethod
    def tearDownClass(cls):
        stop()


if __name__ == "__main__":
    unittest.main()
