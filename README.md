# Tweet Generator
There are several corpora used for this project.
Each of them have a character count appended near the end, indicating how difficult it would be for this program to analyze it.
For example, dracula_850 has 850 characters, thus making it a difficult for this program to analyze.
The default is sherlock_300.

Run locally with `python -m flask --app src.app run`; run tests with `python -m unittest discover -s tests`.
Python 3.10 or newer is required.
Run lint with `ruff check .`.

The homepage generates a tweet draft.
Click **Tweet This!** to post it to Bluesky.

## Website
https://projects.nebuloid.dev/tweet-generator

## Deployment
The Flask app runs on Render using the included `render.yaml` Blueprint.
1. Create a Render Blueprint from this repository.
	The Blueprint tracks `main`, enables automatic deploys, and configures a health check.
2. Set `BLUESKY_APP_PASSWORD` to a Bluesky app password in Render.
	Do not commit  the password to the repository.
3. Deploy the service and verify it at the Render URL, adding `/tweet-generator`  to the URL to load the app.

Custom-domain routing will be configured separately after the Render service
is running.

## Bluesky Account
https://bsky.app/profile/frankensteinengine.bsky.social
