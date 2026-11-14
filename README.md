[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.md)

# Tweet Generator
*This project is live on the web at [**projects.nebuloid.dev/tweet-generator**][tweet-generator-homepage]!*
<br />
*Generated phrases are sent to the [**Frankenstein Generator account on Bluesky**][tweet-generator-bluesky].*

This app generates a random phrase using Frankenstein, and another random open-source book as reference.
Then, it posts the random phrase to Twitter.
The app uses a technology called "Markov Chaining" to accomplish this chatbot-like effect, although it is not nearly as advanced as modern AI would be.
However, it is like a baby version of modern AI, which is certainly interesting!

## Website Routes
| Method | Route                                 | Purpose                                                |
| ------ | ------------------------------------- | ------------------------------------------------------ |
| `GET`  | [/][tweet-generator-homepage]         | The user interface for the tweet generator.            |
| `POST` | [/generate][tweet-generator-function] | Generates a phrase and posts to Bluesky. Returns JSON. |

## Dev Requirements
**Python 3.10** or newer is required.
- Run locally with `python -m flask --app src.app run`.
- Run tests with `python -m unittest discover -s tests`.
- Run the linter with `ruff check .`.

## Deployment
The **Flask** app runs on **Render** using the included `render.yaml` Blueprint.
A **Cloudflare Worker** proxies only `projects.nebuloid.dev/tweet-generator` and its descendants to **Render**; the rest of the site keeps its existing origin.
The repository uses **GitHub Actions** to deploy the `main` branch automatically.

[tweet-generator-homepage]: https://projects.nebuloid.dev/tweet-generator
[tweet-generator-function]: https://projects.nebuloid.dev/tweet-generator/generate
[tweet-generator-bluesky]: https://bsky.app/profile/frankensteinengine.bsky.social
