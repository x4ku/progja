# Progressive Japanese

Data and tools for those studying the Japanese language.

## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Stats](#stats)
- [License and Attribution](#license-and-attribution)
- [Contributing](#contributing)

## Overview

This project is a **progressive** approach to learning Japanese: new material
will build upon material that you've already seen before. It uses
*[progressions]* in order to build up an optimized *[path]* of material to learn
in order. Following this path will help lower the difficulty level.

This project was built with the intermediate to advanced learner in mind. You
should be comfortable with Hiragana, Katakana, Japanese pronunciation, and basic
grammar in order to make the most effective use of this project.

There are several great resources out there for beginners, including the
[Duolingo] Japanese course and [Tae Kim's Guide]. Once you've learned the
basics, you can use this project to quickly learn kanji and build up your
vocabulary.

### What is a "progression"?

Most kanji are *compositions* - they are composed of two or more simple
components, combined together to create a more complex character. If you already
know the components that make up a kanji, then it's a much easier task to learn
that kanji. You're just combining what you already know instead of learning
something completely new.

> For example, the composition of the kanji `時` "time, hour" is `日`
> "day, sun" and `寺` "Buddhist temple".

The components in a kanji composition may themselves be composed of other
components.

> `寺` in the previous example is composed of `土` "earth, ground" and `寸`
> "length, measurement".

A *progression* is the complete list of components, in order, that are required
to build a kanji character, including the character itself.

> The progression to build the kanji `時` is: `日`, `土`, `寸`, `寺` and finally
> `時`.

Most words and sentences are also *compositions*.

Words are often composed of two or more kanji, words, or other components (ex.
prefixes and suffixes).

> For example, the word `時間`, meaning "time, hour", is composed of two kanji:
> `時` "time, hour" and `間` "interval, space". We already know the composition
> for `時`. The composition for `間` is `門` "gate" and `日` "day, sun".
>
> The progression to build this word is: `日`, `土`, `寸`, `寺`, `時`, `門`, `間`,
> and finally `時間`.

Sentences are composed of two or more words or other components (ex. particles
or punctuation).

> For example, the sentence `もう乗り込む時間だ。`, translated as "It's time to get
> aboard.", is composed of the following:
> 1. The word `もう` "now, soon"
> 2. The compound word `乗り込む` "to board"
>    - `乗る` and `込む` combine to form the word `乗り込む`.
> 3. The word `時間` "time, hour"
> 4. The copula `だ` "to be, is"
> 5. The Japanese period `。`
>
> The progression to build this sentence is: `もう`, `乗`, `乗る`, `辵`, `辵(⻍)`,
> `入`, `込`, `込む`, `乗り込む`, `日`, `土`, `寸`, `寺`, `時`, `門`, `間`, `時間`,
> `だ`, `。`, and finally `もう乗り込む時間だ。`.

### What is a "path"?

Progressions are used to build up an optimized *path* of components that should
be learned in order. A path will start with simple components and build up to
more complex components. Complex components will not appear until all of the
components in their progression (excluding themselves) have appeared. This order
will minimize the amount of new material introduced in each increment of the
learning process.

A path is more opinionated than a progression. It's usually structured in order
to achieve some goal or a set of goals. The default path provided by this
project tries to balance the following goals:

1. Learn the primary and secondary Jōyō kanji
2. Learn the Jinmeiyō kanji
3. Learn high priority words, according to JMdict
4. Learn any other kanji or words that appear frequently in Tatoeba sentences
5. Reinforce kanji and vocabulary with example sentences

The default path is split into several levels, each with its own set of
parameters for the goals above. The early levels of the path are more focused on
introducing kanji, while the later levels are more focused on building
vocabulary. See the [Stats] section for more of a breakdown.

This project also includes tools to build your own custom *path* in order to
meet your own interests and learning objectives.

> For example, if you like JPop or JRock, and you have some song lyrics and
> translations, you could use this project to build a path that would cover the
> kanji and words used in those lyrics with lines from the song used as example
> sentences.
>
> You can apply this approach to other forms of media, as well. For example, you
> could build a path for a TV show, movie, or other video by processing the
> subtitles and translations, if available. You could also build a path from one
> or more book files provided by Aozora Bunko or another free book provider.

See the `examples/` directory for more some examples.

## Installation

If you would just like to install the Anki decks for this project, see the
[Shared Deck Installation] section.

You can install this project with pip:
```sh
$ pip install progja
```

See the `examples/` directory for example usage.

### Shared Deck Installation

The Anki decks provided by this project are available via AnkiWeb:
1. [Progressive Japanese (Lv. 1)](https://ankiweb.net/shared/info/1475570445)
2. [Progressive Japanese (Lv. 2)](https://ankiweb.net/shared/info/1622728973)
3. [Progressive Japanese (Lv. 3)](https://ankiweb.net/shared/info/188104618)
4. Progressive Japanese (Lv. 4) (pending)
5. Progressive Japanese (Lv. 5) (pending)

## Caveats

This project is not perfect (yet). There are a few caveats you should be aware
of before using it for your own studies and in your own projects.

- The project is still under active development. It may contain bugs.
- The source for word data is JMdict, a dictionary database. It's a relatively
  exhaustive source for words and definitions. As a result, some words in this
  project have many, many definitions and variations.
    - Our advice is to focus on the first few definitions and treat the
      remaining as optional/extra information.
- The source for sentence data is Tatoeba. Sentences and translations are
  crowd-sourced and managed by volunteers. As a result, some sentences in this
  project may be a bit random or may have low quality translations.
- Sentences and words are split into subcomponents using a tokenizer. The way
  that the tokenizer splits some words and sentences can often result in strange
  or nonintuitive components (notably: grammatical components). You will likely
  encounter several of these.
    - Our advice is to just move past these as you study if they do not provide
      any value to you. Treat them as optional/extra information.
- Sentence readings  had to be hacked together and may be inaccurate. We are
  exploring additional options, like text-to-speech audio readings.

## Stats

> Note: These numbers may not correspond exactly to the number of
> cards in each Anki deck.

Completion schedule (kanji, words, sentences):

> The numbers below are cumulative for each path level. The numbers
> in parenthesis are cumulative for all path levels.

| Level | % | # | Kanji | Words | Sentences |
| ----- | - | - | ----- | ----- | --------- |
| 1 | 25% | 1,162 (1,162) | 524 (524) | 375 (375) | 263 (263) |
| 1 | 50% | 2,407 (2,407) | 903 (903) | 816 (816) | 688 (688) |
| 1 | 75% | 3,650 (3,650) | 1,224 (1,224) | 1,294 (1,294) | 1,132 (1,132) |
| 1 | 100% | 4,907 (4,907) | 1,493 (1,493) | 1,803 (1,803) | 1,611 (1,611) |
| 2 | 25% | 1,715 (6,622) | 443 (1,936) | 669 (2,472) | 603 (2,214) |
| 2 | 50% | 3,426 (8,333) | 835 (2,328) | 1,350 (3,153) | 1,241 (2,852) |
| 2 | 75% | 5,126 (10,033) | 1,057 (2,550) | 2,104 (3,907) | 1,965 (3,576) |
| 2 | 100% | 6,849 (11,756) | 1,062 (2,555) | 3,024 (4,827) | 2,763 (4,374) |
| 3 | 25% | 2,168 (13,924) | 496 (3,051) | 879 (5,706) | 793 (5,167) |
| 3 | 50% | 4,338 (16,094) | 853 (3,408) | 1,836 (6,663) | 1,649 (6,023) |
| 3 | 75% | 6,500 (18,256) | 881 (3,436) | 2,956 (7,783) | 2,663 (7,037) |
| 3 | 100% | 8,691 (20,447) | 895 (3,450) | 4,174 (9,001) | 3,622 (7,996) |
| 4 | 25% | 2,428 (22,875) | 42 (3,492) | 1,297 (10,298) | 1,089 (9,085) |
| 4 | 50% | 4,835 (25,282) | 73 (3,523) | 2,650 (11,651) | 2,112 (10,108) |
| 4 | 75% | 7,251 (27,698) | 109 (3,559) | 4,008 (13,009) | 3,134 (11,130) |
| 4 | 100% | 9,720 (30,167) | 120 (3,570) | 5,587 (14,588) | 4,013 (12,009) |
| 5 | 25% | 4,733 (34,900) | 10 (3,580) | 3,491 (18,079) | 1,232 (13,241) |
| 5 | 50% | 9,438 (39,605) | 44 (3,614) | 7,085 (21,673) | 2,309 (14,318) |
| 5 | 75% | 14,113 (44,280) | 116 (3,686) | 10,696 (25,284) | 3,301 (15,310) |
| 5 | 100% | 18,775 (48,942) | 223 (3,793) | 14,326 (28,914) | 4,226 (16,235) |

Completion schedule (kanji grade):

> Grade 1-6 and 8 are Jōyō kanji. Grade 9-10 are Jinmeiyō kanji.

| Level | % | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 9 | 10 |
| ----- | - | - | - | - | - | - | - | - | - | - |
| 1 | 25% | 100% | 78% | 34% | 24% | 24% | 17% | 5% | 3% | 0% |
| 1 | 50% | 100% | 100% | 89% | 48% | 45% | 34% | 10% | 6% | 0% |
| 1 | 75% | 100% | 100% | 100% | 98% | 60% | 51% | 17% | 9% | 1% |
| 1 | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 23% | 9% | 1% |
| 2 | 25% | 100% | 100% | 100% | 100% | 100% | 100% | 57% | 12% | 3% |
| 2 | 50% | 100% | 100% | 100% | 100% | 100% | 100% | 85% | 14% | 4% |
| 2 | 75% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 17% | 5% |
| 2 | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 17% | 5% |
| 3 | 25% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 85% | 8% |
| 3 | 50% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| 3 | 75% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| 3 | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

Completion schedule (JMdict nf frequency):

> The lower the nf, the higher a word's frequency.

| Level | % | 1-5 | 6-10 | 11-15 | 16-20 | 21-25 | 26-30 | 31+ |
| ----- | - | --- | ---- | ----- | ----- | ----- | ----- | --- |
| 1 | 25% | 8% | 1% | 0% | 0% | 0% | 0% | 0% |
| 1 | 50% | 18% | 2% | 1% | 1% | 1% | 1% | 0% |
| 1 | 75% | 29% | 4% | 2% | 2% | 1% | 1% | 1% |
| 1 | 100% | 45% | 5% | 2% | 2% | 2% | 1% | 1% |
| 2 | 25% | 58% | 5% | 4% | 3% | 3% | 2% | 1% |
| 2 | 50% | 72% | 6% | 5% | 4% | 3% | 3% | 2% |
| 2 | 75% | 76% | 18% | 8% | 5% | 4% | 4% | 3% |
| 2 | 100% | 76% | 50% | 9% | 6% | 5% | 4% | 3% |
| 3 | 25% | 77% | 56% | 22% | 6% | 5% | 4% | 4% |
| 3 | 50% | 78% | 56% | 42% | 7% | 6% | 5% | 5% |
| 3 | 75% | 79% | 57% | 43% | 31% | 6% | 6% | 6% |
| 3 | 100% | 79% | 58% | 44% | 34% | 27% | 22% | 7% |
| 4 | 25% | 79% | 58% | 44% | 35% | 28% | 23% | 16% |
| 4 | 50% | 100% | 63% | 45% | 37% | 31% | 24% | 18% |
| 4 | 75% | 100% | 91% | 45% | 38% | 32% | 25% | 19% |
| 4 | 100% | 100% | 100% | 89% | 39% | 33% | 26% | 20% |
| 5 | 25% | 100% | 100% | 100% | 100% | 98% | 26% | 20% |
| 5 | 50% | 100% | 100% | 100% | 100% | 100% | 100% | 40% |
| 5 | 75% | 100% | 100% | 100% | 100% | 100% | 100% | 83% |
| 5 | 100% | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

## License and Attribution

This project would not be possible without data provided by external projects.
Attribution for the projects providing this data is detailed below. Use of this
data in your own projects is subject to the terms and conditions outlined in the
licenses for each of these projects.

Everything else within this project that did not originate from an outside
source is licensed under the MIT License. Please see `LICENSE` for more
information.

### CHISE

> The CHISE (CHaracter Information Service Environment) project is an open
> source research and development project aiming at realizing a next-generation
> character processing environment that is not restricted by general-purpose
> coded character sets by directly using various knowledge of characters.
>
> Source: https://www.chise.org

The CHISE Ideographic Description Sequences (IDS) package provides descriptions
of the structure of CJK Ideographs. This package is used to populate the kanji
`IDS` field and to derive the compositions of all kanji in this project.
<br>
https://gitlab.chise.org/CHISE/ids
<br>
https://gitlab.chise.org/CHISE/ids/-/blob/master/README.en

The CHISE project is licensed under the GNU General Public License (GPL) v2.
<br>
https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html


### EDRDG

> The Electronic Dictionary Research and Development Group was set up at in 2000
> at Monash University in Australia by Jim Breen, who at that time was an
> Associate Professor in the Faculty of Information Technology. The main reason
> for establishing the Group was to have a vehicle which could hold the
> copyright for the various dictionary files Jim and others had compiled, and
> which could receive and spend funds in a tax-effective way for the improvement
> of the files and associated software.
>
> Source: https://www.edrdg.org/wiki/index.php/About_EDRDG

The EDRDG maintains KANJIDIC and JMdict, which are both used in this project.
KANJIDIC is used for most of the kanji data in this project. JMdict is used for
most of the word data in this project.
<br>
https://www.edrdg.org/wiki/index.php/KANJIDIC_Project
<br>
https://www.edrdg.org/wiki/index.php/JMdict-EDICT_Dictionary_Project

KANJIDIC and JMdict are licensed under a Creative Commons Attribution-ShareAlike
Licence (V3.0).
<br>
https://www.edrdg.org/edrdg/licence.html
<br>
https://creativecommons.org/licenses/by-sa/3.0/

### Tatoeba

> Tatoeba is a large database of sentences and translations. Its content is
> ever-growing and results from the voluntary contributions of thousands of
> members.
>
> Tatoeba provides a tool for you to see examples of how words are used in the
> context of a sentence. You specify words that interest you, and it returns
> sentences containing these words with their translations in the desired
> languages. The name Tatoeba (for example in Japanese) captures this concept.
>
> The project was founded by Trang Ho in 2006, hosted on Sourceforge under the
> codename of multilangdict.
>
> Source: https://tatoeba.org/eng/about

Tatoeba is used for most of the sentence data in this project. Only a subset of
the sentences/translation pairs provided by Tatoeba is used in this project.

Tatoeba is licensed under the Creative Commons Attribution 2.0 France License
(CC BY 2.0 FR).
<br>
https://creativecommons.org/licenses/by/2.0/fr/deed.en

## Contributing

If you are interested in contributing to this project, please see
[CONTRIBUTING.md] for more information.


<!-- links -->
[Attribution]: #attribution
[CONTRIBUTING.md]: CONTRIBUTING.md
[Tae Kim's Guide]: https://guidetojapanese.org/learn/complete/
[Duolingo]: https://www.duolingo.com/
[Tatoeba]: https://tatoeba.org
[progressions]: #what-is-a-progression
[path]: #what-is-a-path
[Stats]: #stats
[Shared Deck Installation]: #shared-deck-installation
