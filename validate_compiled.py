#!/usr/bin/env python3
"""Verify Cherri compiler output, repair its FocusModes field encoding, then
produce an *unsigned* plist for a separate signing step.

Cherri 2.3.0 serializes a custom action's static FocusModes dictionary as a
WFDictionaryFieldValue, but Apple's dnd.set needs a plain dictionary. The
compiler's built-in setFocusMode also omits Enabled=1. Patch and validate
the real compiled plist before signing; do not change the date magic variable.
"""
import plistlib
from pathlib import Path

plists = list(Path(".").glob("*.plist"))
assert len(plists) == 1, f"Expected a single debug .plist, found: {plists}"
wf = plistlib.loads(plists[0].read_bytes())
actions = wf["WFWorkflowActions"]

ids = [a["WFWorkflowActionIdentifier"] for a in actions]
assert ids == [
    "is.workflow.actions.bluetooth.set",
    "is.workflow.actions.wifi.set",
    "is.workflow.actions.cellulardata.set",
    "is.workflow.actions.date",
    "is.workflow.actions.adjustdate",
    "is.workflow.actions.dnd.set",
], f"Unexpected action sequence: {ids}"

for index in range(3):
    params = actions[index]["WFWorkflowActionParameters"]
    assert params.get("OnValue") is False, f"Radio action {index} not explicitly OFF"

now = actions[3]["WFWorkflowActionParameters"]
assert now["WFDateActionMode"] == "Current Date"
now_id = now["UUID"]

delta = actions[4]["WFWorkflowActionParameters"]
assert delta["WFAdjustOperation"] == "Add"
duration = delta["WFDuration"]["Value"]
assert int(duration["Magnitude"]) == 2
assert duration["Unit"] == "hr"
assert delta["WFDate"]["Value"]["attachmentsByRange"]["{0, 1}"]["OutputUUID"] == now_id
deadline_uuid = delta["UUID"]

p = actions[5]["WFWorkflowActionParameters"]
assert p["Operation"] == "Turn"
assert int(p["Enabled"]) == 1, "DND must explicitly be set ON, never toggle/off"
assert p["AssertionType"] == "Time"
assert p["Time"]["Value"]["attachmentsByRange"]["{0, 1}"]["OutputUUID"] == deadline_uuid

focus = p["FocusModes"]
if "Value" in focus and focus.get("WFSerializationType") == "WFDictionaryFieldValue":
    # Cherri custom action wraps the nested FocusModes dictionary in a
    # WFDictionaryFieldValue. Apple's native Set Focus needs an unwrapped dict.
    fixed = {}
    for item in focus["Value"]["WFDictionaryFieldValueItems"]:
        key = item["WFKey"]["Value"]["string"]
        val = item["WFValue"]["Value"]["string"]
        fixed[key] = val
    focus = fixed
assert focus == {
    "DisplayString": "Do Not Disturb",
    "Identifier": "com.apple.donotdisturb.mode.default",
}, f"Not the system's Do Not Disturb Focus: {focus}"
p["FocusModes"] = focus
p["Enabled"] = 1  # ensure integer, not float in Apple plist
assert p["FocusModes"]["Identifier"] == "com.apple.donotdisturb.mode.default"

output = Path("build/verified_unsigned.shortcut")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_bytes(plistlib.dumps(wf, fmt=plistlib.FMT_XML))
check = plistlib.loads(output.read_bytes())
assert check["WFWorkflowActions"][5]["WFWorkflowActionParameters"]["Enabled"] == 1
assert check["WFWorkflowActions"][5]["WFWorkflowActionParameters"]["FocusModes"] == focus
print("PASS: three radios OFF; current date + exactly 2 hours; DND explicitly ON until computed date")
print(f"PASS: repaired FocusModes native dictionary; verified unsigned plist: {output}")
