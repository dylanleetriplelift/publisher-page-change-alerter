# publisher-page-change-alerter
Detects possible placement breaking changes by checking XPaths and CSS of divs containing ads on top spending domains against past values.

### Usage
* python alertermaster.py

### Expected Output
Console logs of analyses for each domain. Specifically, 1. # of ad slots found, 2. XPath changes, 3. CSS changes

## Processing
- Iterates through master list of 'bundles'. Each 'bundle' is a list in the following form: ['domain', [list of all expected XPaths], list of all CSS rules]].
- XPaths and CSS rules are ordered in their respective lists by the position of their corresponding ad slot on the DOM tree
- Attempts to load page. Delays until end of script upon failure.
- Attempts to locate expected number of ads by selecting for a div with id containing 'google_ads_iframe'. Delays until end of script upon failure.
- Genereates XPaths for found div handles and checks against expected XPaths. Reports changes.
- Genereates CSS rules for found div handles and checks against expected CSS rules. Reports changes.
- Attempts to reload pages that failed to load before. If successful, attempts to load expected number of ads.
- If incorrect number of ad slots appears, script matches as many found ads as it can to expected XPaths.
- Matched ads then have CSS rules checked for changes.
- Final report lays out all sites with changes.
