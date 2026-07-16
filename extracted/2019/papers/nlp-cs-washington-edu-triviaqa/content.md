## TriviaQA: A Large Scale Dataset for Reading Comprehension and Question Answering

| TriviaQA is a reading comprehension dataset containing over 650K question-answer-evidence triples. TriviaQA includes 95K question-answer pairs authored by trivia enthusiasts and independently gathered evidence documents, six per question on average, that provide high quality distant supervision for answering the questions. The details can be found in our ACL 17 paper [TriviaQA: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension](https://arxiv.org/abs/1705.03551)   |    |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----|

Mandar Joshi, Eunsol Choi, Daniel Weld, Luke Zettlemoyer. [TriviaQA: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension](https://arxiv.org/abs/1705.03551) In Association for Computational Linguistics (ACL) 2017, Vancouver, Canada.
[ [bib](bibs/triviaqa.bib) ]

## News

##### Jul 2017

The TriviaQA [leaderboard](https://competitions.codalab.org/competitions/17208) is now live on Codalab. Submit your predictions for evaluation on the test set!

## Data

If you are interested in the reading comprehension task motivated in the paper, click on the link below to download the data.

[Download TriviaQA version 1.0 for RC (2.5G)](data/triviaqa-rc.tar.gz)

If you are interested in open domain QA, click on the link below to download the data. It contains the unfiltered dataset with 110K question-answer pairs. The Wikipedia and top 10 search documents can be obtained from the RC version. The main difference between the RC version above and the unfiltered dataset is that not all documents (in the unfiltered set) for a given question contain the answer string(s). This makes the unfiltered dataset more appropriate for IR-style QA.

[Download unfiltered TriviaQA version 1.0 (604M)](data/triviaqa-unfiltered.tar.gz)

The University of Washington does not own the copyright of the questions and documents included in TriviaQA.

## Code

Check out our [Github](https://github.com/mandarjoshi90/triviaqa) repository.

## Contact

For any questions about the code or data, please contact [Mandar Joshi](http://homes.cs.washington.edu/~mandar90) -- **{first name of the first author}90[at]cs[dot]washington[dot]edu**