import random

MIN_HIGHLIGHTS = 5
NUM_BOOKS_TO_SAMPLE = 3
NUM_HIGHLIGHTS_TO_SAMPLE = 2

def parse_highlights(highlights_json):
    books_to_highlights = {}
    for book in highlights_json["books"]:
        # Ignore books that have fewer than MIN_HIGHTLIGHTS highlights
        if len(book["highlights"]) < 5:
            continue

        title = book["title"]
        books_to_highlights[title] = []

        for highlight in book["highlights"]:
            books_to_highlights[title].append(highlight["text"])

    return books_to_highlights

def sample_uniformly(highlights):
    selected_highlights = {}
    books = random.sample(highlights.keys(), NUM_BOOKS_TO_SAMPLE)
    for book in books:
        highlights = random.sample(highlights[book], NUM_HIGHLIGHTS_TO_SAMPLE)
        selected_highlights[book] = highlights

    return selected_highlights

def sample_weighted(hightlights):
    pass

