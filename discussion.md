# Overview

This proposal changes how external plugins are located by PyScript, and how they are installed. For the purposes of this discussion, an 'external plugin' is any plugin that is not built-into the PyScript codebase. (I.e. _not_ py-terminal, py-splashscreen, etc).

This is based on the discussion by XXXXXXXXX on Friday, Feb 24 at the PyScript offsite. See [Future Expansion](#for-future-expansion) for elements of that conversation that have been left out of this proposal.

# Py-Config

This proposal makes a change to the contents of the `plugins` key in \<py-config\>. Previously, this was a list of URLs to single files ending in '.js' or '.py'; these resources were fetched and installed as plugins based on their file ending.

Under this proposal, the `plugins` key would contain a list of URLs pointing to metadata files as specified below. These can be .json or .toml resources; if the URL ends in one of these filetypes, PyScript will try to parse the file as the matching type. If the URL _doesn't_ end in either of these, it is attempted to be parsed as JSON, then as TOML.

# Metadata File

A plugin metadata file is a single JSON or TOML file containing all the information needed to describe, initialize, fetch resources for, and execute a plugin.

The description of the keys of the Metadata file are broken into two types for ease of reading: Functional Keys, which have a direct impact on the behavior of the plugin, how it is loaded/referenced/executed/etc.; and Descriptive Keys, which contain additional textual metadata about the plugin. There is no separation of the keys within the Metadata file; the distinction is purely notional.

## Functional Keys

Functional Keys contain values which have a direct effect on the loading an operation of the plugin. They comprise the only  required keys - `name`, `language`, and, for plugins written in Python, `entrypoint` - and additional optional keys which allow plugins to add values to the list of `packages` to install and `fetch` configurations to execute.

|Key|Type/Valid Values|Required/Optional|Description|
|--|--|--|--|
|`name`|string|Required|The name of the plugin, as it will be referenced within the PyScript App|
|`language`|string|Required|The language of the Plugin. Accepts js/JS/JavaScript or py/PY/Python (the exact list will be specified and documented).|
|`entrypoint`|string|Required for Python Plugins|The name of the module that will be imported; the plugin object should be an object in that module with the identifier `plugin`. XXXXXXX|
|`packages`|list[string]|Optional|Additional Python pacakags to install; these are prepended to the list of packages listed in \<py-config\> prior to attempting to install them all|
|`fetch`|list[fetchConfiguration]|Optional|Additional fetch configurations to execute; works the same as fetch configurations in \<py-config\>. These are files to be fetched and installed into the virtual filesystem which surrounds the Python runtime. These files are fetched before any fetch configurations listed by the user in \<py-config\>. Any relative URLs are treated as relative to the base path of the URL the plugin metadata file was retrieved from. See [Installation Location](#python-plugin-installation-location) for further discussion around exactly where in the filesystem these files should be installed.|
|`files`|list[url]|Optional|Additional files to be fetched into the browser's JavaScript namespace. Likely to be most-used with JS plugins XXXXXXXXXXX|
|`schema` XXXXXXXXXX |string|Optional|Specifies the version of the schema for the metadata file. If not specified or unparsable, PyScript defaults to using the latest specified metadata schema.| 

## Descriptive Keys

Descriptive Keys contain values which describe the project, its origin, usage, or documentation. They are available at run time to PyScript, but are not used to drive plugin-related behaviors directly within the app. The fields listed below _may_ be required if the plugin is to be included in a central plugin index; this is left to the discression of the the index creator. Users made include additional descriptive keys to their Metadata file if they wish.

|Key|Type/Valid Values|Required/Optional|Description|
|--|--|--|--|
|`readableName`|string|Optional|An alternate name to be used as the "human readable name" of this plugin, in contexts where it is needed/appropriate
|`version`|string|Optional|The version of this plugin. Versioning methodology is left to the user|
|`description`|string|Optional|The verbose description of the plugin and its purpose|
|`author`|string|Optional|The name of the author(s) of the plugin|
|`url`|string|Optional|The URL of the 'homepage' for this plugin. Could point to the user's homepage, reference documentation, etc.|

# Python Plugin Installation Location

At the offsite, we didn't come to a conclusion as to where exactly the plugin entrypoint file (and presumably, any addtional files `fetch`'d by the plugin?) end up in the Virtual Filesystem. We talked about several options - those options are listed (a should be discussed) in Discussion ### XXXXXXXXXX.

# For Future Expansion

This proposal does not cover some of the discussion of the discussion at the offsite. Specifically:

  - Allowing users to specify plugins by name (or URL) from central index, e.g. `PyScriptPlugins:pirateplug` or something instead of a fully qualified URL. 
  - Allowing plugins to 'depend' on each other, and exactly how this would work, both in a "what is the desired resolution behavior/order" sense and a "how is this specified by the plugin" sense. As it turns out, packaging is hard.

# Example

To illustrate the features of this new architecture, what follows is in the implementation of a plugin called XXXXXXXX, which XXXXXXXXXXXXX

## Index.html

## laserBeams.json

## laserBeams.py

