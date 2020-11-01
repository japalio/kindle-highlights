import math
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

def select_uniformly(highlights):
    selected_highlights = {}
    books = random.sample(highlights.keys(), NUM_BOOKS_TO_SAMPLE)
    for book in books:
        sampled_highlights = random.sample(highlights[book], NUM_HIGHLIGHTS_TO_SAMPLE)
        selected_highlights[book] = sampled_highlights

    return selected_highlights

def select_weighted(highlights):
    book_list = list(highlights.keys())
    weight_list = [math.sqrt(len(highlights[book])) for book in book_list]
    selected_highlights = {}
    books = weighted_sample(book_list, weight_list, NUM_BOOKS_TO_SAMPLE)
    for book in books:
        sampled_highlights = random.sample(highlights[book], NUM_HIGHLIGHTS_TO_SAMPLE)
        selected_highlights[book] = sampled_highlights

    return selected_highlights

def weighted_sample(population, weights, num):
    selected = set()
    while len(selected) < num:
        r = random.random() * sum(weights)
        total = 0.0
        for i, elem in enumerate(population):
            total += weights[i]
            if r <= total:
                selected.add(elem)
                break
    return list(selected)

