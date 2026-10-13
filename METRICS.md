# Profile metrics

All generated SVG surfaces are transparent. Foreground colors follow the embedding page’s light/dark color scheme. Desktop and mobile layouts use picture sources, keeping the original project icons untouched.

GitHub metrics refresh every 6 hours via the repository workflow. Rank uses the MIT-licensed github-readme-stats formula (see scripts/rank-LICENSE.txt); commits and reviews use the current year, PRs/issues use account totals, stars and language bytes use public owned repositories. The current query supports the first 100 owned repositories and 20 languages per repository. The activity chart uses the last 31 calendar days of GitHub contributions. No private repository content is published.

WakaTime setup:
1. Install the official WakaTime VS Code extension.
2. Log in to WakaTime and configure your key through the extension’s “WakaTime API Key” command.
3. Add the same key to this repository’s Actions secret named WAKATIME_API_KEY. Never commit the key.
4. Run Update profile metrics from Actions, or wait for the next scheduled run. Until connected the profile states “WakaTime 尚未連接”; until coding data exists it states that no weekly records exist.

Only aggregate language durations are published. Project names, paths and file names from WakaTime are not included. GitHub failures fail the workflow rather than fabricating numbers; WakaTime failures produce an unavailable status.
