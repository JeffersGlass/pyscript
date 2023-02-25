# Overview

This proposal touches many parts of the usage and inclusion of External Plugins. For the purposes of this discussion, an "External Plugin" is any plugin that is not built-into the PyScript codebase. (I.e. not py-terminal, py-splashscreen, etc).

# Metadata File

XXXXX Description of the metadata file

....XXXXX

## Keys

...XXXXX

### Functional Keys

|Key|Type/Valid Values|Required/Optional|Description|
|--|--|--|--|
|`name`|string|Required|The name of the plugin, as it will be referenced within the PyScript App|
|`language`|string|Required|The language of the Plugin. Accepts js/JS/JavaScript or py/PY/Python XXXX|
|`entrypoint`|string|Required for Python Plugins|The name of the module that will be imported; the plugin object should be in that module .plugin. XXXXXXXXXXX|
|`packages`|list[string]|optional|Additional Python pacakags to install; works the same as the `packages` key in \<py-config\>
|`fetch`|???|optional|Additional fetch configurations; works the same as fetch configurations in \<py-config\>



### Descriptive Keys
|Key|Type/Valid Values|Required/Optional|Description|
|--|--|--|--|
|`readableName`|string|Optional|An alternate name to be used as the "human readable name" of this plugin, in contexts where that is needed/appropriate
|`version`|string|optional|The version of this plugin. Versioning methodology is left to the user|
|`description`|string|optional|The verbose description of the plugin and its purpose|
|`author`|string|optional|The name of the author(s) of the plugin|
|`homeURL`|string|optional|The URL of the 'homepage' for this plugin. Could point to the user's homepage, reference documentation, etc.|

# Py-Config

...plugins now takes a list of URLs, relative or fully qualified XXXX. These are the URLs for the metadata file

# Example

## Index.html

## laserBeams.json

## laserBeams.py

