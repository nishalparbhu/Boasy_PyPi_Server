# Boasy_PyPi_Server
The source code for a Boasy Python package server for our internal packages which is hosted via Github pages.

# Table of Contents
1. [Creating a new package](#Creating-a-new-package)
2. [Adding a new package](#Adding-a-new-package)
3. [Adding a new version of a package](#Adding-a-new-version-of-a-package)

## Creating a new package

When creating a new Python package for Boasy, it shouldn't be too dissimilar to any other Python package but we do have 
the convention that each new version of your package should be released onto a new branch in the repo with the naming 
structure as follows:

For version 0.0.1, a new branch should be created called `v0.0.1`

This should be repeated for any newer versions created as well as modifying the `setup.py` as well.

**[⬆ back to top](#table-of-contents)**

## Adding a new package

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
    <a href="git+{git_clone_link}@{branch_name}#egg={package-name}" data-requires-python="&gt;={python_version_required}">{package_name}-{version_number}</a><br/>
  </body>
</html>
```

All you need to do is replace the following:
- **package_name** is just the package name with underscores as before
- **package-name** is just the package name with hyphens as before
- **git_clone_link** (e.g. https://github.com/nishalparbhu/Boasy_PyPi_Server.git)
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
    <a href="git+{git_clone_link}@{branch_name}#egg={package-name}" data-requires-python="&gt;={python_version_required}">{package_name}-{version_number}</a><br/>
  </body>
```

All you need to do is add a new line under the last link in the same format but just make sure to change the 
**branch_name**, **version_number** and the **python_version_required** if needed.

**[⬆ back to top](#table-of-contents)**