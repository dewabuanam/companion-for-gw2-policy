# Companion for GW2 – Policy

The policy, privacy notice and disclaimer for Companion for GW2, an unofficial Guild Wars 2 fan app, published with GitHub Pages at <https://dewabuanam.github.io/companion-for-gw2-policy/>.

- `policy.json` is the policy itself: the date it last changed, and its sections in English, German, French and Spanish. The app reads this file to show its Policy page, so a change here reaches every install without a new release.
- `index.html` is the page for people, built from `policy.json`.

To change the policy, edit `policy.json`, including its `updated` date. Then run `python build.py` to rebuild `index.html`, and push. English is required; a language missing from the file falls back to English in the app.
