# Embodied HRI Benchmark

A lightweight, reproducible toolkit for evaluating conversational human-robot interaction across robot embodiments.

The project turns event-level interaction logs into comparable research metrics: task success, valid-answer rate, attention, central gaze, question-generation latency, speech-onset latency, and timeout rate. It is designed for pilot studies, system debugging, and transparent cross-platform reporting.

## Research motivation

Conversational quality depends on more than the language model. Hardware interfaces, sensing reliability, audio routing, network delay, and turn-taking logic can materially change a participant's experience. This toolkit makes those differences measurable.

## Features

- Typed event schema with session, participant, platform, turn, and timestamp fields
- Deterministic metric computation from raw interaction events
- Participant-level paired comparison between two robot platforms
- Bootstrap confidence intervals with a fixed random seed
- Synthetic, non-participant example data for safe demonstration
- Command-line interface and automated tests

## Quick start

```bash
python -m pip install -e .
hri-benchmark analyse data/example_events.csv --platform-a Temi --platform-b Walker
pytest
```

## Event schema

| Field | Description |
|---|---|
| `session_id` | Unique interaction session |
| `participant_id` | Pseudonymous participant identifier |
| `platform` | Robot or embodied-agent condition |
| `turn_id` | Conversation turn identifier |
| `event` | Event type, such as `question_requested` or `speech_started` |
| `timestamp_s` | Monotonic timestamp in seconds |
| `value` | Optional numeric observation |

## Example output

```text
platform  sessions  valid_answer_rate  question_latency_s  speech_onset_s
Temi             2              1.000               1.850           0.650
Walker           2              0.750               2.450           1.050
```

## Reproducibility and ethics

The repository contains synthetic data only. It does not include photographs, audio, transcripts, gaze traces, personal identifiers, or participant records. Researchers should obtain appropriate ethics approval and consent before collecting human-subject data.

## Roadmap

- Add exact paired permutation tests and effect sizes
- Export publication-ready figures
- Support ROS bag and JSONL importers
- Add configurable metric definitions through YAML

## Author

Qinghong Yu — Robotics MSc candidate interested in multimodal HRI, socially assistive robotics, embodied AI, and reproducible evaluation.

## License

MIT
