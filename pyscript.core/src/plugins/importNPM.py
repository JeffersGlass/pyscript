import sys
from collections.abc import Callable, Sequence
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec
from importlib.util import spec_from_loader
from types import ModuleType
from typing import Any

class NPMFinder(MetaPathFinder):
    def __init__(self) -> None:
        self.jsproxies: dict[str, Any] = {}
        self.hook: Callable[[JsProxy], None] = lambda _: None

    def find_spec(
        self,
        fullname: str,
        path: Sequence[bytes | str] | None,
        target: ModuleType | None = None,
    ) -> ModuleSpec | None:
        print(f"{fullname=}")
        print(f"{path=}")
        print(f"{target=}")
        return None
    
        [parent, _, child] = fullname.rpartition(".")
        if parent:
            parent_module = sys.modules[parent]
            if not isinstance(parent_module, JsProxy):
                # Not one of us.
                return None
            try:
                jsproxy = getattr(parent_module, child)
            except AttributeError:
                raise ModuleNotFoundError(
                    f"No module named {fullname!r}", name=fullname
                ) from None
            if not isinstance(jsproxy, JsProxy):
                raise ModuleNotFoundError(
                    f"No module named {fullname!r}", name=fullname
                )
        else:
            try:
                jsproxy = self.jsproxies[fullname]
            except KeyError:
                return None
        loader = JsLoader(jsproxy)
        return spec_from_loader(fullname, loader, origin="javascript")

    def register_js_module(self, name: str, jsproxy: Any) -> None:
        """
        Registers ``jsproxy`` as a JavaScript module named ``name``. The module
        can then be imported from Python using the standard Python import
        system. If another module by the same name has already been imported,
        this won't have much effect unless you also delete the imported module
        from :py:data:`sys.modules`. This is called by the JavaScript API
        :js:func:`pyodide.registerJsModule`.

        Parameters
        ----------
        name :
            Name of js module

        jsproxy :
            JavaScript object backing the module
        """
        assert JsProxy is not None
        if not isinstance(name, str):
            raise TypeError(
                f"Argument 'name' must be a str, not {type(name).__name__!r}"
            )
        if not isinstance(jsproxy, JsProxy):
            raise TypeError(
                f"Argument 'jsproxy' must be a JsProxy, not {type(jsproxy).__name__!r}"
            )
        self.hook(jsproxy)
        self.jsproxies[name] = jsproxy

    def unregister_js_module(self, name: str) -> None:
        """
        Unregisters a JavaScript module with given name that has been previously
        registered with :js:func:`pyodide.registerJsModule` or
        :py:func:`pyodide.ffi.register_js_module`. If a JavaScript module with that name
        does not already exist, will raise an error. If the module has already
        been imported, this won't have much effect unless you also delete the
        imported module from :py:data:`sys.modules`. This is called by the JavaScript
        API :js:func:`pyodide.unregisterJsModule`.

        Parameters
        ----------
        name :
            Name of the module to unregister
        """
        try:
            del self.jsproxies[name]
        except KeyError:
            raise ValueError(
                f"Cannot unregister {name!r}: no Javascript module with that name is registered"
            ) from None


class NPMLoader(Loader):
    def __init__(self, jsproxy: Any) -> None:
        self.jsproxy = jsproxy

    def create_module(self, spec: ModuleSpec) -> Any:
        return self.jsproxy

    def exec_module(self, module: ModuleType) -> None:
        pass

    # used by importlib.util.spec_from_loader
    def is_package(self, fullname: str) -> bool:
        return True


npmfinder: NPMFinder = NPMFinder()


for importer in sys.meta_path:
    if isinstance(importer, NPMFinder):
        raise RuntimeError("NPMFinder already registered")
#jsfinder.hook = hook
sys.meta_path.append(npmfinder)