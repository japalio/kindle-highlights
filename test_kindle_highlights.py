import json
import kindle_highlights

LARGE_EXAMPLE_HIGHLIGHTS_FILENAME = "large_example_highlights.json"

def print_selected_highlights(selected_highlights):
    for book in selected_highlights:
        print(book)
        for i, highlight in enumerate(selected_highlights[book]):
            print(str(i) + ": " + highlight)
        print("\n")

def main():
    with open(LARGE_EXAMPLE_HIGHLIGHTS_FILENAME) as f:
        highlights = json.load(f)
        parsed_highlights = kindle_highlights.parse_highlights(highlights)
        selected_highlights = kindle_highlights.select_weighted(parsed_highlights)
        print_selected_highlights(selected_highlights)


if __name__ == "__main__":
    main()
