import unittest

from gaskill.sfsm import State, StateMachine, FunctionState, StateTransition


class TestState(unittest.TestCase):
    def test_init(self):
        state = State("test")
        self.assertEqual(state.name, "test")
        self.assertIsNone(state.state_machine)

    def test_enter_exit(self):
        state = State("test")
        # 默认方法不抛出异常
        state.enter(None)
        state.exit(None)


class TestStateMachine(unittest.TestCase):
    def test_init(self):
        sm = StateMachine()
        self.assertIsNone(sm.current_state)

    def test_add_state(self):
        sm = StateMachine()
        state = State("idle")
        sm.add_state(state)
        self.assertTrue(sm.has_state("idle"))

    def test_set_state(self):
        sm = StateMachine()
        state = State("idle")
        sm.add_state(state)
        result = sm.set_state("idle")
        self.assertTrue(result)
        self.assertEqual(sm.current_state_name, "idle")

    def test_set_invalid_state(self):
        sm = StateMachine()
        result = sm.set_state("invalid")
        self.assertFalse(result)

    def test_transition(self):
        sm = StateMachine()
        state1 = State("state1")
        state2 = State("state2")
        sm.add_state(state1)
        sm.add_state(state2)
        sm.set_state("state1")
        result = sm.set_state("state2")
        self.assertTrue(result)
        self.assertEqual(sm.current_state_name, "state2")

    def test_revert_to_previous(self):
        sm = StateMachine()
        state1 = State("state1")
        state2 = State("state2")
        sm.add_state(state1)
        sm.add_state(state2)
        sm.set_state("state1")
        sm.set_state("state2")
        result = sm.revert_to_previous()
        self.assertTrue(result)
        self.assertEqual(sm.current_state_name, "state1")

    def test_lock(self):
        sm = StateMachine()
        state1 = State("state1")
        state2 = State("state2")
        sm.add_state(state1)
        sm.add_state(state2)
        sm.set_state("state1")
        sm.lock()
        result = sm.set_state("state2")
        self.assertFalse(result)


class TestFunctionState(unittest.TestCase):
    def test_init(self):
        state = FunctionState("test")
        self.assertEqual(state.name, "test")

    def test_callbacks(self):
        enter_called = []
        exit_called = []

        def on_enter(old_state):
            enter_called.append(old_state)

        def on_exit(new_state):
            exit_called.append(new_state)

        state = FunctionState("test", on_enter=on_enter, on_exit=on_exit)
        state.enter("old")
        state.exit("new")

        self.assertEqual(enter_called, ["old"])
        self.assertEqual(exit_called, ["new"])


class TestStateTransition(unittest.TestCase):
    def test_init(self):
        st = StateTransition()
        self.assertEqual(len(st._transitions), 0)

    def test_add_transition(self):
        st = StateTransition()
        st.add_transition("idle", "running")
        self.assertTrue("idle" in st._transitions)

    def test_get_transition(self):
        st = StateTransition()
        st.add_transition("idle", "running")
        result = st.get_transition("idle")
        self.assertEqual(result, "running")

    def test_condition(self):
        st = StateTransition()
        condition_met = [False]

        def condition(context):
            return condition_met[0]

        st.add_transition("idle", "running", condition=condition)
        result = st.get_transition("idle")
        self.assertIsNone(result)

        condition_met[0] = True
        result = st.get_transition("idle")
        self.assertEqual(result, "running")


if __name__ == '__main__':
    unittest.main()
