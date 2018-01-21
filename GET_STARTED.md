## GET PUMPED (and started)
Sorry if this was confusing, but if you haven't already please go read _README.md_ first.

-----

### Beginning

Ok, so now that you've begun, let's get some stuff set up/explained (we promise you'll code soon). Github is a service that we'll be using a ton, and in essence, it's a version control framework that makes coding/developing "easy." That is, if you know what the terms "fork," "push," "pull," "clone," "branch," and "pull request" mean, it's easy. If you don't, fear not! That's what we're here for. 

Github usage is very vaguely modeled after a tree - there are repositories where code is stored (kinda like their own trees). These _repos_ have branches, where the _master_ branch is kinda like the tree trunk. Every other branch in the repository (you could name them anything, but maybe like _prod_, _dev_, _experimental_) is specific to the branch's purpose. When you want to work on your own repository, or one that you can contribute to direcly, you might _clone_ it onto your own machine (think copying the repository on Github over to your laptop). If there's a repo that you want to contribute to or don't own, you might _fork_ it (think making a copy that you intend to later add back to the original), then make a _pull request_ to merge them back together (this part's hard, don't worry too much about it. We will show you concrete examples). When you're working on a repo on your laptop, and you make a change, you'll want to _push_ your changes (with some brief intermediate steps) to the _remote_ repo (the one on Github). And when someone else made a change, and you want to update your local repo, you may _pull_ those changes from Github. Eventually, this will all make sense and be easy to understand. Until then (and afterwards, too), we're here for you. 

That's a very high level overview of Git and Github, and if it didn't make any sense, we are sorry for badly explaining it and want you not to worry, we're going to demo it for you too!

The above, but in bullet form:
> Repository (repo)- the place where code is stored, remote repos are (generally) on Github, local ones are (generally) on your personal laptop. Everyone can view the remote ones, only you can view the local ones (generally)
> Clone - you create a local copy of a Github repo on your laptop
> Fork - you create a copy of someone else's repo. This is different from clone in that clone: Github -> local, fork: Github -> Github. Fork copies the repository into your account on Github, but does not create a local copy. 
> Pull Request (PR) - takes that forked copy and asks to merge it back into the original repo
> Push/Pull - you pull code changes from remote to local (Github -> laptop), you push code changes from local to remote (laptop -> Github)

Example:
  1. You might _fork_ awesomeperson/cool_project.git to my_account/cool_project.git (Github -> Github)
  2. The you _clone_ my_account/cool_project.git (Github -> local) so you can work on it on your laptop
  3. Your partner _clones_ (my_account/cool_project.git -> my partner's laptop)
  4. You make a change, so you _push_ (update from local to my_account/cool_project.git)
  5. Your partner wants to see the change and made some of their own, so they _pull_ your changes (my_account/cool_project.git -> their laptop), then _push_ their own (their laptop -> my_account/cool_project.git)
  6. You then realize you've finished your team's contributions so one of you makes a _pull request_ to _merge_ my_account/cool_project.git with awesomeperson/cool_project.git
  7. awesomeperson then either accepts the changes, comments on some issues they have with the changes, or rejects the changes. 

Hopefully some part of this page was helpful, if not then you have our apologies. Please ask for help as needed as you begin actually coding (yay!)

Please proceed to _SETUP.md_ to continue on getting ready to code!

