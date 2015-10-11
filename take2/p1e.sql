 select count(*) from ( select sum(count) from frequency group by docid having sum(count) > 300 );
