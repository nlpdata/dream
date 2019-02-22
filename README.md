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
  journal={Transactions of the Association of Computational Linguistics},
  year={2019},
  url={https://arxiv.org/abs/1902.00164v1}
}
```

* Leaderboard: https://dataset.org/dream/

Files in this repository:

* ```data``` folder: the dataset.
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

DSW++
-----
1. Copy the data folder ```data``` to ```dsw++/```.
2. Download ```numberbatch-en-17.06.txt.gz``` from https://github.com/commonsense/conceptnet-numberbatch, and put it into ```dsw++/data/```.
3. In ```dsw++```, execute ```python run.py```.
4. Execute ```python evaluate.py``` to get the accuracy on the test set.

FTLM++
------
1. Download pre-trained language model from https://github.com/openai/finetune-transformer-lm, and copy the model folder ```model``` to ```ftlm++/```.
2. Copy the data folder ```data``` to ```ftlm++/```.
3. In ```ftlm++```, execute ```python train.py --submit```. You may want to also specify ```--n_gpu``` (e.g., 4) and ```--n_batch``` (e.g., 2) based on your environment.
4. Execute ```python evaluate.py``` to get the accuracy on the test set.

Environment
-----------
The code has been tested with Python 3.6/3.7 and Tensorflow 1.4

TODO
----
* Release a finetuned transformer baseline based on BERT for DREAM. (March/April)
