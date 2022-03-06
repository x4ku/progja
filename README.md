# Progressive Japanese

Data and tools for those studying the Japanese language.

## Contents

- [Overview](#overview)
- [Installation](#installation)
- [Stats](#stats)
- [Contributing](#contributing)
- [License](#license)

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

1. Learn the primary and secondary [Jōyō kanji]
2. Learn the [Jinmeiyō kanji]
3. Learn high priority words, according to [JMdict]
4. Learn any other kanji or words that appear frequently in [Tatoeba] sentences
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
[Installing Anki Decks] section. If you need to upgrade to the latest version,
see the [Upgrading Anki Decks] section.

You can install this project with pip:
```sh
$ pip install progja
```

See the `examples/` directory for example usage.

### Installing Anki Decks

It is recommended that you backup your Anki profile before proceeding.

The Anki decks provided by this project are available via AnkiWeb:
1. [Progressive Japanese (Lv. 1)](https://ankiweb.net/shared/info/1475570445)
2. [Progressive Japanese (Lv. 2)](https://ankiweb.net/shared/info/1622728973)
3. [Progressive Japanese (Lv. 3)](https://ankiweb.net/shared/info/188104618)
4. Progressive Japanese (Lv. 4) (pending)
5. Progressive Japanese (Lv. 5) (pending)

### Upgrading Anki Decks

It is recommended that you backup your Anki profile before proceeding.

Updating a deck should be as easy as downloading the new `.apkg` file and
opening it with Anki.

Some of the cards in the deck may get removed in newer versions. You will
probably want to find these cards and either delete them or suspend them. There
is a simple way to locate these cards: the `progja::version::<version>` tag.

All cards are tagged with a `progja::version::<version>` tag. When you update to
a new version, this tag will be updated with the new version number. If a card
was removed in the new version, then its tag will not be updated, making it easy
to locate. Simply search for any cards in the deck that are not tagged with the
new version number.

> For example, if you upgrade from version 1.2.3 to version 1.2.4, cards still
> tagged with `progja::version::1.2.3` (or some other version) are no longer
> included in version 1.2.4 of the project. You can use the search term
> `-tag:progja::version::1.2.4` to find all cards not tagged with the new
> version number.

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

See: [`docs/stats.md`].

## Contributing

See: [`CONTRIBUTING.md`].

## License

See: [`LICENSE`].


<!-- links -->

[`CONTRIBUTING.md`]: CONTRIBUTING.md
[`LICENSE`]: LICENSE
[`docs/stats.md`]: docs/stats.md

[Installing Anki Decks]: #installing-anki-decks
[path]: #what-is-a-path
[progressions]: #what-is-a-progression
[Stats]: #stats
[Upgrading Anki Decks]: #upgrading-anki-decks

[Duolingo]: https://www.duolingo.com/
[Jinmeiyō kanji]: https://en.wikipedia.org/wiki/Jinmeiy%C5%8D_kanji
[JMdict]: https://www.edrdg.org/jmdict/j_jmdict.html
[Jōyō kanji]: https://en.wikipedia.org/wiki/J%C5%8Dy%C5%8D_kanji
[Tae Kim's Guide]: https://guidetojapanese.org/learn/complete/
[Tatoeba]: https://tatoeba.org
