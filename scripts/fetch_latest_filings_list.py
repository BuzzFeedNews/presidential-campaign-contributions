#!/usr/bin/env python
import requests
import sys, os
import argparse
import datetime
import operator
import json
import csv

def parse_args():
    parser = argparse.ArgumentParser(
        description="Get the latest Federal Election Commission F3 filings for a given committee."
    )
    parser.add_argument("committee_cycle")
    parser.add_argument("--api-key",
        default=os.environ.get("PROPUBLICA_API_KEY"),
        help="ProPublica Campaign Finanance API key."
    )
    args = parser.parse_args()
    return args

def get_current_cycle():
    year = datetime.datetime.now().year
    if year % 2: year += 1
    return year

URL_TEMPLATE = "https://api.propublica.org/campaign-finance/v1/{cycle}/committees/{fec_id}/filings.json"

def get_filings(cycle, committee_id, api_key):
    url = URL_TEMPLATE.format(cycle=cycle, fec_id=committee_id)
    res = requests.get(url, headers={
        "X-API-Key": api_key
    })
    data = res.json()
    if "results" in data:
        return data["results"]
    else:
        raise Exception(json.dumps(data, indent=4))

def filter_filings(filings):
    sorter = operator.itemgetter("date_filed", "id")
    _sorted = reversed(sorted(filings, key=sorter))
    index = set()
    most_recent = []
    for f in _sorted:
        if f["form_type"] != "F3": continue
        ix = (f["cycle"], f["date_coverage_from"], f["date_coverage_to"])
        if ix in index: continue
        most_recent.append(f)
        index.add(ix)
    return list(sorted(most_recent, key=operator.itemgetter("date_coverage_to")))

FIELDS = [
    "id", "cycle", "committee_type", "form_type",
    "date_filed", "date_coverage_from", "date_coverage_to",
    "report_title", "report_period", "paper", 
    "contributions_total", "cash_on_hand", "disbursements_total", "receipts_total",
    "amended", "is_amendment", "original_filing",
    "fec_uri", "original_uri", "amended_uri", 
]

if __name__ == "__main__":
    args = parse_args()
    if args.api_key == None:
        raise Exception("ProPublica Campaign Finanance API key required. Set as PROPUBLICA_API_KEY environment variable, or pass directly on command line.")
    cycle, committee = args.committee_cycle.split("/")
    filings = get_filings(cycle, committee, args.api_key)
    filtered = filter_filings(filings)
    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(filtered)
