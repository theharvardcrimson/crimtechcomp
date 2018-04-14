git it?
=======

Everything you need to know about git! Helpful resources: `1`_ and `2`_!
Full documentation `here`_!

--------------

Git-ing Started
---------------

What is git?
~~~~~~~~~~~~

*Git is a free and open source distributed version control system
designed to handle everything from small to very large projects with
speed and efficiency.*

The Git feature that really makes it stand out is its branching model.
To learn more about git, go
`here <https://git-scm.com/about/branching-and-merging>`__!

Put your name on it!
~~~~~~~~~~~~~~~~~~~~

::

    $ git config --global user.name "[name]"

Set a username that will be attached to all your commit transactions

For example: ``git config --global user.name "queenrachel"``

Download a new project
~~~~~~~~~~~~~~~~~~~~~~

::

    $ git clone [url]

This is something you have done or will do when you first join CrimTech!
When cloning a repository from GitHub, click on the green ‘Clone or
download’ button on the right-hand side and copy the URL to be put in
place of [url].

For example:
``git clone https://github.com/rachelkang/crimsononline.git``

Create your own (local) branch!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ git branch [branch-name]

Create a new branch to work on! This way, you’re not working directly on
the main line and you can work directly on your own “local” branch (that
only you can see) without messing up the website! For example:
``git branch RachelIsTheBest``

Conversely, if you, for whatever reason, want to **delete** a branch you
have created:

::

    $ git branch -d [branch-name]

--------------

Working on your branch
----------------------

More useful git branch features!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ git branch

In case you forget about what local branches you have in the current
repository, ``git branch`` will list all of them for you!

::

    $ git branch -a

This is similar to ``git branch``, but it also lists all remote branches
in addition to all local branches. (Note: A remote branch is a branch on
a remote location, and when a local branch is pushed to a remote
location, the version of the branch on that remote location is the
remote branch)

What branch am I working on?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ git branch

In addition to listing all your local branches, ``git branch`` marks
your current branch with an asterisk ``*``.

For example: When I run ``git branch``, I see the following (below).
Because ``RachelIsTheBest`` is marked with a ``*``, I know that
``RachelIsTheBest`` is the branch that I am currently working on.

::

    * RachelIsTheBest
      master

Working on the wrong branch?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    $ git checkout [branch-name]

If you want to switch the branch you’re working on from one to another,
run ``git checkout NameOfBranchYouAreSwitchingTO``. This will work as
long as there are no uncommitted changes.

For example: If I’m currently on the master branch and would like to
switch to my local branch, rachelkang, I would run
``git checkout RachelIsTheBest`` and I would be
``Switched to branch 'RachelIsTheBest'``.

Updating your local
~~~~~~~~~~~~~~~~~~~

::

    $ git pull

Occasionally, you'll need to update your local branch as the main is
being updated. To "download bookmark history and incorporate changes",
as git puts it, it's good practice to ``git pull`` regularly.

Work in progress
~~~~~~~~~~~~~~~~

::

    $ git commit -m "[descriptive message]"

``git commit`` with a message to record file snapshots permanently in
version history, in case you may want to return to a previous saved
version.

For example: ``git commit -m "rachel is the best"``

::

    $ git revert [NameOfCommit]

This command creates "a new commit that undoes all of the changes
introduced" in NameOfCommit and then applies it to the current branch.
``git revert`` is used to remove an entire commit from the history of
the project, by adding a new commit to undo the commit to be removed.

Note: ``git revert`` and ``git reset`` are completely different.
``git revert`` "undoes a single commit" and "does not "revert" back to
the previous state of a project by removing all subsequent commits" as
does ``git reset``. ``git revert`` is often the better move (than is
``git reset``) because (1) it is 'safe' and doesn't alter the history,
and (2) it can target any individual commit at any arbitrary point in
the history.

For more information on ``git revert``, go
`here <https://www.atlassian.com/git/tutorials/undoing-changes>`__. For
full documentation of ``git revert``, go
`here <https://git-scm.com/docs/git-revert>`__.

::

    git reset

If, for some reason, you pull a Nathan Lee and you need to delete
everything on a branch but cannot delete the actual branch (like
master), then you might want to execute:

``git reset --hard origin/NameOfBranch`` to reset all tracked files
(actually discards files unlike ``git revert``).

``git clean -d -f`` to reset all untracked files.

Looking back in time!!!
~~~~~~~~~~~~~~~~~~~~~~~

::

    $ git log

This is a cool feature that allows you to look over the "version history
for the current branch" and what's happened to the repository you're in.

::

    $ git log --follow [file]

This is similar to ``git log``, but is more specific to a specified file
and also includes renames.

::

    $ git status

This feature lists all changed files (both new and old) that have not
yet been committed. This is helpful not only in keeping track of what
still needs to be committed but in keeping track of changes that were
meant to be temporary

--------------

Leaving your mark
-----------------

::

    $ git push [alias] [branch]

This is used frequently to upload all your local branch commits to
GitHub! If you only have one branch (the likely scenario), ``git push``
alone will suffice.

If you have multiple branches, however, run ``git push origin master``
to specify that you want to 'push' to the master branch (the main).

If you encounter the following error,
``current branch NameOfBranch has no upstream branch``, that probably
means this is your first time pushing! YAYY :) To set up the branch in
your remote repository, run ``git push -u origin NameOfBranch``.

::

    $ git merge [branch]

This is not a feature you need to worry much about, but it is helpful to
understand. After you push your commits to GitHub, the Tech Chairs,
after approving changes you have made, ``git merge`` to "combines the
specified branch’s history into the current branch". In other words, the
Execs ``git merge`` to apply your changes to the main and officially
make your mark in the codebase!
