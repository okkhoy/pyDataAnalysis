create view freqWithQuery as
SELECT * FROM frequency
UNION
SELECT 'q' as docid, 'washington' as term, 1 as count 
UNION
SELECT 'q' as docid, 'taxes' as term, 1 as count
UNION 
SELECT 'q' as docid, 'treasury' as term, 1 as count
;

CREATE VIEW freqWithQueryT as 
select term as transposeTerm, docid as transposeDocid, count as transposeCount from freqWithQuery;

create view similarityWithQuery as 
 select freqWithQuery.docid as doc1, freqWithQueryT.transposeDocid as doc2, sum (freqWithQuery.count * freqWithQueryT.transposeCount) as sim
 from freqWithQuery, freqWithQueryT
 where freqWithQuery.term = freqWithQueryT.transposeTerm and freqWithQuery.docid < freqWithQueryT.transposeDocid
 group by freqWithQuery.docid, freqWithQueryT.transposeDocid;


