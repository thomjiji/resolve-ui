from .resolve_init import GetResolve
from .type import Folder, Timeline
import DaVinciResolveScript as dvr_script


class Resolve:
    """
    Resolve class

    This class is used to initialize some necessary objects for the baisc use of
    the API.
    """

    def __init__(self):
        """Initialize some necessary objects."""
        self.resolve = dvr_script.scriptapp("Resolve")
        self.project_manager = self.resolve.GetProjectManager()
        self.project = self.project_manager.GetCurrentProject()
        self.media_storage = self.resolve.GetMediaStorage()
        self.media_pool = self.project.GetMediaPool()
        self.root_folder = self.media_pool.GetRootFolder()
        self.current_timeline = self.project.GetCurrentTimeline()

    def get_all_timeline(self) -> list[Timeline]:
        """Get all existing timelines. Return a list containing all the timeline
        object.
        """
        all_timeline = []
        for timeline_index in range(1, self.project.GetTimelineCount() + 1, 1):
            all_timeline.append(self.project.GetTimelineByIndex(timeline_index))
        return all_timeline

    def get_timeline_by_name(self, timeline_name: str) -> str | Timeline:
        """Get timeline object by name."""
        all_timeline: list[Timeline] = self.get_all_timeline()
        timeline_dict = {
            timeline.GetName(): timeline for timeline in all_timeline  # type: ignore
        }
        return timeline_dict.get(timeline_name, "")

    def get_subfolder_by_name(self, subfolder_name: str) -> str | Folder:
        """Get subfolder (Folder object) under the root folder in the media
        pool.
        """
        all_subfolder = self.root_folder.GetSubFolderList()
        subfolder_dict: dict[str, Folder] = {
            subfolder.GetName(): subfolder for subfolder in all_subfolder
        }
        return subfolder_dict.get(subfolder_name, "")
