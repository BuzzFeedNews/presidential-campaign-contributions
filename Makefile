default:

DIR?=data
compress:
	find $(DIR) -name "*.csv" -exec gzip -v -k -n -f {} \;

decompress:
	find $(DIR) -name "*.csv.gz" -exec gzip -d -v -k -f {} \;

.PHONY: now
now:
	@echo $$(date)

filings/%.csv: now
	python scripts/fetch_latest_filings_list.py $* > $@

filings/2016: $(wildcard filings/2016/*.csv)
filings/2012: $(wildcard filings/2012/*.csv)
filings/2008: $(wildcard filings/2008/*.csv)

filings: $(shell find filings -depth 1 -type d)

data/2016: $(shell find data/2016 -depth 1 -type d)
data/2012: $(shell find data/2012 -depth 1 -type d)
data/2008: $(shell find data/2008 -depth 1 -type d)
data: $(shell find data -depth 1 -type d)

$(shell find data -depth 2 -type d): now
	sh scripts/refresh_data.sh $@
