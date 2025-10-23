# GitHub Flavored Markdown Spec

*This formal specification is based on the [CommonMark Spec](http://spec.commonmark.org/) by [John MacFarlane](http://github.com/jgm) and licensed under ![bysa](https://i.creativecommons.org/l/by-sa/4.0/80x15.png)*

1. [Introduction](#1-introduction)  
    1. [What is GitHub Flavored Markdown?](#11-what-is-github-flavored-markdown)  
    2. [What is Markdown?](#12-what-is-markdown)

## 1 Introduction

### 1.1 What is GitHub Flavored Markdown?

GitHub Flavored Markdown, often shortend as GFM, is the dialect of Markdown that is currently supported for user content on GitHub.com and GitHub Enterprise.

This formal specification, based on the CommonMark Spec, defines the syntax and semantics of this dialect.

GFM is a strict superset of CommonMark. All the features which are supported in GitHub user content and that are not specified on the original CommonMark Spec are hence known as **extensions**, and highlighted as such.

While GFM supports a wide range of inputs, it's worth noting that GitHub.com and GitHub Enterprise perform additional post-processing and sanitization after GFM is converted to HTML to ensure security and consistency of the website.

### 1.2 What is Markdown?
Markdown is a plain text format for writing structured documents, base on conventions for indicating formatting in email and usenet posts. It was developed by John Gruber (with help from Araon Swartz) and released in 2004 in the form of a [syntax description](http://daringfireball.net/projects/markdown/syntax) and a Perl script (`Markdown.pl`) for converting Markdown to HTML. In the next decade, dozens of implementations were developed in many languages. Some extended the original Markdown syntax with conventions for footnotes, tables, and other document elements. Some allowed Markdown documents to be rendered in formats other than HTML. Websites like Reddit, StackOverflow, and GitHub had millions of people using Markdown. And Markdown started to be used beyond the web, to author books, article, slide shows, letters, and lecture notes.

What distinguishes Markdown from many other lightweight markdown syntaxes, which are often easier to write, is its readability. As Gruber writes:

    The Overriding design goal for Markdown's formatting syntax is to make it as readable as\
     possible. The idea is that a Markdown-formatted document should be publishable as-is, as plain\
      text, without looking like it's been marked up with tags or formatting instructions.\
      (http://daringfireball.net/projects/markdown/)

The point can be illustrated by comparing a sample of [AsciiDoc](http://www.methods.co.nz/asciidoc/) with an equivalent sample of Markdown.

``` bash
1. List item one.
+
List item one continued with a second paragraph followed by an Indented block.
+
..........
$ ls *.sh
$ mv *.sh ~/tmp
..........
+
List item continued with a third paragraph.

2. List item continued with an open block.
+
--
This paragraph is part of the preceding list item.

a. This list is nested and does not required explicit item continuation.
+
This paragraph is part of the preceding list item.

b. List item b.

This paragraph belongs to item two of the outer list.
--
```

And here is the equivalent in Markdown:

``` bash
1. List item one.
    List item one continued with a second paragraph followed by an Indented block.
        $ ls *.sh
        $ mv *.sh ~/tmp
    List item continued with a third paragraph.
2. List item two continued with an open block.
    This paragraph is part of the preceding list item.
    1. This list is nested and does not require explicit item continuation.
       This paragraph is part of the preceding list item.
    2. List item b.
    This paragraph belongs to item two of the outer list.
```

The AsciiDoc version is, arguably, easier to write. You don't need to worry about indentation. But the Markdown version is much easier to read. The nesting of list items is apparent to the eye in the secure, not just in the proceeded document.

### 1.3 Why is a spec needed?
John Gruber's [canonical description of Markdown's syntax]() does not specify the syntax unambiguonuosly. Here are some examples of questions it does not answer:

1. How much indentation is needed for a sublist? The spec says that continuation paragraphs need to be indented four spaces, but is not fully explicit about sublists. It is natural to think they, too, must be indented four spaces, but `Markdown.pl` does not required that. This is hardly a "corner case," and divergences between implementations on this issue often lead to surprises for users in real documents. (See [this comment by John Gruber]().)
2. Is a blank line needed before a block quote or heading? Most implementations do not require the blank line. However, this can read to unexpected results in hard-wrapped text, and also to ambiguities in parsing (note that some implementations put the heading inside the blockquote, while other do not). (John Gruber has also spoken [in favor of requiring the blank lines]().)
3. Is a blank line needed before an indented code block? (`Markdown.pl` requires it,)