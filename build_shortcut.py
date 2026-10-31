#!/usr/bin/env python3
"""Generate an unsigned iPhone Shortcut: radios off, DND on for two hours.

Requires only Python's standard library. An Apple signature is required
before the resulting file can be imported on modern iOS.
"""
import argparse
import plistlib
from pathlib import Path

NAME = "一键免打扰（2小时）"
OUTPUT_UUID = "E8C41B0F-91E1-4D7D-84D3-ABF7C09B3C10"
FOCUS_ID = "com.apple.donotdisturb.mode.default"


def action(identifier: str, **params: object) -> dict:
    return {
        "WFWorkflowActionIdentifier": identifier,
        "WFWorkflowActionParameters": params,
    }


def text_token(value: dict) -> dict:
    return {
        "WFSerializationType": "WFTextTokenString",
        "Value": {
            "string": "\ufffc",
            "attachmentsByRange": {"{0, 1}": value},
        },
    }


def workflow() -> dict:
    actions = [
        action("is.workflow.actions.bluetooth.set", operation="Turn", OnValue=False),
        action("is.workflow.actions.wifi.set", operation="Turn", OnValue=False),
        action("is.workflow.actions.cellulardata.set", operation="Turn", OnValue=False),
        action(
            "is.workflow.actions.adjustdate",
            UUID=OUTPUT_UUID,
            WFAdjustOperation="Add",
            WFAdjustOffsetPicker={
                "WFSerializationType": "WFTimeOffsetValue",
                "Value": {"Operation": "Add", "Unit": "Hour", "Value": 2},
            },
            WFDate=text_token({"Type": "CurrentDate"}),
            WFDuration={
                "WFSerializationType": "WFQuantityFieldValue",
                "Value": {"Magnitude": 2, "Unit": "hr"},
            },
        ),
        action(
            "is.workflow.actions.dnd.set",
            Operation="Turn",
            Enabled=1,
            AssertionType="Time",
            FocusModes={"DisplayString": "Do Not Disturb", "Identifier": FOCUS_ID},
            Time=text_token({
                "Type": "ActionOutput",
                "OutputName": "Adjusted Date",
                "OutputUUID": OUTPUT_UUID,
            }),
        ),
    ]
    return {
        "WFWorkflowName": NAME,
        "WFWorkflowActions": actions,
        "WFWorkflowClientVersion": "4033.0.4.3",
        "WFWorkflowMinimumClientVersion": 900,
        "WFWorkflowMinimumClientVersionString": "900",
        "WFWorkflowIcon": {
            "WFWorkflowIconGlyphNumber": 61512,
            "WFWorkflowIconStartColor": 2071128575,
        },
        "WFWorkflowHasOutputFallback": False,
        "WFWorkflowHasShortcutInputVariables": False,
        "WFWorkflowImportQuestions": [],
        "WFWorkflowInputContentItemClasses": [],
        "WFWorkflowOutputContentItemClasses": [],
        "WFWorkflowTypes": ["NCWidget"],
        "WFQuickActionSurfaces": [],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="build/unsigned/one-tap-dnd-2h.shortcut")
    args = p.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(plistlib.dumps(workflow(), fmt=plistlib.FMT_BINARY, sort_keys=True))
    print(f"Unsigned workflow created: {output}")
    print("DO NOT distribute unsigned files as importable shortcuts.")


if __name__ == "__main__":
    main()
