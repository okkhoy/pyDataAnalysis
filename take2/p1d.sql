select count (*) from (
  select distinct docid from frequency where term="law" or term="legal"
);
