from hri_benchmark.metrics import Event, compare_platforms, summarise_platform


def sample_events(platform: str, delay: float, accepted: bool = True):
    rows = [
        Event("s1", "p1", platform, "1", "question_requested", 0.0),
        Event("s1", "p1", platform, "1", "question_ready", delay),
        Event("s1", "p1", platform, "1", "speech_requested", delay),
        Event("s1", "p1", platform, "1", "speech_started", delay + 0.5),
        Event("s1", "p1", platform, "1", "attention_sample", delay + 1, 1.0),
        Event("s1", "p1", platform, "1", "central_gaze_sample", delay + 1, 1.0),
    ]
    if accepted:
        rows.append(Event("s1", "p1", platform, "1", "answer_accepted", delay + 4))
    else:
        rows.append(Event("s1", "p1", platform, "1", "no_speech_timeout", delay + 4))
    return rows


def test_platform_summary():
    summary = summarise_platform(sample_events("Robot-A", 2.0), "Robot-A")
    assert summary.sessions == 1
    assert summary.valid_answer_rate == 1.0
    assert summary.question_latency_s == 2.0
    assert summary.speech_onset_s == 0.5


def test_comparison_direction():
    events = sample_events("Robot-A", 1.0) + sample_events("Robot-B", 2.0, accepted=False)
    result = compare_platforms(events, "Robot-A", "Robot-B")
    assert result["difference_a_minus_b"]["question_latency_s"] == -1.0
    assert result["difference_a_minus_b"]["valid_answer_rate"] == 1.0
