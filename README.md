# kindle highlights

Hi there! This is the source code for a simple python lambda that selects random Kindle highlights and emails you quotes each day (schedule is configurable)! Hooray for reading retention!

It assumes your highlights are in a specific JSON format and available in an S3 bucket. See `template-public.yml` for more configuration details. 


## Kindle Highlights JSON
Example JSON containing highlights is available at `example_highlights.json`.

