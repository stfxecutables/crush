\def\fileversion{1.0}
\def\filedate{2008/01/28}
\def\docdate{2008/01/28}

\NeedsTeXFormat{LaTeX2e}

\ProvidesClass{thesis}
   [\filedate\space v\fileversion\space
    StFX Math Dept thesis class]

\newcommand{\stfx@ptsize}{11pt}
\DeclareOption{10pt}{\renewcommand{\stfx@ptsize}{10pt}}
\DeclareOption{11pt}{} % \stfx@ptsize already set to 11pt
\DeclareOption{12pt}{\renewcommand{\stfx@ptsize}{12pt}}
\ProcessOptions
\LoadClass[\stfx@ptsize]{report}
\RequirePackage{afterpage}
\RequirePackage{epsfig}
\RequirePackage{graphics}
\RequirePackage{amsfonts}
\RequirePackage{amssymb}
\RequirePackage{amsthm}
\RequirePackage{url}

\textwidth 6.2in
\textheight 8.7in
\topmargin -0.6in
\oddsidemargin 0.3in

\def\@title{}
\def\@author{}
\def\faculty#1{\gdef\@faculty{#1}}
\def\degree#1{\gdef\@degree{#1}}
\def\program#1{\gdef\@program{#1}}

\newif\if@masters             \@mastersfalse
\newif\if@honours             \@honoursfalse
\newif\if@supervisor          \@supervisorfalse
\newif\if@first@supervisor    \@first@supervisorfalse
\newif\if@second@supervisor   \@second@supervisorfalse
\newif\if@reader              \@readerfalse
\newif\if@first@member        \@first@memberfalse
\newif\if@second@member       \@second@memberfalse
\newif\if@third@member        \@third@memberfalse
\newif\if@fourth@member       \@fourth@memberfalse
\newif\if@fifth@member        \@fifth@memberfalse

\def\bah{\degree{Bachelor of Arts with Honours}%
         \@honourstrue%
         \gdef\@faculty{Arts}}

\def\baam{\degree{Bachelor of Arts with Advanced Major}%
          \gdef\@faculty{Arts}}

\def\bsch{\degree{Bachelor of Science with Honours}%
          \@honourstrue%
          \gdef\@faculty{Science}}

\def\bscam{\degree{Bachelor of Science with Advanced Major}%
           \gdef\@faculty{Science}}

\def\msc{\degree{Masters of Science}%
         \program{Computer Science}%
         \@masterstrue%
         \gdef\@faculty{Science}}

\def\month#1{\gdef\@month{#1}}
\def\year#1{\gdef\@year{#1}}

\def\supervisor#1{\gdef\@supervisor{#1}\@supervisortrue}
\def\firstsupervisor#1{\gdef\@first@supervisor{#1}\@first@supervisortrue}
\def\secondsupervisor#1{\gdef\@second@supervisor{#1}\@second@supervisortrue}

\def\reader#1{\gdef\@reader{#1}\@readertrue}

\def\firstmember#1{\gdef\@first@member{#1}\@first@membertrue}
\def\secondmember#1{\gdef\@second@member{#1}\@second@membertrue}
\def\thirdmember#1{\gdef\@third@member{#1}\@third@membertrue}
\def\fourthmember#1{\gdef\@fourth@member{#1}\@fourth@membertrue}
\def\fifthmember#1{\gdef\@fifth@member{#1}\@fifth@membertrue}

\newif\if@dedication        \@dedicationfalse

\def\dedication#1{\gdef\@dedication{#1}\@dedicationtrue}

