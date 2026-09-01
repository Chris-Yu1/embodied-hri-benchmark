"""Deterministic metrics computed from event-level HRI logs."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from statistics import mean
from typing import Iterable


@dataclass(frozen=True)
class Event:
    session_id: str
    participant_id: str
    platform: str
    turn_id: str
    event: str
    timestamp_s: float
    value: float | None = None


@dataclass(frozen=True)
class PlatformSummary:
    platform: str
    sessions: int
    turns: int
    valid_answer_rate: float
    attention_rate: float
    central_gaze_rate: float
    question_latency_s: float
    speech_onset_s: float
    timeout_rate: float

    def to_dict(self) -> dict[str, str | int | float]:
        return asdict(self)


def load_events(path: str | Path) -> list[Event]:
    events: list[Event] = []
    with Path(path).open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            raw_value = row.get("value", "").strip()
            events.append(
                Event(
                    session_id=row["session_id"],
                    participant_id=row["participant_id"],
                    platform=row["platform"],
                    turn_id=row["turn_id"],
                    event=row["event"],
                    timestamp_s=float(row["timestamp_s"]),
                    value=float(raw_value) if raw_value else None,
                )
            )
    return events


def _safe_mean(values: list[float]) -> float:
    return mean(values) if values else 0.0


def summarise_platform(events: Iterable[Event], platform: str) -> PlatformSummary:
    selected = [event for event in events if event.platform == platform]
    sessions = {event.session_id for event in selected}
    turns = {(event.session_id, event.turn_id) for event in selected if event.turn_id}
    grouped: dict[tuple[str, str], dict[str, Event]] = defaultdict(dict)
    for event in selected:
        grouped[(event.session_id, event.turn_id)][event.event] = event

    question_latencies: list[float] = []
    speech_latencies: list[float] = []
    valid_answers = timeouts = 0
    for turn in grouped.values():
        if "question_requested" in turn and "question_ready" in turn:
            question_latencies.append(
                turn["question_ready"].timestamp_s - turn["question_requested"].timestamp_s
            )
        if "speech_requested" in turn and "speech_started" in turn:
            speech_latencies.append(
                turn["speech_started"].timestamp_s - turn["speech_requested"].timestamp_s
            )
        valid_answers += int("answer_accepted" in turn)
        timeouts += int("no_speech_timeout" in turn)

    attention = [event.value for event in selected if event.event == "attention_sample" and event.value is not None]
    gaze = [event.value for event in selected if event.event == "central_gaze_sample" and event.value is not None]
    turn_count = len(turns)
    return PlatformSummary(
        platform=platform,
        sessions=len(sessions),
        turns=turn_count,
        valid_answer_rate=valid_answers / turn_count if turn_count else 0.0,
        attention_rate=_safe_mean(attention),
        central_gaze_rate=_safe_mean(gaze),
        question_latency_s=_safe_mean(question_latencies),
        speech_onset_s=_safe_mean(speech_latencies),
        timeout_rate=timeouts / turn_count if turn_count else 0.0,
    )


def compare_platforms(events: Iterable[Event], platform_a: str, platform_b: str) -> dict[str, object]:
    event_list = list(events)
    a = summarise_platform(event_list, platform_a)
    b = summarise_platform(event_list, platform_b)
    metrics = [
        "valid_answer_rate", "attention_rate", "central_gaze_rate",
        "question_latency_s", "speech_onset_s", "timeout_rate",
    ]
    differences = {metric: getattr(a, metric) - getattr(b, metric) for metric in metrics}
    return {"platform_a": a.to_dict(), "platform_b": b.to_dict(), "difference_a_minus_b": differences}
