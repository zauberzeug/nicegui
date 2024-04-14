import fnmatch
from typing import Union, List, Callable, re

from fastapi.routing import APIRoute

from nicegui import core
from nicegui.single_page_router import SinglePageRouter, SinglePageRouterEntry


class SinglePageApp:

    def __init__(self,
                 target: SinglePageRouter,
                 included: Union[List[Union[Callable, str]], str, Callable] = '/*',
                 excluded: Union[List[Union[Callable, str]], str, Callable] = '') -> None:
        """
        :param included: Optional list of masks and callables of paths to include. Default is "/*" which includes all.
        If you do not want to include all relative paths, you can specify a list of masks or callables to refine the
        included paths. If a callable is passed, it must be decorated with a page.
        :param excluded: Optional list of masks and callables of paths to exclude. Default is "" which excludes none.
        Explicitly included paths (without wildcards) and Callables are always included, even if they match an
        exclusion mask.
        """
        self.spr = target
        self.included: List[Union[Callable, str]] = [included] if not isinstance(included, list) else included
        self.excluded: List[Union[Callable, str]] = [excluded] if not isinstance(excluded, list) else excluded
        self.system_excluded = ['/docs', '/redoc', '/openapi.json', '_*']

    def reroute_pages(self):
        """Registers the SinglePageRouter with the @page decorator to handle all routes defined by the router"""
        self._update_masks()
        self._find_api_routes()

    def is_excluded(self, path: str) -> bool:
        """Checks if a path is excluded by the exclusion masks

        :param path: The path to check
        :return: True if the path is excluded, False otherwise"""
        for inclusion_mask in self.included:
            if path == inclusion_mask:  # if it is a perfect, explicit match: allow
                return False
            if fnmatch.fnmatch(path, inclusion_mask):  # if it is just a mask match: verify it is not excluded
                for ex_element in self.excluded:
                    if fnmatch.fnmatch(path, ex_element):
                        return True  # inclusion mask matched but also exclusion mask
                return False  # inclusion mask matched
        return True  # no inclusion mask matched

    def _update_masks(self) -> None:
        """Updates the inclusion and exclusion masks and resolves Callables to the actual paths"""
        from nicegui.page import Client
        for cur_list in [self.included, self.excluded]:
            for index, element in enumerate(cur_list):
                if isinstance(element, Callable):
                    if element in Client.page_routes:
                        cur_list[index] = Client.page_routes[element]
                    else:
                        raise ValueError(
                            f'Invalid target page in inclusion/exclusion list, no @page assigned to element')

    def _find_api_routes(self) -> None:
        """Find all API routes already defined via the @page decorator, remove them and redirect them to the
        single page router"""
        from nicegui.page import Client
        page_routes = set()
        base_path = self.spr.base_path
        for key, route in Client.page_routes.items():
            if route.startswith(base_path) and not self.is_excluded(route):
                page_routes.add(route)
                Client.single_page_routes[route] = self
                title = None
                if key in Client.page_configs:
                    title = Client.page_configs[key].title
                route = route.rstrip('/')
                self.spr.add_router_entry(SinglePageRouterEntry(route, builder=key, title=title))
                route_mask = SinglePageRouterEntry.create_path_mask(route)
                self.spr.included_paths.add(route_mask)
        for route in core.app.routes.copy():
            if isinstance(route, APIRoute):
                if route.path in page_routes:
                    core.app.routes.remove(route)
