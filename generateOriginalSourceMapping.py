from collections import defaultdict
import os

from engine.sourceManager import initSourceManager, getSourceByUrl


SQL = """
CREATE TEMPORARY TABLE `repeated_urls` (
  `url` varbinary(600) DEFAULT NULL,
  PRIMARY KEY (`url`)
);

insert into repeated_urls (select url from items group by url having count(*) > 1);

select url, id, sourceUrl from items where url in (select url from repeated_urls);
"""

DUMP_PATH = 'var/duplicateUrls.txt'
DATA_DUMP_COMMAND = "echo '%s' | ~/bin/dbConnect.sh > %s" % (SQL, DUMP_PATH)
OUT_FILE_PATH = 'var/duplicateUrlToOriginalid.txt'


# Dump the raw data needed.
sys_ret = os.system(DATA_DUMP_COMMAND)
assert(sys_ret == 0)

# Parse data dump. Aggregate by URL.
data_file = open(DUMP_PATH)
data_file.readline()  # ignore header
url_to_source_url_and_id_tuple = defaultdict(lambda: [])

for line in data_file:
    line = line.rstrip()
    (url, id, source_url) = line.split('\t')
    url_to_source_url_and_id_tuple[url].append((source_url, id))
data_file.close()

initSourceManager()

# Find URLs that are included from at least one aggregator source and one non aggregator source.
aggregator_url_to_original_id = {}
for url, tuple_list in url_to_source_url_and_id_tuple.iteritems():
    has_aggregator_source, non_aggregator_id = False, None

    for t in tuple_list:
        (cur_source_url, cur_id) = t
        cur_source = getSourceByUrl(cur_source_url)

        if cur_source.isAggregator():
            has_aggregator_source = True
        else:
            non_aggregator_id = cur_id

    if has_aggregator_source and non_aggregator_id:
        aggregator_url_to_original_id[url] =  non_aggregator_id


# Write urlToOriginalId to disk.
print "Writting final data to disk."
PRIMARY_DELIMITOR = '\001'
out_file = open(OUT_FILE_PATH, 'w')
for key, value in aggregator_url_to_original_id.iteritems():
    line = PRIMARY_DELIMITOR.join([key, value])
    out_file.write(line + '\n')
out_file.close()

print '[Done]'