\def\signature#1#2{%
   \parbox[b]{1in}{\smash{#1}\vskip12pt}\hfill
   \parbox[t]{3in}{%
      \shortstack{\vrule width 3in height 0.4pt\\\small#2}}%
   \vspace{0.5in}
}

\newcommand{\no@breaks}[1]{{\def\\{ \ignorespaces}#1}}

\renewcommand{\titlepage}{%
   \thispagestyle{empty}%
   \null\vspace*{0.5in}
   \begin{center}
      \hyphenpenalty=10000\Large\sc\@title
   \end{center}
   \vfill
   \begin{center}
      \large{By}\\
   \end{center}
   \begin{center}
      \Large\@author
   \end{center}
   \vfill
   \begin{center}
      \linespread{1}\normalsize % Switch to single-spacing
      \sc{Submitted in partial fulfillment of the \\
                 requirements for the degree of \\
                 \@degree\
                 in
                 \@program \\
                 at \\
                 Saint Francis Xavier University\\
                 Antigonish, Nova Scotia\\
                 \@month\  \@year
                 \linespread{1.37}
                 \vskip1in
                 \rmfamily \copyright\ Copyright by \@author, \@year
      }
   \end{center}
   \vspace*{0.2in}
   \clearpage
}

\newcommand{\signaturepage}{%
    \setcounter{page}{1}
    \pagenumbering{roman}
    \vspace*{0.5in}
    \begin{center}
    \sc{\large{Saint Francis Xavier University\\
                Department of\\
                Mathematics, Statistics and Computer Science
    }}
    \end{center}
    \vspace{.2in}
    The undersigned hereby certify that they have read a thesis
            entitled ``\textbf{\no@breaks\@title}'' by  \textbf{\@author}
            in partial fulfillment of the requirements for the degree of
            \textbf{\@degree}.\\
    \vspace{1in}\\
    \begin{tabular}{rrr}
       \hspace{1.1in} &   \signature{Dated:}{} \\
       \if@supervisor
          \hspace{1.1in} &   \signature{Supervisor:}{\@supervisor} \\
       \else
          \if@first@supervisor
             \hspace{1.1in} &   \signature{Co-supervisor:}{\@first@supervisor} \\
             \if@second@supervisor
                \hspace{1.1in} &   \signature{Co-supervisor:}{\@first@supervisor} \\
             \else
                \ClassWarningNoLine{thesis}{Requires second co-supervisor}
             \fi
          \else
             \ClassWarningNoLine{thesis}{Requires supervisor or co-supervisor}
          \fi
       \fi

       \if@masters
          \if@first@member
            \hspace{1.1in} &   \signature{Committee Member:}{\@first@member} \\
          \fi
          \if@second@member
            \hspace{1.1in} &   \signature{Committee Member:}{\@second@member} \\
          \fi
          \if@third@member
            \hspace{1.1in} &   \signature{Committee Member:}{\@third@member} \\
          \fi
          \if@fourth@member
            \hspace{1.1in} &   \signature{Committee Member:}{\@fourth@member} \\
          \fi
          \if@fifth@member
            \hspace{1.1in} &   \signature{Committee Member:}{\@fifth@member} \\
          \fi
       \fi
       \if@honours
          \if@reader
             \hspace{1.1in} &   \signature{Second Reader:}{\@reader} \\
          \else
             \if@supervisor
                \ClassWarningNoLine{thesis}{Honours thesis needs a second reader}%
             \fi
          \fi
       \fi
    \end{tabular}
    \clearpage
}

\newcommand{\permissionpage}{%
    \vspace*{0.5in}
    \begin{center}
    \sc{\huge{St. Francis Xavier University}}\\
    \vspace{0.2in}
    \sc{\Large{\@month\ \@year}}\\
    \end{center}
    \vspace{.5in}
    \addtolength{\tabcolsep}{0mm}
    \renewcommand{\arraystretch}{1.5}
    \begin{tabular}{ll}
        \sc{Author:}     & \sc{\@author}\\
        \sc{Title:}      & \sc{\no@breaks\@title}\\
        \sc{Department:} & \sc{Mathematics, Statistics and Computer Science}\\
        \sc{Faculty:}    & \sc{\@faculty}\\
        \sc{Convocation} & \sc{\@month\ \@year}\\
    \end{tabular}\\
    \vspace{0.5in}\\
    Permission is herewith granted to Saint Francis Xavier
        University to circulate and to have copied for non-commercial
        purposes, at its discretion, the above title upon request of
        individuals or institutions.\\
    \vspace{.5in}\\
    \hspace{3in} \signature{}{\@author}\\
    \vspace{0.5in}\\
    {\sc{ The author reserves other publication rights, and
        neither the thesis nor extensive extractions from it may be
        printed or otherwise reproduced without the author's written
        permission.}

     \sc{ The Author attests that permissions has been obtained for the use
        of any copyrighted material appearing in this thesis (other than
        brief excerpts requiring only proper acknowledgement in scholarly
        writing) and that all such use is clearly acknowledged.}}
    \clearpage
}

\def\dedicationpage{%
    \vspace*{2in}
    \begin{center}
    \em{\@dedication}
    \end{center}
    \vspace*{3in}
    \vfil\clearpage
}

\newif\if@title@page        \@title@pagetrue
\newif\if@signature@page    \@signature@pagetrue
\newif\if@permission@page   \@permission@pagetrue
\newif\if@contents@page     \@contents@pagetrue
\newif\if@tables@page       \@tables@pagetrue
\newif\if@figures@page      \@figures@pagetrue

\def\notitlepage{\@title@pagefalse}
\def\nosignaturepage{\@signature@pagefalse}
\def\nopermissionpage{\@permission@pagefalse}
\def\notableofcontents{\@contents@pagefalse}
\def\nolistoftables{\@tables@pagefalse}
\def\nolistoffigures{\@figures@pagefalse}

\def\frontmatter{%
   \pagenumbering{roman}
   \pagestyle{plain}
   \if@title@page
        \titlepage
   \fi
   \if@signature@page
       \signaturepage
   \fi
   \if@permission@page
       \permissionpage
   \fi
   \if@dedication
      \dedicationpage
   \fi
}

% Almost everything is double spaced.
%
\newcommand{\spacing}{1.8}

\renewenvironment{abstract}%
   {\def\baselinestretch{\spacing}
    \newpage\normalsize
    \chapter*{Abstract}}
   {\vfil\clearpage}

\newenvironment{acknowledgements}%
   {\def\baselinestretch{\spacing}
    \newpage\normalsize
    \chapter*{Acknowledgements}}
   {\vfil\clearpage}

\def\mainmatter{
    \def\baselinestretch{\spacing}
    \newpage\normalsize
    \if@contents@page
        \tableofcontents
        \newpage\normalsize
    \fi
    \if@tables@page
        \listoftables
        \newpage\normalsize
    \fi
    \if@figures@page
        \listoffigures
        \newpage\normalsize
    \fi
    \pagenumbering{arabic}
    \def\baselinestretch{\spacing}
    \newpage\normalsize
}

% Footnotes are to be single spaced.
%
\newcommand{\stfxfootnote}[1]{%
    \renewcommand{\baselinestretch}{1.0}%
    \footnote{#1}%
    \renewcommand{\baselinestretch}{\spacing}%
}

% Lengthy quotes must also be single spaced.
% We provide a parameter for the citation label too.
%
\newcommand{\stfxquote}[2]{%
    \renewcommand{\baselinestretch}{1.0}%
    \normalsize
    \begin{quote}{``\textsl{#1}''~\cite{#2}}\end{quote}
    \renewcommand{\baselinestretch}{\spacing}%
    \normalsize
}

%
% The \stfxepsfig command is used to insert a new EPS figure
% into our document.  Usage is:
%
%   \stfxepsfig[scale]{filename}{caption}
%
% Note:
%   - scale is optional (defaults to 1.0)
%   - Assumes that the EPS file is in the 'figures' directory.
%   - 'filename' should not include the filename extension.
%   - 'filename' also serves as the label for the figure.
%
\newcommand{\stfxepsfig}[3][1.0]{%
    \begin{figure}[!htbp]
    \centering
    \vspace{2mm}
    \scalebox{#1}{\includegraphics{figures/#2}}
    \caption{#3}
    \label{fig:#2}
    \end{figure}
}

%
% The \stfxbbfig command is used to insert a new PNG, JPG, GIF, or BMP figure
% into our document.  Usage is:
%
%   \stfxbbfig[bb=0 0 300 400]{filename}{caption}
%
% Note:
%   - bb argument required, first two values 0, others image size in pixels
%   - can add width, e.g. [bb=0 0 300 400, width=2.5in]
%   - Assumes that the file is in the 'figures' directory.
%   - 'filename' should not include the filename extension.
%   - 'filename' also serves as the label for the figure.
%
\newcommand{\stfxbbfig}[3][1.0]{%
    \begin{figure}[!htbp]
    \centering
    \vspace{2mm}
    \includegraphics[#1]{figures/#2}
    \caption{#3}
    \label{fig:#2}
    \end{figure}
}

\DeclareGraphicsExtensions{.jpg, .png, .bmp, .gif, .eps}

%
% The \stfxfig command is used to insert 'textual' figures
% into our document.  Usage is:
%
%   \stfxfig{label}{caption}{content}
%
\newcommand{\stfxfig}[3]{%
    \begin{figure}[!htbp]
    \centering
    \vspace{2mm}
    #3
    \caption{#2}
    \label{fig:#1}
    \end{figure}
}

%
% The \stfxtab command is used to insert a new table into our document.
% The \stfxtabsingle command is used to insert a single-spaced table into our document.
% Usage is:
%
%   \stfxtab{table_format}{label}{caption}{table_contents}
%
%   \stfxtabsingle{table_format}{label}{caption}{table_contents}
%
% Note that we could have created a \newenvironment, but opted for
% a \newcommand so as to be consistent with the \stfxepsfig command.
%
\newcommand{\stfxtab}[4]{%
    \begin{table}[!htbp]
    \centering
    \vspace{2mm}
    \begin{tabular}{#1}
    #4
    \end{tabular}
    \vspace{5mm}
    \caption{#3}
    \label{tab:#2}
    \end{table}
}

\newcommand{\stfxtabsingle}[4]{%
    \renewcommand{\baselinestretch}{1.0}%
    \stfxtab{#1}{#2}{#3}{#4}
    \renewcommand{\baselinestretch}{\spacing}%
}

%
% The \stfxeqn command is used to add an equation to the thesis.
% Usage is
%
%   \stfxeqn{label}{equation_body}
%
\newcommand{\stfxeqn}[2]{%
    \begin{equation}
    \centering
    \label{eqn:#1}
    #2
    \end{equation}
}

%
% For theorems and corollaries.
%
\newtheorem{cor}{Corollary}
\newtheorem{thm}{Theorem}
