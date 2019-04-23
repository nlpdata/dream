DREAM
=====
Overview
--------
This repository maintains **DREAM**, a multiple-choice **D**ialogue-based **REA**ding comprehension exa**M**ination dataset.

* Paper: https://arxiv.org/abs/1902.00164
```
@article{sundream2018,
  title={{DREAM}: A Challenge Dataset and Models for Dialogue-Based Reading Comprehension},
  author={Sun, Kai and Yu, Dian and Chen, Jianshu and Yu, Dong and Choi, Yejin and Cardie, Claire},
  journal={Transactions of the Association for Computational Linguistics},
  year={2019},
  url={https://arxiv.org/abs/1902.00164v1}
}
```

* Leaderboard: https://dataset.org/dream/

Files in this repository:

* ```data``` folder: the dataset.
* ```annotation``` folder: question type annotations.
* ```dsw++``` folder: code of DSW++.
* ```ftlm++``` folder: code of FTLM++.
* ```license.txt```: the license of DREAM.
* ```websites.txt```: list of websites used for the data collection of DREAM.

Dataset
-------
```data/train.json```, ```data/dev.json``` and ```data/test.json``` are the training, development and test sets, respectively. The format of them is as follows:

```
[
  [
    [
      dialogue 1 / turn 1,
      dialogue 1 / turn 2,
      ...
    ],
    [
      {
        "question": dialogue 1 / question 1,
        "choice": [
          dialogue 1 / question 1 / answer option 1,
          dialogue 1 / question 1 / answer option 2,
          dialogue 1 / question 1 / answer option 3
        ],
        "answer": dialogue 1 / question 1 / correct answer option
      },
      {
        "question": dialogue 1 / question 2,
        "choice": [
          dialogue 1 / question 2 / answer option 1,
          dialogue 1 / question 2 / answer option 2,
          dialogue 1 / question 2 / answer option 3
        ],
        "answer": dialogue 1 / question 2 / correct answer option
      },
      ...
    ],
    dialogue 1 / id
  ],
  [
    [
      dialogue 2 / turn 1,
      dialogue 2 / turn 2,
      ...
    ],
    [
      {
        "question": dialogue 2 / question 1,
        "choice": [
          dialogue 2 / question 1 / answer option 1,
          dialogue 2 / question 1 / answer option 2,
          dialogue 2 / question 1 / answer option 3
        ],
        "answer": dialogue 2 / question 1 / correct answer option
      },
      {
        "question": dialogue 2 / question 2,
        "choice": [
          dialogue 2 / question 2 / answer option 1,
          dialogue 2 / question 2 / answer option 2,
          dialogue 2 / question 2 / answer option 3
        ],
        "answer": dialogue 2 / question 2 / correct answer option
      },
      ...
    ],
    dialogue 2 / id
  ],
  ...
]
```

Question Type Annotations
-------------------------

```annotation/{annotator1,annotator2}_{dev,test}.json``` are the question type annotations for 25% questions in the development and test sets from two annotators.

In accordance with the format explanation above, the question index starts from ```1```.

We adopt the following abbreviations:

| Abbreviation | Question Type | 
| ------------ | ------------- |
| m            | matching      |
| s            | summary       |
| l            | logic         |
| a            | arithmetic    |
| c            | commonsense   |

Code
----

* DSW++

  1. Copy the data folder ```data``` to ```dsw++/```.
  2. Download ```numberbatch-en-17.06.txt.gz``` from https://github.com/commonsense/conceptnet-numberbatch, and put it into ```dsw++/data/```.
  3. In ```dsw++```, execute ```python run.py```.
  4. Execute ```python evaluate.py``` to get the accuracy on the test set.

* FTLM++

  1. Download the pre-trained language model from https://github.com/openai/finetune-transformer-lm, and copy the model folder ```model``` to ```ftlm++/```.
  2. Copy the data folder ```data``` to ```ftlm++/```.
  3. In ```ftlm++```, execute ```python train.py --submit```. You may want to also specify ```--n_gpu``` (e.g., 4) and ```--n_batch``` (e.g., 2) based on your environment.
  4. Execute ```python evaluate.py``` to get the accuracy on the test set.


**Note**: The results you get may be slightly different from those reported in the paper. For example, the dev and test accuracy for DSW++ in this repository is 51.2 and 50.2 respectively, while the reported accuracy in the paper is 51.4 and 50.1. That is due to (1) we refactor the code with different dependencies to make it portable, and (2) some of the code is non-deterministic due to GPU non-determinism.

**Environment**: The code has been tested with Python 3.6/3.7 and Tensorflow 1.4

Other Useful Code
-----------------
You can refer to [this repository](https://github.com/nlpdata/mrc_bert_baseline) for a finetuned transformer baseline based on BERT.
