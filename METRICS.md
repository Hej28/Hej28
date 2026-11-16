# Profile metrics

All generated SVG surfaces are transparent. Foreground colors follow the embedding page’s light/dark color scheme. Desktop and mobile layouts use picture sources, keeping the original project icons untouched.

GitHub metrics refresh every 6 hours via the repository workflow. Rank uses the MIT-licensed github-readme-stats formula (see scripts/rank-LICENSE.txt); commits and reviews use the current year, PRs/issues use account totals, stars and language bytes use public owned repositories. The current query supports the first 100 owned repositories and 20 languages per repository. The activity chart uses the last 31 calendar days of GitHub contributions. No private repository content is published.

WakaTime setup:
1. Install the official WakaTime VS Code extension.
2. Log in to WakaTime and configure your key through the extension’s “WakaTime API Key” command.
3. Get your personal OAuth token at https://wakatime.com/oauth and save it as this repository’s Actions secret named WAKATIME_ACCESS_TOKEN. API keys are now write-only for editor plugins and cannot read statistics. Keep the editor API key unchanged. Never commit either credential. For compatibility, a personal OAuth token stored in the older WAKATIME_API_KEY secret also works; WAKATIME_ACCESS_TOKEN takes precedence.
4. Run Update profile metrics from Actions, or wait for the next scheduled run. Missing credentials, rejected authorization, calculating statistics, and a connected account with no coding records each have distinct messages. HTTP 401/403 requires updating the OAuth secret; transient failures retry on the next scheduled run. Diagnostics log only HTTP status codes or fixed messages, never credentials or response bodies.

Authentication reference: https://wakatime.com/developers#authentication. The integration uses the OAuth Bearer header on the official API host. It only reads the last seven days of language statistics.

Only aggregate language durations are published. Project names, paths and file names from WakaTime are not included. GitHub failures fail the workflow rather than fabricating numbers; WakaTime failures produce an unavailable status.
