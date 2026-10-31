#!/usr/bin/env python3
"""Validate the *Cherri-compiled* Shortcut plist, not merely reference source.

Fail closed: never publish a signed file if it would leave DND off, set an
unbounded Focus, or fail to use the dynamic two-hour adjusted date.
"""
from pathlib import Path
import plistlib

files = list(Path(".").glob("*.plist"))
assert files, "Compiler didn't emit debug .plist; cannot validate actual actions"
assert len(files) == 1, f"Ambiguous debug plists: {files}"
wf = plistlib.loads(files[0].read_bytes())
actions = wf["WFWorkflowActions"]
print("Compiled actions:")
for i, a in enumerate(actions):
    print(i, a["WFWorkflowActionIdentifier"], str(a.get("WFWorkflowActionParameters", {}))[:1600])

ids = [a["WFWorkflowActionIdentifier"] for a in actions]
expect = [
    "is.workflow.actions.bluetooth.set",
    "is.workflow.actions.wifi.set",
    "is.workflow.actions.cellulardata.set",
]
assert ids[:3] == expect, f"Unexpected radio action order: {ids[:3]}"
for a in actions[:3]:
    p = a["WFWorkflowActionParameters"]
    assert (p.get("OnValue") is False or p.get("Enabled") is False), f"Radio not OFF: {p}"

date_actions = [a for a in actions if a["WFWorkflowActionIdentifier"] == "is.workflow.actions.adjustdate"]
assert len(date_actions) == 1, "Expected one two-hour adjust date"
date_params = date_actions[0]["WFWorkflowActionParameters"]
assert "2" in str(date_params), "2 hours missing from date adjustment"
assert ("hr" in str(date_params) or "Hour" in str(date_params)), "Hour unit missing"
output_uuid = date_params.get("UUID")
assert output_uuid, "Date adjustment missing UUID"

focuses = [a for a in actions if a["WFWorkflowActionIdentifier"] == "is.workflow.actions.dnd.set"]
assert len(focuses) == 1, f"Expected exactly one Focus action, got {len(focuses)}"
fp = focuses[0]["WFWorkflowActionParameters"]
assert fp.get("Enabled") == 1, f"DND must explicitly turn ON; compiled params: {fp}"
assert fp.get("Operation") == "Turn", "DND must not be a toggle"
assert fp.get("AssertionType") == "Time", "DND needs a fixed deadline, not unlimited duration"
assert fp.get("FocusModes", {}).get("Identifier") == "com.apple.donotdisturb.mode.default", "Not DND"
assert output_uuid in str(fp.get("Time", "")), "DND must end at the adjusted date output"
assert ids.index("is.workflow.actions.dnd.set") > ids.index("is.workflow.actions.adjustdate"), "Focus triggered before end time exists"
print("Verified actual compiled shortcut: radios off, DND ON, until dynamic +2 hours.")
