
import sys
import os
from typing import List, Dict

# Mock the logic from main.py to avoid importing the whole file and its dependencies
def load_frequency_words_mock(content: str) -> List[Dict]:
    word_groups = [group.strip() for group in content.split("\n\n") if group.strip()]
    processed_groups = []

    for group in word_groups:
        words = [word.strip() for word in group.split("\n") if word.strip()]
        group_required_words = []
        group_normal_words = []
        
        for word in words:
            if word.startswith("#"): continue
            if word.startswith("+"):
                group_required_words.append(word[1:])
            else:
                group_normal_words.append(word)

        if group_required_words or group_normal_words:
            processed_groups.append({
                "required": group_required_words,
                "normal": group_normal_words,
                "group_key": " ".join(group_normal_words) if group_normal_words else " ".join(group_required_words)
            })
    return processed_groups

def matches_word_groups_mock(title: str, word_groups: List[Dict]) -> bool:
    if not title.strip(): return False
    title_lower = title.lower()
    
    print(f"\nTesting Title: '{title}'")

    for group in word_groups:
        required_words = group["required"]
        normal_words = group["normal"]
        
        print(f"  Checking Group: {group['group_key'][:20]}...")
        print(f"    Required: {required_words}")
        print(f"    Normal: {normal_words}")

        # Required words check
        if required_words:
            missing_required = [w for w in required_words if w.lower() not in title_lower]
            if missing_required:
                print(f"    ❌ Failed: Missing required words {missing_required}")
                continue
            else:
                print(f"    ✅ All required words present")

        # Normal words check
        if normal_words:
            present_normal = [w for w in normal_words if w.lower() in title_lower]
            if not present_normal:
                print(f"    ❌ Failed: No normal words found")
                continue
            else:
                print(f"    ✅ Found normal words: {present_normal}")

        print("  ✨ MATCHED!")
        return True

    print("  🚫 No match found in any group")
    return False

# Data from user's XML
test_titles = [
    "Show GN: Cresco - 국내 주식 모바일 AI 에이전트 '이제 주식 분석도 해 봐야죠!'",
    "AI 프로토타이핑 도구 완벽 가이드",
    "도구가 많을수록 AI가 멍청해진다: Dropbox Dash 팀의 Context Engineering 전략",
    "AI 에이전트를 마케팅에 활용하는 방법"
]

# Read actual config file
try:
    with open("config/frequency_words.txt", "r", encoding="utf-8") as f:
        config_content = f.read()
except FileNotFoundError:
    print("Error: config/frequency_words.txt not found")
    sys.exit(1)

print("=== Loading Configuration ===")
groups = load_frequency_words_mock(config_content)
print(f"Loaded {len(groups)} word groups.")

print("\n=== Starting Test ===")
matched_count = 0
for title in test_titles:
    if matches_word_groups_mock(title, groups):
        matched_count += 1

print(f"\nTotal Matched: {matched_count}/{len(test_titles)}")
