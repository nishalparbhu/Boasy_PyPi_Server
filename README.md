# Boasy_PyPi_Server
The source code for a Boasy Python package server for our internal packages which is hosted via Github pages.

# Table of Contents
1. [Downloading a new package](#Downloading-a-new-package)
2. [Creating a new package](#Creating-a-new-package)
   - [Guidelines](#Guidelines)
   - [Versioning](#Versioning)
   - [Dependencies](#Dependencies)
3. [Adding a new package](#Adding-a-new-package)
4. [Adding a new version of a package](#Adding-a-new-version-of-a-package)

## Downloading a new package

To download a package from this package index, you can do it directly from the command line as follows:

```shell script
pip install package_name --extra-index-url https://nishalparbhu.github.io/Boasy_PyPi_Server/
```

Or if you have a _requirements.txt_ file than you can just add the following two line to the file:

```requirements.txt
--extra-index-url https://nishalparbhu.github.io/Boasy_PyPi_Server/
package_name==0.0.1
```

You will also need to make sure that you have a valid SSH deploy key which is required to install the package. If 
you don't have one, you will need to get in contact with the owner of the package to see if they can grant you access to
the package with a deploy key. Once you have this deploy key, you will need to add it to your `~/.ssh` folder on your 
machine and then you will need to have a file called `config` which also goes in that folder and should look like this:

```text
Host package_one.github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa
    IdentitiesOnly yes

Host package_two.github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_rsa
    IdentitiesOnly yes
``` 

You must have this `config` file so that when you install, your ssh client knows which key to use to get that package. 

**[⬆ back to top](#table-of-contents)**

## Creating a new package

When creating a new Python package for Boasy, it shouldn't be too dissimilar to any other Python package.
 
We do have a few guidelines that we follow to make creating a package easy and safe which are listed below:

### Guidelines

- When creating a package, the workflow should go as follows:
   - Your actual package file must use underscores for the spaces between words not hyphens (to work with pip)
   - Your `master` branch is the production latest version of your package
   - Your `stable` branch is the stable version of your branch that you are currently working on
   - You create your `feat-my_new_change-{ticket_number}`, `refactor-using_new_module{ticket_number}`,
    `chore-something_else{ticket_number}` or other branches as normal and merge them into your `stable` branch when happy
   - You can then raise a PR to merge the `stable` branch into the `master` branch.
   - When you are ready to release the next version of your package, you need to create a release tag on Github with
     the version number in the format `v[0-9].[0.9].[0-9]` and associate it to the `stable` branch commit at the point
     of release. You should also detail in this release what the changes you made were in that update to the package
   - Once this is merged into `master`, it again contains the latest version and when the `master` branch is being 
    built in Jenkins, you should use the Jenkins freestyle job named `Boasy_Pypi_Package_Update` to automatically 
    deploy it to our PyPi server (see [the section below](#Automatically))

### Versioning

In order to keep your versions in check for your new package, we enforce that you follow the guidelines set out by this
document regarding semantic versioning https://semver.org/.

This guide gives clear instructions on how to do versioning to ensure that it is clear to the package consumers how your
package has been updated

### Dependencies

Below are some useful tips we have learnt about dependencies of your packages:

- When you are building a package which has optional dependencies of that package (they don't have to be installed with 
the package but for certains parts of the package they are required), then we use the `extras_require` field in your
`setup.py` file. More information on this can be found here: http://peak.telecommunity.com/DevCenter/setuptools#declaring-extras-optional-features-with-their-own-dependencies
- When you have dependencies of your project, make sure you follow this guide regarding the differences between your 
`setup.py` `install_requires` section vs a `requirements.txt` file: https://caremad.io/posts/2013/07/setup-vs-requirement/

**[⬆ back to top](#table-of-contents)**

## Adding a new package

If you want to add a new package, you have two options, if you have authorization to write to this repository, you can
add it in [manually](#Manually) following the steps there. The easier approach is to set up your job on Jenkins to add
the package [automatically](#Automatically) after an update to the `master` branch. Note using the automatic way 
requires less knowledge but it does require you to conform to the steps in [guidelines](#Guidelines) in terms of how 
you create the package.

### Automatically

To add a new package automatically, once your `master` branch is being built in Jenkins, you need to add a conditional
step to the build which does the following:

```text
    if (env.BRANCH_NAME == 'master') {
      stage('Updated PyPi server with result') {
        env.PACKAGE_VERSION = sh(returnStdout: true, script: "git tag --sort version:refname | tail -1").trim()
        echo "Adding package: my_boasy_package with version: ${PACKAGE_VERSION} to the PyPi server"
        build job: '../Boasy_Pypi_Package_Update', parameters: [[$class: 'StringParameterValue', name: 'PACKAGE_NAME', value: 'my_boasy_package'], [$class: 'StringParameterValue', name: 'PACKAGE_VERSION', value: "${PACKAGE_VERSION}"]], wait: true, propagate: true
        echo "Successfully added the package to the PyPi server"
      }
    }
```

What this does is call the `Boasy_Pypi_Package_Update` job to update the Pypi index with your new package and/or new 
version of the package. Note if you are implementing this in your pipeline, make sure that you change
 `my_boasy_package` to the lowercase name of your package with underscores and also that if needed, you change the 
 relative path of the build job to wherever your project is running run relatively on Jenkins.

**Note**: If you are running a pipeline job, then you will need to go into your configuration for the project and enable
fetching git tags by choosing `Advanced clone behaviours` and then ensuring that `fetch tags` is ticked.

 
### Manually

Once you've created a new Python package, to add it to the to the list of Python packages, you will need to modify the 
following file:

```shell script
Boasy_PyPi_Server/index.html
```

Then in this file find the following snippet of html:

```html
<div class="package">
<!--there will be package links here already in the format shown in the line below-->
<p><a href="boasy-authentication-package/">boasy_authentication_package</a></p>
</div>
```

Then find where your package should be listed (**keep it in alphabetical order**) and add the following line:

```html
<p><a href="package-name/">package_name</a></p>
```

Then you need to create a new folder within _Boasy_PyPi_Server_ called _package-name_ which should be the same as the
html above. In this folder you will also want to create a new `index.html` file which should be in the following format:


```html
<!DOCTYPE html>
<html>
  <head>
    <title>Links for package_name</title>
  </head>
  <body>
    <h1>Links for package_name</h1>
    <a href="git+ssh://git@{package_name}.github.com/nishalparbhu/{package_name}@{branch_name}#egg={package_name}-{version_number}" data-requires-python="&gt;={python_version_required}">{package_name}-{version_number}</a><br/>
  </body>
</html>
```

All you need to do is replace the following:
- **package_name** is just the package name with underscores as before
- **package-name** is just the package name with hyphens as before
- **ssh_git_clone_link** (e.g. https://github.com/nishalparbhu/Boasy_PyPi_Server.git)
- **branch_name**, this should be just the version number so for version 0.0.1 you should make a branch called v0.0.1
and this is the value of the **branch_name** variable
- **python_version_required** is the Python version needed to use this package
- **version_number** should be the same as **branch_name** just without the 'v' at the beginning

Once you've added this in, you can commit your additions and they will appear on the PyPi server once approved and
merged into the master :D

**[⬆ back to top](#table-of-contents)**

## Adding a new version of a package

To add a new version of a package, simply find the folder of your package in this repository and then open the 
`index.html` inside of that folder. Then you should find a section of your file that looks like this:

```html
  <body>
    <h1>Links for package_name</h1>
    <a href="git+ssh://git@{package_name}.github.com/nishalparbhu/{package_name}@{branch_name}#egg={package_name}-{version_number}" data-requires-python="&gt;={python_version_required}">{package_name}-{version_number}</a><br/>
  </body>
```

All you need to do is add a new line under the last link in the same format but just make sure to change the 
**branch_name**, **version_number** and the **python_version_required** if needed.

**[⬆ back to top](#table-of-contents)**