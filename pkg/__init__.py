"""Supported docstring formats
---------------------------
Currently, pure Markdown (with [extensions]), [numpydoc],
and [Google-style] docstrings formats are supported,
along with some reST directives.

*[reST]: reStructuredText
[extensions]: https://python-markdown.github.io/extensions/#officially-supported-extensions
[numpydoc]: https://numpydoc.readthedocs.io/
[Google-style]: http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings


### Supported reST directives

The following reST directives should work:

* specific and generic [admonitions],
* [`.. image::`][image] or `.. figure::` (without options),
* [`.. include::`][include], with support for the options:
  `:start-line:`, `:end-line:`, `:start-after:` and `:end-before:`.
* `.. versionadded::`
* `.. versionchanged::`
* `.. deprecated::`
* `.. todo::`

[admonitions]: http://docutils.sourceforge.net/docs/ref/rst/directives.html#admonitions
[image]: http://docutils.sourceforge.net/docs/ref/rst/directives.html#images
[include]: \
http://docutils.sourceforge.net/docs/ref/rst/directives.html#including-an-external-document-fragment
"""
