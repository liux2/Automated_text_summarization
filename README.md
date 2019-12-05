# My Meadville Text Analyze Project

This is a project repository for MyMeadville organization. The city of Meadville is located in Crawford County, Pennsylvania.

The goal of this project is to analyze the talking session records and find the interests form guests. The answer will be used to improve the life in Meadville.

## Repository Structure

* `trained_model`: This directory has the trained models that we are going to use.

* `input_files`: This directory has the input files.

* `output_files`: This directory has the final output files.

* `src`: This directory has the source code of the program.

* `experimental_functions`: This directory contains training algorithms and texts.

## Required Dependencies

1. The example shown below uses Linux, python3, and pip3. You can add sudo in front for permission.

  1. [Numpy](https://pypi.org/project/numpy/): `pip3 install -U numpy`

  2. [NLTK](https://www.nltk.org/install.html): `pip3 install -U nltk`.
    * [NLTK datas](https://www.nltk.org/data.html) After installed NLTK, type `python3` then `nltk.download()`. You will see a window pop out, you can choose what package to install. If you have enough storage, you can choose all packages.q

  3. [scikit-learn](https://scikit-learn.org/stable/install.html): `pip3 install -U scikit-learn`

  4. Four dependencies for [pytextrank](https://github.com/ceteri/pytextrank):

    * [spaCy](https://spacy.io/usage/): use `pip3 install -U spacy`, then, use `python3 -m spacy download en` to install English language models.
    * [NetworkX](https://networkx.github.io/documentation/stable/install.html):  `pip3 install networkx`.
    * [datasketch](https://github.com/ekzhu/datasketch): use `pip3 install datasketch -U`.
    * [graphviz](https://pypi.org/project/graphviz/): use `pip3 install graphviz`.
    * Then, use `pip3 install pytextrank` to install `pytextrank`.

2. Besides the python libraries listed above, you also have to install java jdk:

  1. Update the packages: `sudo apt update`.
  2. Install Ubuntu default java jdk: `sudo apt install default-jdk`.
  3. You can verify the version by using `java -version`.

3. And [Stanford NER Tagger](https://nlp.stanford.edu/software/CRF-NER.shtml).

  1. Download Stanford Named Entity Recognizer version x.x.x.
  2. Create `stanford_ner/` directory under `trained_model/`.
  3. Extract `classifiers/` and `stanford-ner.jar`, and put them into `stanford_ner/`.
  4. Make sure the path of the Stanford NER Tagger files are the same with the path in `src/named_entity.py` file.

4. To get the emotions of the text, we need to pickle the training models.

## Library Modifications

There is bug reported in GitHub community, people have proposed a [way](https://github.com/ceteri/pytextrank/issues/15#issuecomment-392323261) to fix the issue. Since, the maintainer haven't updated the program, so we have to do it but ourselves.

1. Navigate to `~/.local/lib/python3.6/site-packages/pytextrank` (Here you should use your version of python directory).
2. Use your favorite text editor (e.g. vim,nano) to open pytexyrank.py.
3. Go to line 193, replace `doc = spacy_nlp(graf_text, parse=True)` with `doc = spacy_nlp(graf_text)`. Go to line 421, replace `doc = spacy_nlp(text.strip(), parse=True)` with `doc = spacy_nlp(text.strip())`. These steps can fix `TypeError: __call__() got an unexpected keyword argument 'parse'`.
4. Go to line 308, replace `graph.edge[pair[0]][pair[1]]["weight"] += 1.0` with `graph.edges[0,1]["weight"] += 1.0`. This step can fix `AttributeError: 'DiGraph' object has no attribute 'edge'`.
5. In order to make sure the `graph.dot` that pytextrank generated doesn't affect out input list, I changed path to `../graph.dot` in line 315 and 331.

## Input Files

For the input file, you have to do some revision for the program to recognize the texts.

1. For the interviewee responses, you have to add 'R:' in front to indicate the function of this paragraph. For example:

```
Interviewer: What do you love about the city of Meadville?

R: The season changes, I love the weather around here.
```

2. You can not have other rich text formats, that means you can not use pictures, charts, etc. If you used charts, you will have to manually change it to plain text format.

3. For the privacy issues, we removed all the transcribe files from the repository. You can make your own files to test the program.

## How to Run

Check the following conditions before run the program:

1. The structure at least looks like:
```
src/
    └| main.py
    └| main_processes.py
    └| named_entity.py
    └| pytextrank_stages.py
    └| sentiment_mod.py
trained_model/
    └| special_signs.txt
    └| pickled_algos/
          └| *.pickle # Bunch of pickle files
      └| stanford_ner/
          └| classifiers/
          └| stanford-ner.jar
input_files/
output_files/
```
2. The dependencies are installed, and modified.
3. The path to trained models in programs are the same as repository structures.
4. If anything is wrong, check back to the sections above.

To run the program, your computer has to have python 3 or higher version of python. Navigate to `src/` directory, and use ```bash proc_script.sh``` to run the program. Always put input files into `input_files/` directory, create one if there is none in the repository. Replace `phrase_limit`, `word_limit_in_sentence` with correct parameters. You can use `pwd` in terminal under the location you want for the correctly formatted path.

Note that, while running the program, there shouldn't be any opened docx file in input directory.

For our transcribes, the answers are marked with `R: ` in front. There should be no images and tables in the docx file.

## Sample Outputs

Here is a sample from document `CONNECTION#36.docx`:
Under *excerpts* section, we have all the top ranked sentences, and under *keywords* section, we have all the top ranked keywords.
```
# CONNECTION#36.docx
**sum:**
**excerpts:**
The season changes , I love the weather around here .
The rural community , hunting , fishing availabilities .
The birth of my children .

...omitted to save space...

**keywords:**
weather, season changes
fishing availabilities
children
family

...omitted to save space...
```
Note that there are only part of sentences and keywords are here to save space.
