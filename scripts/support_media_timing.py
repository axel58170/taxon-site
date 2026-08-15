#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import math
import re
from dataclasses import dataclass
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$")


class TimingError(ValueError):
    pass


@dataclass(frozen=True)
class Phase:
    name: str
    source_start: float
    source_end: float
    output_duration: float
    output_start: float


@dataclass(frozen=True)
class Marker:
    name: str
    phase: str
    start: float
    duration: float
    center_x: float
    center_y: float
    radius_x: float
    radius_y: float
    stroke: str
    fill: str
    stroke_width: float


def positive_number(value: str, field: str, row: int, *, allow_zero: bool = False) -> float:
    try:
        number = float(value)
    except ValueError as error:
        raise TimingError(f"Row {row}: {field} must be a number.") from error
    if not math.isfinite(number):
        raise TimingError(f"Row {row}: {field} must be finite.")
    if number < 0 or (number == 0 and not allow_zero):
        qualifier = "non-negative" if allow_zero else "positive"
        raise TimingError(f"Row {row}: {field} must be {qualifier}.")
    return number


def load_timeline(path: Path) -> tuple[Phase, ...]:
    phases: list[Phase] = []
    output_start = 0.0
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        expected = {"phase", "source_start", "source_end", "output_duration"}
        if set(reader.fieldnames or ()) != expected:
            raise TimingError(f"{path} must contain exactly: {', '.join(sorted(expected))}.")
        for row_number, row in enumerate(reader, start=2):
            name = row["phase"].strip()
            if not NAME_PATTERN.fullmatch(name):
                raise TimingError(f"Row {row_number}: invalid phase name {name!r}.")
            if any(phase.name == name for phase in phases):
                raise TimingError(f"Row {row_number}: duplicate phase {name!r}.")
            source_start = positive_number(row["source_start"], "source_start", row_number, allow_zero=True)
            source_end = positive_number(row["source_end"], "source_end", row_number)
            duration = positive_number(row["output_duration"], "output_duration", row_number)
            if source_end <= source_start:
                raise TimingError(f"Row {row_number}: source_end must be after source_start.")
            phases.append(Phase(name, source_start, source_end, duration, output_start))
            output_start += duration
    if not phases:
        raise TimingError("Timeline must contain at least one phase.")
    return tuple(phases)


def load_markers(path: Path, phases: tuple[Phase, ...]) -> tuple[Marker, ...]:
    phase_by_name = {phase.name: phase for phase in phases}
    markers: list[Marker] = []
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        expected = {
            "marker", "phase", "start", "duration", "center_x", "center_y",
            "radius_x", "radius_y", "stroke", "fill", "stroke_width",
        }
        if set(reader.fieldnames or ()) != expected:
            raise TimingError(f"{path} must contain exactly: {', '.join(sorted(expected))}.")
        for row_number, row in enumerate(reader, start=2):
            name = row["marker"].strip()
            phase_name = row["phase"].strip()
            if not NAME_PATTERN.fullmatch(name):
                raise TimingError(f"Row {row_number}: invalid marker name {name!r}.")
            if any(marker.name == name for marker in markers):
                raise TimingError(f"Row {row_number}: duplicate marker {name!r}.")
            if phase_name not in phase_by_name:
                raise TimingError(f"Row {row_number}: unknown phase {phase_name!r}.")
            start = positive_number(row["start"], "start", row_number, allow_zero=True)
            duration = positive_number(row["duration"], "duration", row_number)
            phase = phase_by_name[phase_name]
            if start + duration > phase.output_duration + 1e-9:
                raise TimingError(f"Row {row_number}: marker extends beyond phase {phase_name!r}.")
            coordinates = [
                positive_number(row[field], field, row_number, allow_zero=field.startswith("center_"))
                for field in ("center_x", "center_y", "radius_x", "radius_y")
            ]
            stroke = row["stroke"].strip()
            fill = row["fill"].strip()
            if not COLOR_PATTERN.fullmatch(stroke) or not COLOR_PATTERN.fullmatch(fill):
                raise TimingError(f"Row {row_number}: stroke and fill must be #RRGGBB or #RRGGBBAA.")
            stroke_width = positive_number(row["stroke_width"], "stroke_width", row_number)
            markers.append(Marker(
                name, phase_name, start, duration, *coordinates, stroke, fill, stroke_width
            ))
    return tuple(markers)


def timeline_filter(phases: tuple[Phase, ...]) -> str:
    bases = "".join(f"[base{index}]" for index in range(len(phases)))
    filters = [f"[0:v]fps=30,split={len(phases)}{bases}"]
    for index, phase in enumerate(phases):
        scale = phase.output_duration / (phase.source_end - phase.source_start)
        filters.append(
            f"[base{index}]trim=start={phase.source_start:g}:end={phase.source_end:g},"
            f"setpts=(PTS-STARTPTS)*{scale:.12g}[phase{index}]"
        )
    inputs = "".join(f"[phase{index}]" for index in range(len(phases)))
    filters.append(f"{inputs}concat=n={len(phases)}:v=1:a=0[timed]")
    return ";".join(filters)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    timeline_parser = subparsers.add_parser("timeline-filter")
    timeline_parser.add_argument("timeline", type=Path)
    markers_parser = subparsers.add_parser("markers")
    markers_parser.add_argument("timeline", type=Path)
    markers_parser.add_argument("markers", type=Path)
    markers_parser.add_argument("--prefix-seconds", type=float, default=0.0)
    arguments = parser.parse_args()

    try:
        phases = load_timeline(arguments.timeline)
        if arguments.command == "timeline-filter":
            print(timeline_filter(phases))
            return
        markers = load_markers(arguments.markers, phases)
        phase_by_name = {phase.name: phase for phase in phases}
        for marker in markers:
            absolute_start = arguments.prefix_seconds + phase_by_name[marker.phase].output_start + marker.start
            absolute_end = absolute_start + marker.duration
            print("\t".join((
                marker.name, f"{absolute_start:g}", f"{absolute_end:g}",
                f"{marker.center_x:g}", f"{marker.center_y:g}",
                f"{marker.radius_x:g}", f"{marker.radius_y:g}", marker.stroke,
                marker.fill, f"{marker.stroke_width:g}",
            )))
    except TimingError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
