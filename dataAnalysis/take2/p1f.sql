select count (*) from (
  select  docid from frequency where term="transactions" 
  intersect
  select  docid from frequency where term="world"
);
