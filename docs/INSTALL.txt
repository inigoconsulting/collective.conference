collective.conference Installation
----------------------------------

To install collective.conference using zc.buildout and the plone.recipe.zope2instance
recipe to manage your project, you can do this:

* Add ``collective.conference`` to the list of eggs to install, e.g.:

    [buildout]
    ...
    eggs =
        ...
        collective.conference
       
* Re-run buildout, e.g. with:

    $ ./bin/buildout
