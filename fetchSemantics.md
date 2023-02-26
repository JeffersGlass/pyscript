This proposal expands the section "Python Plugin Installation Location" from Discussion #### XXXXXXXXXXXX.

# Where do Plugins Go in the Virtual Filesystem?

At the offsite, we didn't come to a conclusion as to where exactly the plugin entrypoint file (and any addtional files `fetch`'d by the plugin) end up in the Virtual Filesystem. For the sake of showing examples of the options we discussed, we'll invent a new `fado` plugin with a few files. We'll use the following partial metadata file:

```json
{
    "name": "fado",
    "language": "python",
    "entrypoint": "singer",
    "fetch": [
        {
            "files": ["singer.py"]
        },
        {
            "files": ["cod.py", "frenchfries.csv"],
            "to_folder": "dinner"
        },
    ]
}
```

## (1) "Home"
Files are fetched relative to the current working directory where Pyodide defaults to execution (/home/pyodide/), the same as they are for normal [[fetch]] configurations. The resulting file structure is:

```
/home/pyodide/
  ├─ pyscript.py
  ├─ singer.py
  ├─ dinner
  │  ├─ cod.py
  │  ├─ frenchfries.csv
```

This allows the user to write, in their \<py-script\> tags: 
  - `from singer import vasco`
  - `from dinner import cod`

## (2) Folder-Per-Plugin
For each plugin, a new folder is created in the home directory with the name of the plugin. The fetch configurations are executed relative to that folder. The resulting file structure is:

```
/home/pyodide/
  ├─ pyscript.py
  ├─ fado
  │  ├─ singer.py
  │  ├─ dinner
  │  │  ├─ cod.py
  │  │  ├─ frenchfries.csv
```

This allows the user to write, in their \<py-script\> tags: 
  - `from fado.singer import vasco`
  - `from fado.dinner import cod`

## (3) 'Plugins' Folder
A folder called `plugins` is created in the home directory. For each plugin a new folder is created within _that_ folder with the name of the plugin. The resulting file structure is:

```
/home/pyodide/
  ├─ pyscript.py
  ├─ plugins
  │  ├─ fado
  │  │  ├─ singer.py
  │  │  ├─ dinner
  │  │  │  ├─ cod.py
  │  │  │  ├─ frenchfries.csv
```

This allows the user to write, in their \<py-script\> tags: 
  - `from plugins.fado.singer import vasco`
  - `from plugins.fado.dinner import cod`