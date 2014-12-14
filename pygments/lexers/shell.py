# -*- coding: utf-8 -*-
"""
    pygments.lexers.shell
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for various shells.

    :copyright: Copyright 2006-2014 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import Lexer, RegexLexer, do_insertions, bygroups, \
     include, default, this, using
from pygments.token import Punctuation, \
     Text, Comment, Operator, Keyword, Name, String, Number, Generic
from pygments.util import shebang_matches


__all__ = ['BashLexer', 'BashSessionLexer', 'TcshLexer', 'BatchLexer',
           'PowerShellLexer', 'ShellSessionLexer']

line_re  = re.compile('.*?\n')


class BashLexer(RegexLexer):
    """
    Lexer for (ba|k|)sh shell scripts.

    .. versionadded:: 0.6
    """

    name = 'Bash'
    aliases = ['bash', 'sh', 'ksh']
    filenames = ['*.sh', '*.ksh', '*.bash', '*.ebuild', '*.eclass',
                 '.bashrc', 'bashrc', '.bash_*', 'bash_*', 'PKGBUILD']
    mimetypes = ['application/x-sh', 'application/x-shellscript']

    tokens = {
        'root': [
            include('basic'),
            (r'\$\(\(', Keyword, 'math'),
            (r'\$\(', Keyword, 'paren'),
            (r'\${#?', Keyword, 'curly'),
            (r'`', String.Backtick, 'backticks'),
            include('data'),
        ],
        'basic': [
            (r'\b(if|fi|else|while|do|done|for|then|return|function|case|'
             r'select|continue|until|esac|elif)(\s*)\b',
             bygroups(Keyword, Text)),
            (r'\b(alias|bg|bind|break|builtin|caller|cd|command|compgen|'
             r'complete|declare|dirs|disown|echo|enable|eval|exec|exit|'
             r'export|false|fc|fg|getopts|hash|help|history|jobs|kill|let|'
             r'local|logout|popd|printf|pushd|pwd|read|readonly|set|shift|'
             r'shopt|source|suspend|test|time|times|trap|true|type|typeset|'
             r'ulimit|umask|unalias|unset|wait)\s*\b(?!\.)',
             Name.Builtin),
            (r'#.*\n', Comment),
            (r'\\[\w\W]', String.Escape),
            (r'(\b\w+)(\s*)(=)', bygroups(Name.Variable, Text, Operator)),
            (r'[\[\]{}()=]', Operator),
            (r'<<<', Operator),  # here-string
            (r'<<-?\s*(\'?)\\?(\w+)[\w\W]+?\2', String),
            (r'&&|\|\|', Operator),
        ],
        'data': [
            (r'(?s)\$?"(\\\\|\\[0-7]+|\\.|[^"\\])*"', String.Double),
            (r"(?s)\$?'(\\\\|\\[0-7]+|\\.|[^'\\])*'", String.Single),
            (r';', Punctuation),
            (r'&', Punctuation),
            (r'\|', Punctuation),
            (r'\s+', Text),
            (r'\d+(?= |\Z)', Number),
            (r'[^=\s\[\]{}()$"\'`\\<&|;]+', Text),
            (r'\$#?(\w+|.)', Name.Variable),
            (r'<', Text),
        ],
        'curly': [
            (r'}', Keyword, '#pop'),
            (r':-', Keyword),
            (r'\w+', Name.Variable),
            (r'[^}:"\'`$]+', Punctuation),
            (r':', Punctuation),
            include('root'),
        ],
        'paren': [
            (r'\)', Keyword, '#pop'),
            include('root'),
        ],
        'math': [
            (r'\)\)', Keyword, '#pop'),
            (r'[-+*/%^|&]|\*\*|\|\|', Operator),
            (r'\d+#\d+', Number),
            (r'\d+#(?! )', Number),
            (r'\d+', Number),
            include('root'),
        ],
        'backticks': [
            (r'`', String.Backtick, '#pop'),
            include('root'),
        ],
    }

    def analyse_text(text):
        if shebang_matches(text, r'(ba|z|)sh'):
            return 1
        if text.startswith('$ '):
            return 0.2


class BashSessionLexer(Lexer):
    """
    Lexer for simplistic shell sessions.

    .. versionadded:: 1.1
    """

    name = 'Bash Session'
    aliases = ['console']
    filenames = ['*.sh-session']
    mimetypes = ['application/x-shell-session']

    def get_tokens_unprocessed(self, text):
        bashlexer = BashLexer(**self.options)

        pos = 0
        curcode = ''
        insertions = []

        for match in line_re.finditer(text):
            line = match.group()
            m = re.match(r'^((?:\(\S+\))?(?:|sh\S*?|\w+\S+[@:]\S+(?:\s+\S+)'
                          r'?|\[\S+[@:][^\n]+\].+)[$#%])(.*\n?)' , line)
            if m:
                # To support output lexers (say diff output), the output
                # needs to be broken by prompts whenever the output lexer
                # changes.
                if not insertions:
                    pos = match.start()

                insertions.append((len(curcode),
                                   [(0, Generic.Prompt, m.group(1))]))
                curcode += m.group(2)
            elif line.startswith('>'):
                insertions.append((len(curcode),
                                   [(0, Generic.Prompt, line[:1])]))
                curcode += line[1:]
            else:
                if insertions:
                    toks = bashlexer.get_tokens_unprocessed(curcode)
                    for i, t, v in do_insertions(insertions, toks):
                        yield pos+i, t, v
                yield match.start(), Generic.Output, line
                insertions = []
                curcode = ''
        if insertions:
            for i, t, v in do_insertions(insertions,
                                         bashlexer.get_tokens_unprocessed(curcode)):
                yield pos+i, t, v


class ShellSessionLexer(Lexer):
    """
    Lexer for shell sessions that works with different command prompts

    .. versionadded:: 1.6
    """

    name = 'Shell Session'
    aliases = ['shell-session']
    filenames = ['*.shell-session']
    mimetypes = ['application/x-sh-session']

    def get_tokens_unprocessed(self, text):
        bashlexer = BashLexer(**self.options)

        pos = 0
        curcode = ''
        insertions = []

        for match in line_re.finditer(text):
            line = match.group()
            m = re.match(r'^((?:\[?\S+@[^$#%]+\]?\s*)[$#%])(.*\n?)', line)
            if m:
                # To support output lexers (say diff output), the output
                # needs to be broken by prompts whenever the output lexer
                # changes.
                if not insertions:
                    pos = match.start()

                insertions.append((len(curcode),
                                   [(0, Generic.Prompt, m.group(1))]))
                curcode += m.group(2)
            else:
                if insertions:
                    toks = bashlexer.get_tokens_unprocessed(curcode)
                    for i, t, v in do_insertions(insertions, toks):
                        yield pos+i, t, v
                yield match.start(), Generic.Output, line
                insertions = []
                curcode = ''
        if insertions:
            for i, t, v in do_insertions(insertions,
                                         bashlexer.get_tokens_unprocessed(curcode)):
                yield pos+i, t, v


class BatchLexer(RegexLexer):
    """
    Lexer for the DOS/Windows Batch file format.

    .. versionadded:: 0.7
    """
    name = 'Batchfile'
    aliases = ['bat', 'batch', 'dosbatch', 'winbatch']
    filenames = ['*.bat', '*.cmd']
    mimetypes = ['application/x-dos-batch']

    flags = re.MULTILINE | re.IGNORECASE

    _nl = r'\n\x1a'
    _punct = r'&<>|'
    _ws = r'\t\v\f\r ,;=\xa0'
    _space = r'(?:(?:\^[%s])*(?:\^?[%s])+(?:\^?[%s]|\^[%s])*)' % (_nl, _ws,
                                                                  _ws, _nl)
    _rest_of_line = r'(?:(?:[^%s^]|\^[\w\W])*)' % _nl
    _keyword_terminator = (r'(?=(?:(?:\^[%s])*)(?:[%s]|\^?[%s%s(+./:[\\\]]))' %
                           (_nl, _nl, _punct, _ws))
    _token_terminator = r'(?=\^?[%s]|[%s%s])' % (_ws, _punct, _nl)
    _token = r'(?:[%s]+|(?:\^?[^%s%s%s^]|\^[%s%s])+)' % (_punct, _nl, _punct,
                                                        _ws, _nl, _ws)
    _label = r'(?:(?:\^?[^%s%s+:^])*)' % (_nl, _ws)

    # TODO:
    # goto and set in compounds
    # if %var%
    # if not "%cd:0,3%"
    # set /a iterations+=(%%M%%M^)

    # TODO:
    # KanjiScan
    # `echo foo)` vs `(echo foo)`
    # `^^!`
    # newline-terminated string
    # rem and goto and : (others?) only parse one arg (relevant for ^<LF>)
    # ... but only if the first token is `rem` i.e. `rem.x x x x x^` continues
    # onto the next line properly. `goto` parses all. `:` parses 1 or 0.
    # `rem x^ x`: `x^ x` is one token, at least for my purposes
    # `rem /? x^`
    # `rem >^`
    # re.DOTALL?
    # Use _nl instead of \n (except after ^@). Use [^_nl] instead of ..
    # BOM? Unicode?
    # labels: http://www.dostips.com/forum/viewtopic.php?f=3&t=3803
    # `>nul rem a b^`
    # check ^ before everything everywhere
    # `%%`
    # account for \x00 when detecting next token
    # lex escaped _space as String.Escape not Text
    # allow variables (which can include ws) in _token
    # Number in `if 1 gtr 1` and Name.Variable in `if [%x%]==[]`
    # `^\n` between chars and escaped chars in keywords
    # ^H deletes previous character
    tokens = {
        'root': [
            include('*'),
            (r'\)%s%s' % (_token_terminator, _rest_of_line), Comment.Single),
            default('pump-statement')
        ],
        'begin-statement': [
            include('*'),
            (r'(?=[%s])' % _nl, Text, '#pop:2'),
            (r'\(', Punctuation, 'pump-statement/compound'),
            (r'@+', Punctuation),
            (r'((?:for|if|rem)(?:%s(?=%s%s?\^?/\^?\?)|(?=\^?/\^?\?)))' %
             (_token_terminator, _space, _token), Keyword, '#pop:2'),
            (r'(assoc|break|cd|chdir|cls|color|copy|del|dir|date|echo|'
             r'endlocal|erase|exit|ftype|md|mkdir|move|path|pause|popd|prompt|'
             r'pushd|rd|ren|rename|rmdir|setlocal|shift|start|time|title|type|'
             r'ver|verify|vol)%s' % _keyword_terminator, Keyword, '#pop:2'),
            (r'call%s' % _keyword_terminator, Keyword, 'call'),
            (r'(for%s)(%s?)(/f%s)' %
             (_token_terminator, _space, _token_terminator),
             bygroups(Keyword, Text, Keyword), ('for/f', 'for')),
            (r'(for%s)(%s?)(/l%s)' %
             (_token_terminator, _space, _token_terminator),
             bygroups(Keyword, Text, Keyword), ('for/l', 'for')),
            (r'for%s' % _token_terminator, Keyword, ('for2', 'for')),
            (r'(goto%s)(%s?)(:?)(%s?)(%s)' %
             (_keyword_terminator, _space, _label, _rest_of_line),
             bygroups(Keyword, Text, Punctuation, Name.Label, Comment.Single),
             '#pop:2'),
            (r'(if%s)(%s?)((?:/i%s)?)(%s?)((?:not%s)?)(%s?)' %
             (_token_terminator, _space, _token_terminator, _space,
              _token_terminator, _space),
             bygroups(Keyword, Text, Keyword, Text, Keyword, Text),
             ('(?', 'if')),
            (r'rem(%s%s%s.*|%s%s)' % (_token_terminator, _space, _token,
                                      _keyword_terminator, _rest_of_line),
             Comment.Single, '#pop:2'),
            (r'(set%s)(%s?)(/a)' % (_keyword_terminator, _space),
             bygroups(Keyword, Text, Keyword), '#pop'),
            (r'(set%s)(%s?)((?:/p)?)(%s?)((?:(?!\^?[%s]?["%s])'
             r'(?:\^?[^%s%s^=]|\^[%s]?[\w\W])+)?)(=?)' %
             (_keyword_terminator, _space, _space, _nl, _ws, _nl, _punct, _nl),
             bygroups(Keyword, Text, Keyword, Text, Name.Variable,
                      Punctuation), '#pop:2'),
            default('#pop:2')
        ],
        'arithmetic': [
            (r'0[0-7]+', Number.Oct),
            (r'0x[0-9a-f]+', Number.Hex),
            (r'\d+', Number.Integer),
            (r'[(),]+', Punctuation),
            (r'([=+\-*/!~]|%%|\^\^)+', Operator),
            (r'(?![%s"^%%])%s' % (_punct, _token), Name.Variable),
            # TODO: `set/a >o.txt x=4`
            (r'(?=[\x00|&])', Text, '#pop'),
            include('follow-statement')
        ],
        'follow-statement': [
            include('*'),
            (r'(?=[%s])' % _nl, Text, '#pop'),
            (r'\x00.*\n?', Comment.Single, '#pop'),
            (r'"[^%s"]*"?' % _nl, String.Double),
            (r'%%%%|\^[%s]?[\w\W]' % _nl, String.Escape),
            # TODO: variables in FOR
            # TODO: %x~1,-1%
            # TODO: variables inside strings
            # TODO: test variable %foo:~-,% (which is legal)
            (r'%%(\*|(~[a-z]*($[^:]+:)?)?\d|[^%%:%s]+(:(~(-?\d+)?(,-?\d+)?|'
             r'\*?([^^]|\^[^%%])+=([^^]|\^[^%%])*))?%%)' % _nl, Name.Variable),
            (r'\|\|?|&&?', Punctuation, '#pop'),
            (r'.', Text) # TODO: more characters at a time
        ],
        'pump-statement': [
            (r'[%s]+' % _nl, Text, '#pop'),
            default(('follow-statement', 'arithmetic', 'begin-statement'))
        ],
        'begin-statement/compound': [
            include('*'),
            (r'(?=\))', Text, '#pop:2'), # TODO: pop directly to the pump
            include('begin-statement')
        ],
        'arithmetic/compound': [
            (r'(?=\))', Text, '#pop'),
            include('arithmetic')
        ],
        'follow-statement/compound': [
            include('*'),
            (r'(?=\))', Text, '#pop'),
            include('follow-statement')
        ],
        'pump-statement/compound': [
            (r'[%s]+' % _nl, Text),
            (r'\)', Punctuation, '#pop'),
            default(('follow-statement/compound', 'arithmetic/compound',
                     'begin-statement/compound'))
        ],
        '*': [
            (r'(^[^:]?[%s]*)(:)([%s]*)(%s)(.*)' % (_ws, _ws, _label),
             bygroups(Text, Punctuation, Text, Name.Label, Comment.Single)),
            (_space, Text),
            (r'((?:%s.\d)?)(>>?&|<&)([%s%s]*)(\d)' %
             (_token_terminator, _ws, _nl),
             bygroups(Number.Integer, Punctuation, Text, Number.Integer)),
            (r'((?:%s.\d)?)(>>?|<)(%s?%s)' %
             (_token_terminator, _space, _token),
             bygroups(Number.Integer, Punctuation, Text))
        ],
        'call': [
            (_space, Text),
            (r'(::?)(%s)' % _label, bygroups(Punctuation, Name.Label),
             '#pop:2'),
            default('#pop')
        ],
        'for': [
            (r'(%s)(in)(%s)(\()' % (_space, _space),
             bygroups(Text, Keyword, Text, Punctuation), '#pop'),
            include('follow-statement')
        ],
        'for2': [
            (r'\)', Punctuation),
            (r'(%s)(do%s)' % (_space, _token_terminator),
             bygroups(Text, Keyword), '#pop'),
            include('follow-statement')
        ],
        'for/f': [
            (r'"[^"]*"', String.Double),
            (r'`[^`]*`', String.Backtick),
            include('for2')
        ],
        'for/l': [
            (r'-?\d+', Number.Integer),
            (r',', Punctuation),
            include('for2')
        ],
        'if': [
            (r'((?:cmdextversion|errorlevel)%s)(%s)(\d+)' %
             (_token_terminator, _space),
             bygroups(Keyword, Text, Number.Integer), '#pop'),
            (r'(defined%s)(%s)(%s)' % (_token_terminator, _space, _token),
             bygroups(Keyword, Text, Name.Variable), '#pop'),
            (r'(exist%s)(%s%s)' % (_token_terminator, _space, _token),
             bygroups(Keyword, Text), '#pop'),
            (r'(%s%s?)(==)(%s?%s)' % (_token, _space, _space, _token),
             bygroups(Text, Operator, Text), '#pop'),
            (r'(%s)(%s)(equ|geq|gtr|leq|lss|neq)(%s)(%s)' %
             (_token, _space, _space, _token),
             bygroups(using(this, state='arithmetic/if'), Text, Operator.Word,
                      Text, using(this, state='arithmetic/if')), '#pop')
        ],
        'arithmetic/if': [
            (r'(?![%s"^%%\d(),=+\-*/!~])%s' % (_punct, _token), Text),
            include('arithmetic')
        ],
        '(?': [
            (_space, Text),
            (r'\(', Punctuation, ('#pop', 'else?', 'pump-statement/compound')),
            default('#pop')
        ],
        'else?': [
            (_space, Text),
            (r'else%s' % _token_terminator, Keyword, '#pop'),
            default('#pop')
        ],

        '_root': [
            # Lines can start with @ to prevent echo
            (r'^\s*@', Punctuation),
            (r'^(\s*)(rem\s.*)$', bygroups(Text, Comment)),
            (r'".*?"', String.Double),
            (r"'.*?'", String.Single),
            # If made more specific, make sure you still allow expansions
            # like %~$VAR:zlt
            (r'%%?[~$:\w]+%?', Name.Variable),
            (r'::.*', Comment), # Technically :: only works at BOL
            (r'\b(set)(\s+)(\w+)', bygroups(Keyword, Text, Name.Variable)),
            (r'\b(call)(\s+)(:\w+)', bygroups(Keyword, Text, Name.Label)),
            (r'\b(goto)(\s+)(\w+)', bygroups(Keyword, Text, Name.Label)),
            (r'\b(set|call|echo|on|off|endlocal|for|do|goto|if|pause|'
             r'setlocal|shift|errorlevel|exist|defined|cmdextversion|'
             r'errorlevel|else|cd|md|del|deltree|cls|choice)\b', Keyword),
            (r'\b(equ|neq|lss|leq|gtr|geq)\b', Operator),
            include('_basic'),
            (r'.', Text),
        ],
        '_echo': [
            # Escapes only valid within echo args?
            (r'\^\^|\^<|\^>|\^\|', String.Escape),
            (r'\n', Text, '#pop'),
            include('_basic'),
            (r'[^\'"^]+', Text),
        ],
        '_basic': [
            (r'".*?"', String.Double),
            (r"'.*?'", String.Single),
            (r'`.*?`', String.Backtick),
            (r'-?\d+', Number),
            (r',', Punctuation),
            (r'=', Operator),
            (r'/\S+', Name),
            (r':\w+', Name.Label),
            (r'\w:\w+', Text),
            (r'([<>|])(\s*)(\w+)', bygroups(Punctuation, Text, Name)),
        ],
    }


class TcshLexer(RegexLexer):
    """
    Lexer for tcsh scripts.

    .. versionadded:: 0.10
    """

    name = 'Tcsh'
    aliases = ['tcsh', 'csh']
    filenames = ['*.tcsh', '*.csh']
    mimetypes = ['application/x-csh']

    tokens = {
        'root': [
            include('basic'),
            (r'\$\(', Keyword, 'paren'),
            (r'\${#?', Keyword, 'curly'),
            (r'`', String.Backtick, 'backticks'),
            include('data'),
        ],
        'basic': [
            (r'\b(if|endif|else|while|then|foreach|case|default|'
             r'continue|goto|breaksw|end|switch|endsw)\s*\b',
             Keyword),
            (r'\b(alias|alloc|bg|bindkey|break|builtins|bye|caller|cd|chdir|'
             r'complete|dirs|echo|echotc|eval|exec|exit|fg|filetest|getxvers|'
             r'glob|getspath|hashstat|history|hup|inlib|jobs|kill|'
             r'limit|log|login|logout|ls-F|migrate|newgrp|nice|nohup|notify|'
             r'onintr|popd|printenv|pushd|rehash|repeat|rootnode|popd|pushd|'
             r'set|shift|sched|setenv|setpath|settc|setty|setxvers|shift|'
             r'source|stop|suspend|source|suspend|telltc|time|'
             r'umask|unalias|uncomplete|unhash|universe|unlimit|unset|unsetenv|'
             r'ver|wait|warp|watchlog|where|which)\s*\b',
             Name.Builtin),
            (r'#.*', Comment),
            (r'\\[\w\W]', String.Escape),
            (r'(\b\w+)(\s*)(=)', bygroups(Name.Variable, Text, Operator)),
            (r'[\[\]{}()=]+', Operator),
            (r'<<\s*(\'?)\\?(\w+)[\w\W]+?\2', String),
            (r';', Punctuation),
        ],
        'data': [
            (r'(?s)"(\\\\|\\[0-7]+|\\.|[^"\\])*"', String.Double),
            (r"(?s)'(\\\\|\\[0-7]+|\\.|[^'\\])*'", String.Single),
            (r'\s+', Text),
            (r'[^=\s\[\]{}()$"\'`\\;#]+', Text),
            (r'\d+(?= |\Z)', Number),
            (r'\$#?(\w+|.)', Name.Variable),
        ],
        'curly': [
            (r'}', Keyword, '#pop'),
            (r':-', Keyword),
            (r'\w+', Name.Variable),
            (r'[^}:"\'`$]+', Punctuation),
            (r':', Punctuation),
            include('root'),
        ],
        'paren': [
            (r'\)', Keyword, '#pop'),
            include('root'),
        ],
        'backticks': [
            (r'`', String.Backtick, '#pop'),
            include('root'),
        ],
    }


class PowerShellLexer(RegexLexer):
    """
    For Windows PowerShell code.

    .. versionadded:: 1.5
    """
    name = 'PowerShell'
    aliases = ['powershell', 'posh', 'ps1', 'psm1']
    filenames = ['*.ps1','*.psm1']
    mimetypes = ['text/x-powershell']

    flags = re.DOTALL | re.IGNORECASE | re.MULTILINE

    keywords = (
        'while validateset validaterange validatepattern validatelength '
        'validatecount until trap switch return ref process param parameter in '
        'if global: function foreach for finally filter end elseif else '
        'dynamicparam do default continue cmdletbinding break begin alias \\? '
        '% #script #private #local #global mandatory parametersetname position '
        'valuefrompipeline valuefrompipelinebypropertyname '
        'valuefromremainingarguments helpmessage try catch throw').split()

    operators = (
        'and as band bnot bor bxor casesensitive ccontains ceq cge cgt cle '
        'clike clt cmatch cne cnotcontains cnotlike cnotmatch contains '
        'creplace eq exact f file ge gt icontains ieq ige igt ile ilike ilt '
        'imatch ine inotcontains inotlike inotmatch ireplace is isnot le like '
        'lt match ne not notcontains notlike notmatch or regex replace '
        'wildcard').split()

    verbs = (
        'write where wait use update unregister undo trace test tee take '
        'suspend stop start split sort skip show set send select scroll resume '
        'restore restart resolve resize reset rename remove register receive '
        'read push pop ping out new move measure limit join invoke import '
        'group get format foreach export expand exit enter enable disconnect '
        'disable debug cxnew copy convertto convertfrom convert connect '
        'complete compare clear checkpoint aggregate add').split()

    commenthelp = (
        'component description example externalhelp forwardhelpcategory '
        'forwardhelptargetname functionality inputs link '
        'notes outputs parameter remotehelprunspace role synopsis').split()

    tokens = {
        'root': [
            # we need to count pairs of parentheses for correct highlight
            # of '$(...)' blocks in strings
            (r'\(', Punctuation, 'child'),
            (r'\s+', Text),
            (r'^(\s*#[#\s]*)(\.(?:%s))([^\n]*$)' % '|'.join(commenthelp),
             bygroups(Comment, String.Doc, Comment)),
            (r'#[^\n]*?$', Comment),
            (r'(&lt;|<)#', Comment.Multiline, 'multline'),
            (r'@"\n', String.Heredoc, 'heredoc-double'),
            (r"@'\n.*?\n'@", String.Heredoc),
            # escaped syntax
            (r'`[\'"$@-]', Punctuation),
            (r'"', String.Double, 'string'),
            (r"'([^']|'')*'", String.Single),
            (r'(\$|@@|@)((global|script|private|env):)?\w+',
             Name.Variable),
            (r'(%s)\b' % '|'.join(keywords), Keyword),
            (r'-(%s)\b' % '|'.join(operators), Operator),
            (r'(%s)-[a-z_]\w*\b' % '|'.join(verbs), Name.Builtin),
            (r'\[[a-z_\[][\w. `,\[\]]*\]', Name.Constant),  # .net [type]s
            (r'-[a-z_]\w*', Name),
            (r'\w+', Name),
            (r'[.,;@{}\[\]$()=+*/\\&%!~?^`|<>-]|::', Punctuation),
        ],
        'child': [
            (r'\)', Punctuation, '#pop'),
            include('root'),
        ],
        'multline': [
            (r'[^#&.]+', Comment.Multiline),
            (r'#(>|&gt;)', Comment.Multiline, '#pop'),
            (r'\.(%s)' % '|'.join(commenthelp), String.Doc),
            (r'[#&.]', Comment.Multiline),
        ],
        'string': [
            (r"`[0abfnrtv'\"\$`]", String.Escape),
            (r'[^$`"]+', String.Double),
            (r'\$\(', Punctuation, 'child'),
            (r'""', String.Double),
            (r'[`$]', String.Double),
            (r'"', String.Double, '#pop'),
        ],
        'heredoc-double': [
            (r'\n"@', String.Heredoc, '#pop'),
            (r'\$\(', Punctuation, 'child'),
            (r'[^@\n]+"]', String.Heredoc),
            (r".", String.Heredoc),
        ]
    }
