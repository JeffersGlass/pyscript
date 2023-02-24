# Overview

This proposal touches many parts of the usage and inclusion of External Plugins. For the purposes of this discussion, an "External Plugin" is any plugin that is not built-into the PyScript codebase. (I.e. not py-terminal, py-splashscreen, etc).

# Metadata File

## Keys

### Descriptive Keys
|Key|Type/Valid Values|Required/Optional|Description|
|--|--|--|--|
|`readableName`|string|Optional|An alternate name to be used as the "human readable name" of this plugin, in contexts where that is needed/appropriate
|`version`|string|optional|The version of this plugin. Versioning methodology is left to the user|
|`description`|string|optional|The verbose description of the plugin and its purpose|
|`author`|string|optional|The name of the author(s) of the plugin|
|`homeURL`|string|optional|The URL of the 'homepage' for this plugin. Could point to the user's homepage, reference documentation, etc.

### Functional Keys

|Key|Type/Valid Values|Required/Optional|Description|
|--|--|--|--|
|`name`|string|Required|The name of the plugin|


## Python Plugin-Specific Keys


# Py-Config

