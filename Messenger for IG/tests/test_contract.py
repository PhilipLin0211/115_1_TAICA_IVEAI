"""
tests/test_contract.py
驗證 docs/CONTRACT.md 定義的資料結構、JSON 格式與事件類型是否合規且無語法錯誤。
"""

import json
import re
from pathlib import Path


def extract_json_blocks_from_markdown(md_path: Path):
    """從 Markdown 檔案中提取所有 ```json 區塊並驗證是否為合法 JSON"""
    content = md_path.read_text(encoding="utf-8")
    json_blocks = re.findall(r"```json\n(.*?)\n```", content, re.DOTALL)
    valid_data = []

    for idx, block in enumerate(json_blocks, start=1):
        # 僅移除獨立註解或非 URL 中的 // 註解（避免把 https:// 誤判為註解）
        cleaned = re.sub(r"(?<!:)\/\/.*$", "", block, flags=re.MULTILINE)
        try:
            parsed = json.loads(cleaned)
            valid_data.append((idx, parsed))
        except json.JSONDecodeError as e:
            raise AssertionError(f"JSON 區塊 #{idx} 解析失敗: {e}\n內容:\n{block}")

    return valid_data


def test_contract_json_blocks():
    contract_path = Path(__file__).resolve().parent.parent / "docs" / "CONTRACT.md"
    assert contract_path.exists(), f"{contract_path} 不存在！"

    blocks = extract_json_blocks_from_markdown(contract_path)
    assert len(blocks) >= 8, f"契約應包含至少 8 個範例 JSON 區塊，目前僅找到 {len(blocks)} 個"

    print(f"✅ 成功驗證 docs/CONTRACT.md 中的 {len(blocks)} 個 JSON 資料區塊，語法皆合規！")


def test_required_event_types():
    contract_path = Path(__file__).resolve().parent.parent / "docs" / "CONTRACT.md"
    content = contract_path.read_text(encoding="utf-8")

    required_keywords = [
        "NEW_MESSAGE",
        "THREAD_READ_SYNC",
        "SEND_MESSAGE",
        "SEND_RESULT",
        "MESSAGE_RECEIVED",
        "MESSAGE_ACK",
        "MARK_READ",
        "PING",
        "PONG",
        "ERR_AGENT_OFFLINE",
        "ERR_SEND_TIMEOUT",
        "ERR_AUTH_INVALID",
        "ERR_INPUT_BLOCKED",
    ]

    for kw in required_keywords:
        assert kw in content, f"CONTRACT.md 缺少必要通訊事件或錯誤代碼: {kw}"

    print(f"✅ 成功驗證 CONTRACT.md 包含所有關鍵事件與錯誤碼 ({len(required_keywords)} 項)！")


if __name__ == "__main__":
    try:
        test_contract_json_blocks()
        test_required_event_types()
        print("\n🎉 區塊 0：通訊契約驗證全部通過！零語法錯誤！")
    except Exception as e:
        print(f"\n❌ 驗證失敗: {e}")
        exit(1)
