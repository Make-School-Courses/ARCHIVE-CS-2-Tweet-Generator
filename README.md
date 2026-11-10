# Tweet Generator
There are several corpora used for this project.
Each of them have a character count appended near the end, indicating how difficult it would be for this program to analyze it.
For example, dracula_850 has 850 characters, thus making it a difficult for this program to analyze.
The default is sherlock_300.

**Python 3.10** or newer is required.
- Run locally with `python -m flask --app src.app run`.
- Run tests with `python -m unittest discover -s tests`.
- Run the linter with `ruff check .`.

## Website
https://projects.nebuloid.dev/tweet-generator

### Routes
| Method | Route                                 | Purpose                                                |
| ------ | ------------------------------------- | ------------------------------------------------------ |
| `GET`  | [/](tweet-generator-homepage)         | The user interface for the tweet generator.            |
| `POST` | [/generate](tweet-generator-function) | Generates a phrase and posts to Bluesky. Returns JSON. |

## Deployment
The Flask app runs on Render using the included `render.yaml` Blueprint.
1. Create a Render Blueprint from this repository.
	The Blueprint tracks `main`, enables automatic deploys, and configures a health check.
2. Set `BLUESKY_APP_PASSWORD` to a Bluesky app password in Render.
	Do not commit  the password to the repository.
3. Deploy the service and verify it at the Render URL, adding `/tweet-generator`  to the URL to load the app.

## Bluesky Account
https://bsky.app/profile/frankensteinengine.bsky.social

[tweet-generator-homepage]: https://projects.nebuloid.dev/tweet-generator
[tweet-generator-function]: https://projects.nebuloid.dev/tweet-generator/generate
