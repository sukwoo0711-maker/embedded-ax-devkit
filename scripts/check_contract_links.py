from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def packet_fields(packet_contract: dict) -> set[str]:
    fields = set()
    for packet in packet_contract.get("packets", []):
        packet_id = packet.get("id")
        for field in packet.get("fields", []):
            field_name = field.get("name")
            if packet_id and field_name:
                fields.add(f"{packet_id}.{field_name}")
    return fields


def ux_packet_refs(ux_contract: dict) -> list[tuple[str, str]]:
    refs = []
    for screen in ux_contract.get("screens", []):
        screen_id = screen.get("id", "<unknown-screen>")
        for item in screen.get("required_data", []):
            packet_field = item.get("packet_field")
            if packet_field:
                refs.append((screen_id, packet_field))
    return refs


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify UX required data references packet fields.")
    parser.add_argument("--ux", type=Path, default=Path("templates/ux_contract.yaml"))
    parser.add_argument("--packet", type=Path, default=Path("templates/packet_contract.yaml"))
    args = parser.parse_args()

    ux = load_yaml(args.ux)
    packet = load_yaml(args.packet)
    defined_fields = packet_fields(packet)
    refs = ux_packet_refs(ux)

    missing = []
    for screen_id, ref in refs:
        if ref not in defined_fields:
            missing.append((screen_id, ref))

    print(f"Defined packet fields: {len(defined_fields)}")
    print(f"UX packet references: {len(refs)}")
    if missing:
        print("Missing packet references:")
        for screen_id, ref in missing:
            print(f"  - {screen_id}: {ref}")
        return 1

    print("Contract links OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

