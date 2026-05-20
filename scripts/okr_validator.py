import sys
import json

def validate_okr_structure(data):
    """
    校验 OKR 结构的规范性：
    1. O (Objective) 必须存在且非空。
    2. KR (Key Results) 至少要有 2 个，最多 5 个。
    3. 每个 KR 必须是字符串且非空。
    """
    issues = []
    
    if not data.get("objective"):
        issues.append("缺少目标 (Objective)")
    
    krs = data.get("key_results", [])
    if not isinstance(krs, list):
        issues.append("关键结果 (Key Results) 必须是列表格式")
    else:
        if len(krs) < 2:
            issues.append(f"关键结果数量过少 ({len(krs)}个)，建议至少 2 个")
        if len(krs) > 5:
            issues.append(f"关键结果数量过多 ({len(krs)}个)，建议不超过 5 个")
        
        for i, kr in enumerate(krs):
            if not kr or not str(kr).strip():
                issues.append(f"第 {i+1} 个关键结果为空")

    return {
        "is_valid": len(issues) == 0,
        "issues": issues
    }

if __name__ == "__main__":
    # 从命令行接收 JSON 字符串
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No input provided"}))
        sys.exit(1)
    
    try:
        input_data = json.loads(sys.argv[1])
        result = validate_okr_structure(input_data)
        print(json.dumps(result, ensure_ascii=False))
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON format"}))
        sys.exit(1)
