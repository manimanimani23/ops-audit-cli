#!/usr/bin/env python3
import json
import sys
from pathlib import Path

THRESHOLDS = {
    "retry_rate": 0.10,
    "p95_latency_ms": 2500,
    "error_rate": 0.015,
}

REQUIRED_FIELDS = {
    "project_id": str,
    "date": str,
    "inference_cost_usd": (int, float),
    "retry_rate": (int, float),
    "p95_latency_ms": (int, float),
    "error_rate": (int, float),
    "requests": int,
    "notes": str,
}


class ValidationError(Exception):
    pass


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_input(data: dict) -> None:
    if not isinstance(data, dict):
        raise ValidationError("Input must be a JSON object")

    missing = [k for k in REQUIRED_FIELDS.keys() if k not in data]
    if missing:
        raise ValidationError(f"Missing required fields: {', '.join(missing)}")

    for key, expected_type in REQUIRED_FIELDS.items():
        value = data[key]
        if not isinstance(value, expected_type):
            if isinstance(expected_type, tuple):
                expected_name = " or ".join(t.__name__ for t in expected_type)
            else:
                expected_name = expected_type.__name__
            raise ValidationError(
                f"Field '{key}' must be {expected_name}, got {type(value).__name__}"
            )

    if not (0 <= float(data["retry_rate"]) <= 1):
        raise ValidationError("retry_rate must be between 0 and 1")
    if not (0 <= float(data["error_rate"]) <= 1):
        raise ValidationError("error_rate must be between 0 and 1")
    if int(data["requests"]) < 0:
        raise ValidationError("requests must be >= 0")


def audit(data: dict) -> dict:
    risks = []
    actions = []

    retry_rate = float(data.get("retry_rate", 0))
    p95 = float(data.get("p95_latency_ms", 0))
    err = float(data.get("error_rate", 0))
    notes = str(data.get("notes", "")).lower()

    if retry_rate > THRESHOLDS["retry_rate"]:
        risks.append({"level": "warn", "code": "retry_loop_risk", "value": retry_rate, "threshold": THRESHOLDS["retry_rate"]})
        actions.append("バックオフ設定と最大再試行回数を見直す")

    if p95 > THRESHOLDS["p95_latency_ms"]:
        risks.append({"level": "warn", "code": "latency_degradation", "value": p95, "threshold": THRESHOLDS["p95_latency_ms"]})
        actions.append("高遅延区間を分離し、入力サイズ上限を設定する")

    if err > THRESHOLDS["error_rate"]:
        risks.append({"level": "warn", "code": "error_rate_spike", "value": err, "threshold": THRESHOLDS["error_rate"]})
        actions.append("エラーログを分類し、上位2原因を当日中に封じる")

    if any(k in notes for k in ["timeout", "429", "rate limit", "deploy"]):
        risks.append({"level": "info", "code": "notes_alert_keyword", "value": data.get("notes", ""), "threshold": "n/a"})
        actions.append("notes起因の事象を再現し、監視メトリクスに追加する")

    if not risks:
        summary = "主要指標は閾値内で安定。現行運用を継続可能。"
        actions = ["現行設定を維持しつつ、週次で閾値再評価を行う"]
    else:
        summary = "再試行率・遅延・エラーのいずれかで悪化兆候あり。即日チューニング推奨。"

    result = {
        "project_id": data.get("project_id"),
        "date": data.get("date"),
        "summary": summary,
        "risks": risks,
        "actions": actions,
        "next_check": {
            "retry_rate_lte": THRESHOLDS["retry_rate"],
            "p95_latency_ms_lte": THRESHOLDS["p95_latency_ms"],
            "error_rate_lte": THRESHOLDS["error_rate"],
        },
    }
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python ops_audit_cli.py <input.json> [output.json]", file=sys.stderr)
        sys.exit(1)

    input_path = Path(sys.argv[1])

    try:
        data = load_json(input_path)
        validate_input(data)
        report = audit(data)
    except FileNotFoundError:
        print(f"Input file not found: {input_path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(3)
    except ValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(4)

    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
        output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote report: {output_path}")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
