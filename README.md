# Tweet Generator
There are several corpora used for this project. Each of them have a character count appended near the end, indicating how difficult it would be for this program to analyze it. For example, dracula_850 has 850 characters, thus making it a difficult for this program to analyze. The default is sherlock_300.

> use `git add .; git commit -m "message";git push;git push heroku` when updating — its important to update heroku!

Run locally with `python -m flask --app src.app run`; run tests with `python -m unittest discover -s tests`.
Python 3.7 or newer is required.
Run lint with `ruff check .`.

The homepage generates a tweet draft. Click **Tweet This!** to post it to
Bluesky.

## Website
https://tweet-generator-nak.herokuapp.com/

## Bluesky Account
https://bsky.app/profile/frankensteinengine.bsky.social
