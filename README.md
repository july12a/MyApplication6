# GitHub에 쓰기 시작

# Writing oni GitHub

## 기본 쓰기 및 서식 지정 구문

## Basic writing and formatting syntax

### 간단한 구문을 사용하여 GitHub에서 산문 및 코드에 대한 정교한 서식을 만듭니다

### Create sophisticated formatting for your prose and code on GitHub with simple sytax

```
누가 이 기능을 사용할 수 있나요?
Markdown은 GitHub 웹 인터페이스에서 사용할 수 있습니다.
Who can use this feature?
Markdown can be used in the GitHub web interface.
```

### 제목

### Headings

제목을 만들려면 제목 텍스트 앞에 1~6개의 `#`기호를 추가합니다. 사용하는 `#`의 수에 따라 제목의 계층 구조 수준과 글꼴 크기가 결정 됩니다.
To create a heading, add one to six `#` symbols before your heading text. The number of `#` you use will determine the hierarchy level and typeface size of the heading.

```
# A first-level heading
## A second-level heading
### A third-level heading
```

# A first-level heading

## A second-level heading

### A third-level heading

When you use two or more headings, GitHub automatically generates a table of contents that you can access by clicking : : within the file header. Each heading title is listed in the table of contents and you can click a title to navigate to the selected section.
![image](https://docs.github.com/assets/cb-69181/mw-1440/images/help/repository/headings-toc.webp)

### Sytle text

You can indicate emphasis with bold, italic, strikethrough, subscript, or superscript text in comment fields and `.md` files.

|**Style**|Syntax|Keyboard shortcut|Example|Output|
|-|-|-|-|-|
|Bold|`** **` or `__ __`|`Command`+`B`(Mac) or`Ctrl`+`B`(Windows/Linux)|`**This is bold text**`|**This is bold text**|
|Italic|`* *` or `_ _`|`Command`+`I`(Mac) or`Ctrl`+`I`(Windows/Linux)|`_This is italicized_`|_This is italicized_|
|Strikethrough| `~~ ~~` or `~ ~` |None| `~~This was mistaken text~~` |~~This was mistaken text~~|
|Bold and nested italic| `** **` and `_ _`| None| `**This text is _extremely_ important**` |**This text is _extremely_ important**|
|All bold and italic |`*** ***` |None| `***All this text is important***` |_**All this text is important**_|
|Subscript |`<sub> </sub>` |None| ```This is a <sub>subscript</sub> text``` |This is a <sub>subscript</sub> text|
|Superscript |`<sup> </sup>` |None| `This is a <sup>superscript</sup> text`| This is a <sup>superscript</sup> text|
|Underline |`<ins> </ins>` |None| `This is an <ins>underlined</ins> text` |This is an <ins>underlined</ins> text|

### Quoting text

You can quote text with a `>`.

```
Text that is not a quote
> Text that is a quote
```

Quoted text is indented with a vertical line on the left and displayed using gray type.

![](https://docs.github.com/assets/cb-13462/mw-1440/images/help/writing/quoted-text-rendered.webp)
> [!NOTE]  
> When viewing a conversation, you can automatically quote text in a comment by highlighting the text, then typing `R`. You can quote an entire comment by clicking..., then **Quote** replay. For more information about keyboard shortcuts, see [Keyboard shortcuts](https://docs.github.com/en/get-started/accessibility/keyboard-shortcuts).

### Quoting code

You can call out code or a command within a sentence with single backticks. The text within the backticks wills not be formatted. You can also press the `Command`+`E`(Mac) or `Ctrl`+`E`(Windows/Linux) keyboard shortcut to insert the backticks for a code block within a line of Markdown.

```Use `git status` to list all new or modified files that haven't yet been committed.```
![](https://docs.github.com/assets/cb-24556/mw-1440/images/help/writing/inline-code-rendered.webp)

To format code or text into its own disttinct block, use triple backticks.

Some basic Git commands are:

```
git status
git add
git commit
```

![](https://docs.github.com/assets/cb-34231/mw-1440/images/help/writing/code-block-rendered.webp)
For more information, see [Creating and highlighting code blocks](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-and-highlighting-code-blocks).

If you are frequently editing code snippets and tables, you may benefit from enabling a fixed-width font in all comment fields on GitHub. For more information, see [About writing and formatting on GitHub](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/about-writing-and-formatting-on-github#enabling-fixed-width-fonts-in-the-editor).

### Supported color models
In issue, pull requests, and discussions, you can call out colors within a sentence by using backticks. A supported color model within backticks will display a visualization of the color.
```
The background color is `#ffffff` for light mode and `#000000` for dark mode.
```
![](https://docs.github.com/assets/cb-11643/mw-1440/images/help/writing/supported-color-models-rendered.webp)
Here are the currently supported color models.
|**Color**|**Syntax**|**Example**|**Output**|
|-|-|-|-|
|HEX|`#RRGGBB`|`#0969DA`|![](https://docs.github.com/assets/cb-1558/mw-1440/images/help/writing/supported-color-models-hex-rendered.webp)|
|RGB|`rgb(R,G,B)`|`rgb(9,105,218)`|![](https://docs.github.com/assets/cb-1962/mw-1440/images/help/writing/supported-color-models-rgb-rendered.webp)|
|HSL|`hsl(H,S,L)`|`hsl(212,92%,45%)`|![](https://docs.github.com/assets/cb-2066/mw-1440/images/help/writing/supported-color-models-hsl-rendered.webp)|
> [!NOTE]
> * A supported color model cannot have any leading or traing spaces within the backticks.
> * The visualization of the color is only supported in issues, pull requests, and discussions.

### Links
You can create an inline link by wrapping link in brackets `[ ]`, and then wrapping the URL in parentheses `( )`. You can also use the keyboard shortcut `Command`+`K` to create a link. When you have text selected, you can paste a URL from your clipboard to automatically create a link from the selection.
You can also create a Markdown hyperlink by highlighting the text and using the keyboard shortcut `Command`+`v`. If you'd like to replace the text with the link, use the keyboard shortcut `Command`+`Shift`+`v`.
```
This site was build using [GitHub Pages](https://pages.github.com/).
```
This site was build using [GitHub Pages](https://pages.github.com/).
> [!NOTE]
> Github automatically creates links when valid URLs are written in a comment. For more information, see [Autolinked referenxes and URLs](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls).
### Section links 
You can link directly to any section that has a heading. To view the automatically generated anchor in a rendered file, hover over the section heading to expose the 🔗 icon and click the icon to display the anchor in your browser.
![](https://docs.github.com/assets/cb-55933/mw-1440/images/help/repository/readme-links.webp)
If you need to determine the anchor for a heading in a file you are editing, you can use following basic rules:
* Letters are converted to lower-case.
* Spaces are replaced by hyphens(`-`). Any order whitespace or punctuation characters are removed.
* Leading and trailing whitespace are removed.
* Markup formatting is removed, leaving only the contents (for example, `_italics_` becomes `italics`).
* If the automatically generated anchor for a heading is identical to an earlier anchor in the same document, a unique identifier is generated by appending a hyphen and an auto-incrementing integer.

For more detailed information on the requirements of URI fragments, see [RFC 3986: Uniform Resource Identifier (URI): Generic Syntax, Section 3.5](https://www.rfc-editor.org/rfc/rfc3986#section-3.5).
The code block below demonstrates the basic rules used to generate anchors from headings in rendered content.

# Example headings

## Sample Section

## This'll be a _Helpful_ Section About the Greek Letter 0!
A heading containing characters not allowed in fragments, UTF-8 characters, two consecutive spaces between the first and second words, and formatting.

## This heading is not unique in the file

TEXT 1

## This heading is not unique in the file

TEXT 2

# Links to the example headings above

Link to the sample section: [Link Text](#sample-section).

Link to the helpful section: [Link Text](#thisll-be-a-helpful-section-about-the-greek-letter-0).

Link to the first non-unique section: [Link Text](#this-heading-is-not-unique-in-the-file).

Link to the second non-unique section: [Link Text](#this-heading-is-not-unique-in-the-file-1).

> [!NOTE] 
> 
> If you edit a heading, or if you change the order of headings with "identical" anchors, you will also need to update any links to those headings as the anchors will change,

### Relative links
