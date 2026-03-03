#!/usr/bin/env python3
"""
Ops Audit CLI - AI運用ログの日次監査ツール
"""

import json
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional


def load_input(filepath: str) -> Dict[str, Any]:
    """入力JSONを読み込む"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_input(data: Dict[str, Any]) -> List[str]:
    """入力データの必須項目を検証"""
    errors = []
    required = ['project_id', 'date', 'inference_cost_usd', 'retry_rate', 'p95_latency_ms', 'error_rate']
    
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: {field}")
    
    # 型・値域チェック
    if 'retry_rate' in data and not (0 <= data['retry_rate'] <= 1):
        errors.append("retry_rate must be between 0 and 1")
    if 'error_rate' in data and not (0 <= data['error_rate'] <= 1):
        errors.append("error_rate must be between 0 and 1")
    if 'inference_cost_usd' in data and data['inference_cost_usd'] < 0:
        errors.append("inference_cost_usd must be >= 0")
    if 'p95_latency_ms' in data and data['p95_latency_ms'] < 0:
        errors.append("p95_latency_ms must be >= 0")
    
    return errors


def check_error_rate(error_rate: float) -> tuple:
    """R1: Error Rate Spike"""
    if error_rate >= 0.05:
        return 'critical', 'Error Rate Spike (>= 5%)'
    elif error_rate >= 0.02:
        return 'warn', 'Error Rate Elevated (>= 2%)'
    return 'ok', None


def check_retry_rate(retry_rate: float) -> tuple:
    """R2: Retry Loop Risk"""
    if retry_rate >= 0.25:
        return 'critical', 'Retry Loop Risk (>= 25%)'
    elif retry_rate >= 0.12:
        return 'warn', 'Retry Rate Elevated (>= 12%)'
    return 'ok', None


def check_latency(p95_latency_ms: float) -> tuple:
    """R3: Latency Degradation"""
    if p95_latency_ms >= 5000:
        return 'critical', 'Latency Critical (P95 >= 5000ms)'
    elif p95_latency_ms >= 2500:
        return 'warn', 'Latency Degraded (P95 >= 2500ms)'
    return 'ok', None


def check_cost_absolute(cost_usd: float) -> tuple:
    """R4: Cost Overrun (Absolute)"""
    if cost_usd >= 50:
        return 'critical', f'Cost Overrun (>= $50, current: ${cost_usd:.2f})'
    elif cost_usd >= 20:
        return 'warn', f'Cost Warning (>= $20, current: ${cost_usd:.2f})'
    return 'ok', None


def check_cost_efficiency(cost_usd: float, requests: Optional[int]) -> tuple:
    """R5: Cost Efficiency Drop"""
    if requests is None or requests == 0:
        return 'ok', None
    
    cost_per_request = cost_usd / requests
    if cost_per_request >= 0.03:
        return 'critical', f'Cost Efficiency Critical (${cost_per_request:.4f}/req)'
    elif cost_per_request >= 0.015:
        return 'warn', f'Cost Efficiency Warning (${cost_per_request:.4f}/req)'
    return 'ok', None


def check_combined_failure(retry_rate: float, error_rate: float) -> tuple:
    """R6: Combined Failure Risk"""
    if retry_rate >= 0.12 and error_rate >= 0.02:
        return 'critical', 'Combined Failure Risk (High retry + error rate)'
    return 'ok', None


def check_latency_cost_coupled(p95_latency_ms: float, cost_usd: float) -> tuple:
    """R7: Latency-Cost Coupled Risk"""
    if p95_latency_ms >= 2500 and cost_usd >= 20:
        return 'critical', 'Latency-Cost Coupled Risk'
    return 'ok', None


def check_silent_failure(requests: Optional[int], error_rate: float, retry_rate: float) -> tuple:
    """R8: Silent Failure Suspicion"""
    if requests and requests > 0 and error_rate == 0 and retry_rate >= 0.15:
        return 'warn', 'Silent Failure Suspicion (Retries with zero errors)'
    return 'ok', None


def check_notes_alert(notes: Optional[str]) -> tuple:
    """R10: Notes Alert Keyword"""
    if not notes:
        return 'ok', None
    
    alert_keywords = ['incident', 'outage', 'timeout', 'rollback']
    notes_lower = notes.lower()
    
    for keyword in alert_keywords:
        if keyword in notes_lower:
            return 'warn', f'Notes Alert Keyword: "{keyword}"'
    
    return 'ok', None


def determine_overall_status(risks: List[Dict]) -> str:
    """全体ステータスを判定"""
    if any(r['level'] == 'critical' for r in risks):
        return 'critical'
    elif any(r['level'] == 'warn' for r in risks):
        return 'warn'
    return 'ok'


def generate_summary(status: str, risks: List[Dict]) -> str:
    """サマリーを生成"""
    if status == 'ok':
        return '全指標正常。運用は安定しています。'
    
    critical_count = sum(1 for r in risks if r['level'] == 'critical')
    warn_count = sum(1 for r in risks if r['level'] == 'warn')
    
    parts = []
    if critical_count > 0:
        parts.append(f'緊急リスク{critical_count}件')
    if warn_count > 0:
        parts.append(f'警告リスク{warn_count}件')
    
    return f"{', '.join(parts)}を検出。対応を検討してください。"


def generate_actions(risks: List[Dict]) -> List[str]:
    """推奨アクションを生成"""
    actions = []
    risk_messages = [r['message'] for r in risks]
    
    # Critical優先のアクション
    if any('Error Rate' in m for m in risk_messages):
        actions.append('失敗タイプ上位3件を抽出し、当日変更との差分確認')
    
    if any('Retry' in m for m in risk_messages):
        actions.append('再試行回数上限とバックオフ戦略を見直す')
    
    if any('Latency' in m for m in risk_messages):
        actions.append('入力長分布とタイムアウト設定を点検')
    
    if any('Cost' in m for m in risk_messages):
        actions.append('高コスト経路上位を特定し、キャッシュ適用を検討')
    
    if any('Silent Failure' in m for m in risk_messages):
        actions.append('ログ欠損・集計漏れを監査')
    
    if any('Notes Alert' in m for m in risk_messages):
        actions.append('手動インシデントレビューを優先')
    
    if any('Combined Failure' in m for m in risk_messages):
        actions.append('プロンプト/ツール失敗を分離して原因切り分け')
    
    # デフォルトアクション（リスクが少ない場合）
    if len(actions) < 2:
        actions.append('翌日の同時間帯と比較し、トレンドを確認')
    
    return actions[:3]  # 最大3件


def generate_next_check(risks: List[Dict]) -> Dict[str, str]:
    """翌日の確認ポイントを生成"""
    next_checks = {}
    risk_messages = [r['message'] for r in risks]
    
    if any('Retry' in m for m in risk_messages):
        next_checks['retry_rate'] = '<= 0.10'
    
    if any('Latency' in m for m in risk_messages):
        next_checks['p95_latency_ms'] = '<= 2500'
    
    if any('Error Rate' in m for m in risk_messages):
        next_checks['error_rate'] = '<= 0.01'
    
    if any('Cost' in m for m in risk_messages):
        next_checks['inference_cost_usd'] = '<= $15.00'
    
    if not next_checks:
        next_checks['status'] = '継続監視'
    
    return next_checks


def audit(data: Dict[str, Any]) -> Dict[str, Any]:
    """監査を実行"""
    risks = []
    
    # 各ルールを実行
    checks = [
        check_error_rate(data.get('error_rate', 0)),
        check_retry_rate(data.get('retry_rate', 0)),
        check_latency(data.get('p95_latency_ms', 0)),
        check_cost_absolute(data.get('inference_cost_usd', 0)),
        check_cost_efficiency(data.get('inference_cost_usd', 0), data.get('requests')),
        check_combined_failure(data.get('retry_rate', 0), data.get('error_rate', 0)),
        check_latency_cost_coupled(data.get('p95_latency_ms', 0), data.get('inference_cost_usd', 0)),
        check_silent_failure(data.get('requests'), data.get('error_rate', 0), data.get('retry_rate', 0)),
        check_notes_alert(data.get('notes')),
    ]
    
    for level, message in checks:
        if level != 'ok':
            risks.append({'level': level, 'message': message})
    
    status = determine_overall_status(risks)
    
    return {
        'project_id': data.get('project_id', 'unknown'),
        'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
        'summary': generate_summary(status, risks),
        'status': status,
        'risks': [f"{r['level']}: {r['message']}" for r in risks],
        'actions': generate_actions(risks),
        'next_check': generate_next_check(risks),
        'input_summary': {
            'inference_cost_usd': data.get('inference_cost_usd'),
            'retry_rate': data.get('retry_rate'),
            'p95_latency_ms': data.get('p95_latency_ms'),
            'error_rate': data.get('error_rate'),
            'requests': data.get('requests'),
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description='Ops Audit CLI - AI運用ログの日次監査ツール',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ops-audit input.json output.json
  ops-audit input.json - --fail-on warn | jq '.risks'
  ops-audit input.json - --fail-on critical
        """
    )
    parser.add_argument('input', help='入力JSONファイルのパス')
    parser.add_argument('output', help='出力JSONファイルのパス（- でstdout）')
    parser.add_argument('--fail-on', choices=['warn', 'critical'], 
                        help='指定レベル以上で終了コード2を返す')
    
    args = parser.parse_args()
    
    # 入力読み込み
    try:
        data = load_input(args.input)
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 入力検証
    errors = validate_input(data)
    if errors:
        for error in errors:
            print(f"Validation Error: {error}", file=sys.stderr)
        sys.exit(1)
    
    # 監査実行
    result = audit(data)
    
    # 出力
    output_json = json.dumps(result, ensure_ascii=False, indent=2)
    
    if args.output == '-':
        print(output_json)
    else:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_json)
    
    # 終了コード判定
    if args.fail_on == 'critical' and result['status'] == 'critical':
        sys.exit(2)
    elif args.fail_on == 'warn' and result['status'] in ['warn', 'critical']:
        sys.exit(2)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
