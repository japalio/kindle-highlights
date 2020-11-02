import math
import random

MIN_HIGHLIGHTS = 5
NUM_BOOKS_TO_SAMPLE = 3
NUM_HIGHLIGHTS_TO_SAMPLE = 2

# Converts the full input json into a map of book title (string) -> list of highlights ([string]).
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

# Select books and quotes uniformly at random without replacement.
def select_uniformly(highlights):
    selected_highlights = {}
    books = random.sample(highlights.keys(), NUM_BOOKS_TO_SAMPLE)
    for book in books:
        sampled_highlights = random.sample(highlights[book], NUM_HIGHLIGHTS_TO_SAMPLE)
        selected_highlights[book] = sampled_highlights

    return selected_highlights

# Select books with weighted sampling. A book's weight is equal to the square root of the number of highlights the book has.
# Example: If book A has 9 highlights, book B has 100 highlights, and book C has 36 highlights, they will be sampled with
# weights 3, 10, and 6 respectively. Highlights are still sampled uniformly at random.
def select_weighted(highlights):
    book_list = list(highlights.keys())
    weight_list = [math.sqrt(len(highlights[book])) for book in book_list]
    selected_highlights = {}
    books = weighted_sample(book_list, weight_list, NUM_BOOKS_TO_SAMPLE)
    for book in books:
        sampled_highlights = random.sample(highlights[book], NUM_HIGHLIGHTS_TO_SAMPLE)
        selected_highlights[book] = sampled_highlights

    return selected_highlights

# Given a list of elements to sample from, an equal sized list of weights for each element, 
# and a number of elements to sample, sample num elements according to the weights. Elements
# are sampled without replacement. 
def weighted_sample(elems, weights, num):
    # If there are fewer elements than num, return elems.
    if len(elems) <= num:
        return elems

    # Record the selected elements in a set to ensure elements are selected without replacement.
    selected = set()

    # Keep selecting elements until num distinct elements have been selected. No repeats.
    while len(selected) < num:

        # Perform weighted sampling by selecting a random number between 0 and the sum of all weights.
        r = random.random() * sum(weights)
        total = 0.0

        # Iterate over all the elemnts to find the weight interval that the random value falls between.
        for i, elem in enumerate(elems):
            total += weights[i]

            # Once the cumulative sum of weights is greater than the random value, the current element is selected.
            if r <= total:
                selected.add(elem)
                break

    # Return the selected unique elements as a list.
    return list(selected)

