from mini_git.models import Object
from mini_git.core.object_store import ObjectStore
from mini_git.core.git_repository import GitRepository


class AddCommand:
    def __init__(self, git_repository: GitRepository):
        self.object_store = ObjectStore(git_repository=git_repository)

    def _save_object(self, object: Object) -> None:
        self.object_store.save_object(object)

    def execute(self, path):
        print("Add Command")
        if not path:
            print("No files specified to add.")
            return
        object = Object.from_path(path)
        # FIXME: 想定とは異なるものが保存されているようだ
        self._save_object(object)
