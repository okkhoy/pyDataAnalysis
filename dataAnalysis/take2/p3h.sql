CREATE VIEW frequencyT as 
select term as transposeTerm, docid as transposeDocid, count as transposeCount from frequency;

create view similarity as 
 select frequency.docid as doc1, frequencyT.transposeDocid as doc2, sum (frequency.count * frequencyT.transposeCount) as sim
 from frequency, frequencyT
 where frequency.term = frequencyT.transposeTerm and frequency.docid < frequencyT.transposeDocid
 group by frequency.docid, frequencyT.transposeDocid;


### alternate:

create view smallFreq as
 select docid, term, count from frequency
 where docid="10080_txt_crude"
 union 
 select docid, term, count from frequency
 where docid="17035_txt_earn"
;

create view smallFreqT as 
 select term, docid,count from smallFreq;

create view smallSimilarity as
 select smallFreq.docid, smallFreqT.docid, sum (smallFreq.count * smallFreqT.count)
 from smallFreq, smallFreqT
 where smallFreq.term = smallFreqT.term
 group by smallFreq.docid, smallFreqT.docid;

