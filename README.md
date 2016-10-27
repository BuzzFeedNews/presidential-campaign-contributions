# Presidential Campaign Contributions

*Last updated: October 26, 2016*

## What

For each recent U.S. presidential candidate's principal campaign committee, this repository contains the following data:

- All __itemized contributions__ (Form 3P, Schedule A, Line 17a)
- All __transfers from other authorized committees__ (Form 3P, Schedule A, Line 18), including the alloted portions of individual contributions to joint-fundraising committees.
- All __refunds to individuals__ (Form 3P, Schedule B, Line 28a)

## Why

This is all data *you* could get from the Federal Election Commission, but we've gone through the trouble of fetching and formatting it for you. Specifically, we've:

- __Identified the latest versions__ of each committee's F3P filings. (Committees often amended their filings, sometimes multiple times for a single filing.)
- __Extracted__ the SA17A, SA18, and SB28A lines from the broader filings (which also contain disbursements to vendors, loans, et cetera). 
- __Converted__ the FEC's `ASCII 28`-delimited format into comma-delimited files, and added header rows with field names.

## Committees

The data currently covers these committees:

| Cycle | Committee Name                        | Committee ID |
|-------|---------------------------------------|--------------|
| 2016  | HILLARY FOR AMERICA                   | C00575795    |
| 2016  | DONALD J. TRUMP FOR PRESIDENT, INC.   | C00580100    |
| 2016  | GARY JOHNSON 2016                     | C00605568    |
| 2016  | JILL STEIN FOR PRESIDENT              | C00581199    |
| 2016  | MCMULLIN FOR PRESIDENT COMMITTEE INC. | C00623884    |
| 2012  | OBAMA FOR AMERICA                     | C00431445    |
| 2012  | ROMNEY FOR PRESIDENT, INC.            | C00431171    |
| 2012  | GARY JOHNSON 2012 INC                 | C00495622    |
| 2012  | JILL STEIN FOR PRESIDENT              | C00505800    |
| 2008  | OBAMA FOR AMERICA                     | C00431445    |
| 2008  | JOHN MCCAIN 2008 INC.                 | C00430470    |

## Filings

The [`filings/` directory](filings/) contains CSVs listing each committee's most recently updated FEC Form F3P submissions for each filing period. These listings were obtained from the [ProPublica Campaign Finance API](https://propublica.github.io/campaign-finance-api-docs/#get-committee-filings).

## Contributions, Transfers, and Refunds

The [`data/` directory](data/) contains all contributions, transfers, and refunds described above, organized as such: `data/{cycle}/{committee}/{committee}-{line_type}-{coverage_period}.csv`.

To save storage (and stay under GitHub's file size limits), all contribution files are compressed with `gzip`. To decompress all files, run `make decompress`.

## Feedback

Contact Jeremy Singer-Vine at jeremy.singer-vine@buzzfeed.com.

Looking for more from BuzzFeed News? [Click here for a list of our open-sourced projects, data, and code.](https://github.com/BuzzFeedNews/everything)
