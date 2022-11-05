from typing import Union
from .resolve_init import GetResolve
from pybmd import timeline as bmd_timeline
from pybmd import folder as bmd_folder


class Resolve:
    """
    Resolve class

    This class is used to initialize some necessary objects for the baisc use of
    the API.

    Arrtibutes
    ----------
    resolve
        resolve object, the beginning of all the other object of DaVinci
        Resolve.
    project_manager
    project
    media_storage
    media_pool
    root_folder
    current_timeline

    """

    def __init__(self):
        """Initialize some necessary objects."""
        self.resolve = GetResolve()
        self.project_manager = self.resolve.GetProjectManager()
        self.project = self.project_manager.GetCurrentProject()
        self.media_storage = self.resolve.GetMediaStorage()
        self.media_pool = self.project.GetMediaPool()
        self.root_folder = self.media_pool.GetRootFolder()
        self.current_timeline = self.project.GetCurrentTimeline()

    def get_all_timeline(self) -> list[bmd_timeline.Timeline]:
        """
        Get all existing timelines. Return a list containing all the timeline
        object.
        """
        all_timeline = []
        for timeline_index in range(1, self.project.GetTimelineCount() + 1, 1):
            all_timeline.append(self.project.GetTimelineByIndex(timeline_index))
        return all_timeline

    def get_timeline_by_name(
        self, timeline_name: str
    ) -> Union[str, bmd_timeline.Timeline]:
        """Get timeline object by name."""
        all_timeline: list[bmd_timeline.Timeline] = self.get_all_timeline()
        timeline_dict = {
            timeline.GetName(): timeline for timeline in all_timeline  # type: ignore
        }
        return timeline_dict.get(timeline_name, "")

    def get_subfolder_by_name(
        self, subfolder_name: str
    ) -> Union[str, bmd_folder.Folder]:
        """
        Get subfolder (Folder object) under the root folder in the media pool.
        """
        all_subfolder = self.root_folder.GetSubFolderList()
        subfolder_dict: dict[str, bmd_folder.Folder] = {
            subfolder.GetName(): subfolder for subfolder in all_subfolder
        }
        return subfolder_dict.get(subfolder_name, "")

    def get_subfolder_recursively(self, recursion_begins_at_root=False) -> dict:
        """
        Traverse the media pool recursively, return a dictionary containing all
        the subfolders (Folder object) and their names.

        Parameters
        ----------
        recursion_begins_at_root:
            If True, the recursion will begin at the root folder. If False, the
            recursion will begin at the current selected folder in media pool.

        Returns
        -------
        dict
            A dictionary containing all the subfolders (Folder object) and their
            names.

        """
        if recursion_begins_at_root:
            current_selected_folder = self.root_folder
        else:
            current_selected_folder = self.media_pool.GetCurrentFolder()

        subfolder_dict = {}

        for subfolder in current_selected_folder.GetSubFolderList():
            # if subfolder has child bins, its `GetSubFolderList()` method will
            # return a list, otherwise it will return `[]` which is False. If it
            # is True (means subfolder does have child bins), it will go to the
            # next level of recursion until there is no child bin
            # (`GetSubFolderList` return `[]`).
            if subfolder.GetSubFolderList():
                self.media_pool.SetCurrentFolder(subfolder)
                subfolder_dict.setdefault(subfolder.GetName(), subfolder)
                subfolder_dict = (
                    subfolder_dict | self.get_subfolder_recursively()
                )
            else:
                subfolder_dict.setdefault(subfolder.GetName(), subfolder)

        return subfolder_dict

    def get_subfolder_by_name_recursively(
        self, subfolder_name: str, recursion_begins_at_root=False
    ):
        """
        Traverse the media pool recursively, find the subfolder (Folder object)
        by given name. If there are subfolders with the same name, it will only
        return the first one that appears.

        Parameters
        ----------
        subfolder_name:
            The name of the subfolder you want to find and get the corresponding
            Folder object of it.
        recursion_begins_at_root:
            If True, the recursion will begin at the root folder. If False, the
            recursion will begin at the current selected folder in the media
            pool.

        """
        return self.get_subfolder_recursively(recursion_begins_at_root).get(
            subfolder_name
        )
