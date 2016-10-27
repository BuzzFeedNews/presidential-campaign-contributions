#!/usr/bin/env python
import requests
import argparse
import csv
import sys, os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("filings",
        type=argparse.FileType("r"),
        nargs="?",
        default=sys.stdin
    )
    args = parser.parse_args()
    return args

SCHED_A_FIELDS = [ "form_type", "filer_committee_id_number", "transaction_id", "back_reference_tran_id_number", "back_reference_sched_name", "entity_type", "contributor_organization_name", "contributor_last_name", "contributor_first_name", "contributor_middle_name", "contributor_prefix", "contributor_suffix", "contributor_street_1", "contributor_street_2", "contributor_city", "contributor_state", "contributor_zip", "election_code", "election_other_description", "contribution_date", "contribution_amount", "contribution_aggregate", "contribution_purpose_descrip", "contributor_employer", "contributor_occupation", "donor_committee_fec_id", "donor_committee_name", "donor_candidate_fec_id", "donor_candidate_last_name", "donor_candidate_first_name", "donor_candidate_middle_name", "donor_candidate_prefix", "donor_candidate_suffix", "donor_candidate_office", "donor_candidate_state", "donor_candidate_district", "conduit_name", "conduit_street1", "conduit_street2", "conduit_city", "conduit_state", "conduit_zip", "memo_code", "memo_text_description", "reference_code" ]

SCHED_B_FIELDS = [ "form_type", "filer_committee_id_number", "transaction_id", "back_reference_tran_id_number", "back_reference_sched_name", "entity_type", "payee_organization_name", "payee_last_name", "payee_first_name", "payee_middle_name", "payee_prefix", "payee_suffix", "payee_street_1", "payee_street_2", "payee_city", "payee_state", "payee_zip", "election_code", "election_other_description", "expenditure_date", "expenditure_amount", "semi_annual_refunded_bundled_amt", "expenditure_purpose_descrip", "category_code", "beneficiary_committee_fec_id", "beneficiary_committee_name", "beneficiary_candidate_fec_id", "beneficiary_candidate_last_name", "beneficiary_candidate_first_name", "beneficiary_candidate_middle_name", "beneficiary_candidate_prefix", "beneficiary_candidate_suffix", "beneficiary_candidate_office", "beneficiary_candidate_state", "beneficiary_candidate_district", "conduit_name", "conduit_street_1", "conduit_street_2", "conduit_city", "conduit_state", "conduit_zip", "memo_code", "memo_text_description", "reference_code" ]

FIELDS = {
    "SA17A": SCHED_A_FIELDS,
    "SA18": SCHED_A_FIELDS,
    "SB28A": SCHED_B_FIELDS,
}

URL_TEMPLATE = "http://docquery.fec.gov/dcdev/posted/{filing_id}.fec"

def get_filing_lines(filing_id):
    url = URL_TEMPLATE.format(filing_id=filing_id)
    sys.stderr.write(url + "\n")
    res = requests.get(url, headers={ "User-Agent": None })
    contribs = [ line.split("\x1C")
        for line in res.content.decode("latin-1").split("\n") ]
    return contribs

def write_lines(lines, form_type, file_obj):
    writer = csv.writer(file_obj)
    writer.writerow(FIELDS[form_type])
    writer.writerows((line for line in lines
        if line[0] == form_type))

FORM_TYPES = [
    "SA17A", # Individual contributions
    "SA18", # Transfers from other authorized committees
    "SB28A", # Refunds to individuals
]

if __name__ == "__main__":
    args = parse_args()
    filings = csv.DictReader(args.filings)
    for filing in filings:
        cycle = filing["cycle"]
        cid = filing["fec_uri"].split("/")[-3]
        directory = "data/{0}/{1}".format(cycle, cid)
        if not os.path.exists(directory):
            os.makedirs(directory)
        lines = get_filing_lines(filing["id"])
        for form_type in FORM_TYPES:
            fname = "{0}-{1}-from-{2}-to-{3}.csv".format(
                cid,
                form_type,
                filing["date_coverage_from"],
                filing["date_coverage_to"]
            )
            dest = os.path.join(directory, fname)
            with open(dest, "w") as f:
                write_lines(lines, form_type, f)
