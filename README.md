# kindle highlights

Hi there! This is the source code for a simple python lambda that selects random Kindle highlights and emails you quotes each day (schedule is configurable)! Hooray for reading retention!

It assumes your highlights are in a specific JSON format and available in an S3 bucket. See `template-public.yml` for more configuration details. 


## Kindle Highlights JSON
Example JSON containing highlights is available at `example_highlights.json.` [Readsmart](https://chrome.google.com/webstore/detail/kindle-highlights-to-read/kghigmohnggnegnoielmjnkhookemobp?hl=en-US) is a Chrome extension you can use to download all your highlights. [Bookcision](https://readwise.io/bookcision) is a bookmarklet you can use to download highlights, although it only support downloading highlights for one book at a time.

Thank you for visiting - happy reading!
