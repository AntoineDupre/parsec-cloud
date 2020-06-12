from parsec.core.types import (
    FsPath,
    EntryID,
    LocalDevice,
    WorkspaceRole,
    LocalFolderishManifests,
    LocalFileManifest,
    DEFAULT_BLOCK_SIZE,
)


class WorkspaceFilesFS:
    def __init__(self, workspace_id: EntryID):
        self.workspace_id = workspace_id
