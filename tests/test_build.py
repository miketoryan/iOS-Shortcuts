import plistlib
import unittest
from build_shortcut import workflow, OUTPUT_UUID, FOCUS_ID


class WorkflowTest(unittest.TestCase):
    def test_binary_plist_roundtrip(self):
        w = workflow()
        self.assertEqual(plistlib.loads(plistlib.dumps(w, fmt=plistlib.FMT_BINARY)), w)

    def test_connections_are_explicitly_off(self):
        actions = workflow()["WFWorkflowActions"]
        ids = [a["WFWorkflowActionIdentifier"] for a in actions]
        self.assertEqual(ids[:3], [
            "is.workflow.actions.bluetooth.set",
            "is.workflow.actions.wifi.set",
            "is.workflow.actions.cellulardata.set",
        ])
        for a in actions[:3]:
            self.assertEqual(a["WFWorkflowActionParameters"]["operation"], "Turn")
            self.assertIs(a["WFWorkflowActionParameters"]["OnValue"], False)

    def test_two_hours_from_run_time(self):
        params = workflow()["WFWorkflowActions"][3]["WFWorkflowActionParameters"]
        self.assertEqual(params["UUID"], OUTPUT_UUID)
        self.assertEqual(
            params["WFDate"]["Value"]["attachmentsByRange"]["{0, 1}"]["Type"],
            "CurrentDate",
        )
        self.assertEqual(
            params["WFAdjustOffsetPicker"]["Value"],
            {"Operation": "Add", "Unit": "Hour", "Value": 2},
        )
        self.assertEqual(params["WFDuration"]["Value"], {"Magnitude": 2, "Unit": "hr"})

    def test_focus_ends_at_adjusted_date(self):
        params = workflow()["WFWorkflowActions"][4]["WFWorkflowActionParameters"]
        self.assertEqual(params["FocusModes"]["Identifier"], FOCUS_ID)
        self.assertEqual(params["AssertionType"], "Time")
        self.assertEqual(params["Enabled"], 1)
        self.assertEqual(
            params["Time"]["Value"]["attachmentsByRange"]["{0, 1}"]["OutputUUID"],
            OUTPUT_UUID,
        )

    def test_no_other_actions_or_background_reenable(self):
        self.assertEqual(len(workflow()["WFWorkflowActions"]), 5)


if __name__ == "__main__":
    unittest.main()
