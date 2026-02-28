from typing import TypedDict, List, Dict

class LectureState(TypedDict, total=False):
    audio_path: str
    raw_segments: List[Dict]
    cleaned_text: str
    semantic_chunks: List[str]
    topics: List[str]
    summaries: List[str]
    keywords: List[List[str]]
    structured_notes: List[Dict]
    global_context: str
    validation_passed: bool