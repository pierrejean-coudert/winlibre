# Introduction #

We will discuss how to get the source code, structure of the project and the build tool we used to generate documentation, tests and binaries.

# Development Environment #

## Get the Source Code ##

The main repository of the source is on [code.google](http://code.google.com/p/winlibre). We also have a Git repository on [github](http://github.com/bcachet/winlibrepacman) and a Mercurial one on [bitbucket](http://bitbucket.org/bcachet/winlibre/).

### Work with SVN ###

You can download subversion binaries from [tigris website ](http://subversion.tigris.org/).

To get source you have to check out the code:
  * Anonymously:
> > ` svn checkout http://winlibre.googlecode.com/svn/trunk/ winlibre `.


> This way you can't commit your modification onto the repository, it's a ReadOnly access.
  * Using your code.google ID:
> > ` svn checkout https://winlibre.googlecode.com/svn/trunk/ winlibre --username your.code.google.ID `


> This way you will be able to commit your modifications onto the repository. You will
> need to send us an email to obtain Write access onto this SVN repository.

To commit modification you have done, you have to run the **svn commit -m "Message that
indicates what you have modified"**

You can have more informations about SVN on their [FAQ](http://subversion.tigris.org/faq.html) or by running **svn help**.


### Work with GIT ###

You can download binaries for your OS from [here](http://git-scm.com/download) and find
information on how to use git with github [here](http://github.com/guides/home).

### Work with Mercurial ###

You can download Mercurial (hg) binaries from [selenic website](http://www.selenic.com/mercurial/wiki/BinaryPackages). They also provide a very good [beginner guide](http://www.selenic.com/mercurial/wiki/QuickStart) and a more [advanced tutorial](http://www.selenic.com/mercurial/wiki/Tutorial)

You can find interesting [QuickStart](http://stuff.mit.edu/afs/athena/software/mercurial_v1.0.1/QuickStart.png) and a [User Guide](http://www.ivy.fr/mercurial/ref/v1.0/Mercurial-Usage-v1.0-300dpi.png)


## Prepare Development Environment ##

First you will need to generate the virtual environnement which will contain all the python libraries we need for our development.
To do this, launch the following command from the project directory:
```
  python bootstrap.py
```

For the Package Manager project, we get the list of available packages from the repository server. Actually this repository server does not exist anywhere on the Web. At this time our "repository" is a local HTTP server. You will need to specify the address of your local HTTP server in ./package\_manager/winlibre.py file. You can use EasyPHP to manage a HTTP server very easily on Windows.

For the Package Manager project, we also need to install [python for windows extensions](http://starship.python.net/crew/mhammond/win32/) library which is used in the SMART port on windows platform. This library is normally installed when you launch the bootstrap.py script, but sometime it fails and you need to install it by yourself, from binaries.

# Structure of the project #

## Global structure ##

Here is the structure of the global project when you download it:


|   **Type**      |  **File Name**   |  **Description**             |
|:----------------|:-----------------|:-----------------------------|
|   file        | bootstrap.py   | Script that generates the virtual environnement used for our development. |
|  directory    | docs/          |  **source** directory contains all the documents that will be used to generate the documentation. **build** directory contains the generated documentation    |
|  directory    | package\_manager | Subdirectory associated to the Package Manager which will install packages downloaded from repository. |
|  directory    | package\_creator | Subdirectory associated to the Package Creator which will be used to generate packages stored onto repository and used by package manager to install associated application  |
|  directory    | repository      | Source code of the web application that will be used to store information about available packages |
|   file        | pavement.py     | Paver configuration file. |
|   file        | setup.py        | Alias to the Paver utility to be compatible with distutils |
|  directory    |   tests         | Places to store source code used to test the complete platform |

Each directory associated to part of a project (package\_manager, package\_creator, repository) contains its own **tests** directory where unittest source code associated to the given project is stored.

In a later stage, each directory associated to part of a project will also contains its own **docs** directory.


### Package\_Manager project ###

The following table describes organisation of the package\_manager project.

|   **Type**      |  **File Name** | **Description** |
|:----------------|:---------------|:----------------|
|  directory  | smart/     | Contains the source code of the SMART library. Source code of our GUI, backends and channels will be added to smart/interfaces, smart/backends, smart/channels directories |
|  directory  |   wpkg    | Contains the modules used to manage Windows packages (MSI, NSIS ...) |
|  directory  | datadir/  | **pacmandir** directory is the working directory of the SMART library. Cached data will be stored here. |
|   file      | winlibre.py | Application launcher.|



# Paver scripting tool #

We manage our project using the [Paver](http://www.blueskyonmars.com/projects/paver/) scripting tool. We use it to generate the documentation (using the [Sphinx](http://sphinx.pocoo.org/) tool), find and launch unittests (via the [nose](http://somethingaboutorange.com/mrl/projects/nose/) tool).

You can perform several actions:

  * Generating documentation:
> > ./bin/paver html

  * Finding and performing unittests:
    * All the tests of each sub-projects
> > > ` ./bin/paver test   `
    * Tests of a specific sub-project:
> > > ` ./bin/paver test subproject_name `

  * Cleaning .pyc and temporary files:

> > ./bin/paver clean

  * Cleaning generating documentation:
> > ./bin/paver doc\_clean

  * Cleaning ending of files:
> > ./bin/paver endings

# Used Libraries #

## SMART ##

Our development is axis around SMART library. We use it to get the list of available packages, to download them, and to handle cached files.

The **smart** directory contains the [Windows branch](https://code.launchpad.net/~afb/smart/windows) of the SMART library

Every basic commands are handle from the **commands** which call the **controller** module (from control.py) to perform them.

Controller module get list of available packages by fetching channels. All supported  hannels (such as apt, rpm, yast) defined some specific files into the **channels**  irectory. From these files SMART knows how to get informations from available packages from repositories.

SMART interact with packages using backends adapted to the channel that has been used to  et these packages. All the supported channels define some backends in the **backends**  irectory. These backends will be used to get informations about packages.

We will study an example, installing firefox on Ubuntu using apt channel from SMART:

  * Controller gets information about available packages using the code into  **channels/apt\_deb** files. SMART will search for firefox package. As soon as it find it,  it will get informations about it using the **backends/deb/** files.
  * From these informations it will find dependencies. From **backends/deb/** files it will know how to call **apt** tool to install dependencies and firefox packages.

SMART has its own CLI/GUI. We can use them to test our Windows backend and then develop our own solution.