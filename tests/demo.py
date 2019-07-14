# -*- coding: utf-8 -*-

from prompt_toolkit import prompt, print_formatted_text, HTML, PromptSession
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style


def formatted_texts():
    print_formatted_text('Hello world')
    print_formatted_text(HTML('<b>This is bold</b>'))
    print_formatted_text(HTML('<i>This is italic</i>'))
    print_formatted_text(HTML('<u>This is underlined</u>'))

    # Colors from the ANSI palette.
    print_formatted_text(HTML('<ansired>This is red</ansired>'))
    print_formatted_text(HTML('<ansigreen>This is green</ansigreen>'))

    # Named colors (256 color palette, or true color, depending on the output).
    print_formatted_text(HTML('<skyblue>This is sky blue</skyblue>'))
    print_formatted_text(HTML('<seagreen>This is sea green</seagreen>'))
    print_formatted_text(HTML('<violet>This is violet</violet>'))

    print_formatted_text(HTML('<aaa fg="ansiwhite" bg="ansigreen">White on green</aaa>'))

    style = Style.from_dict({
        'aaa': '#ff0066',
        'bbb': '#44ff00 italic',
    })

    print_formatted_text(HTML('<aaa>Hello</aaa> <bbb>world</bbb>!'), style=style)

    text = FormattedText([
        ('#ff0066', 'Hello'),
        ('', ' '),
        ('#44ff00 italic', 'World'),
    ])

    print_formatted_text(text)


def prompts():
    # Create prompt object.
    session = PromptSession()
# Do multiple input calls.
    from pygments.lexers.html import HtmlLexer
    from pygments.styles import get_style_by_name
    from prompt_toolkit.shortcuts import prompt
    from prompt_toolkit.lexers import PygmentsLexer
    from prompt_toolkit.styles.pygments import style_from_pygments_cls

    style = style_from_pygments_cls(get_style_by_name('monokai'))
    text = prompt('Enter HTML: ', lexer=PygmentsLexer(HtmlLexer), style=style,
                include_default_pygments_style=False)
    print('You said: %s' % text)

    from prompt_toolkit.completion import WordCompleter

    html_completer = WordCompleter(['<html>', '<body>', '<head>', '<title>'])
    text = prompt('Enter HTML: ', completer=html_completer)
    print('You said: %s' % text)

    class MyCustomCompleter(Completer):
        def get_completions(self, document, complete_event):
            yield Completion('completion', start_position=0)

    text = prompt('> ', completer=MyCustomCompleter())

    from prompt_toolkit import prompt
    from prompt_toolkit.styles import Style

    example_style = Style.from_dict({
        'rprompt': 'bg:#ff0066 #ffffff',
    })

    def get_rprompt():
        return '<rprompt>'

    answer = prompt('> ', rprompt=get_rprompt, style=example_style)



if __name__ == '__main__':
    from prompt_toolkit import Application

    app = Application(full_screen=True)
    app.run()
    # prompts()
