#!/bin/sh
set -e
CC=$1
function error_exit {
	echo "$1" 1>&2
	exit 1
}
[ -z "$CC" ] && error_exit "Must specify 'cycle/committee'."

CC=$(echo $CC | sed -e 's|^data/||')
FILINGS_CSV="filings/$CC".csv
CONTRIBUTIONS_DIR="data/$CC"
python scripts/fetch_latest_filings_list.py $CC > $FILINGS_CSV
mkdir -p $CONTRIBUTIONS_DIR
python scripts/fetch_data.py < $FILINGS_CSV
