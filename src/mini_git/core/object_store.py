from mini_git.core.git_repository import GitRepository
from mini_git.models import Object


class ObjectStore:
    def __init__(self, git_repository: GitRepository):
        self.git_repository = git_repository

    def save_object(self, object: Object) -> None:
        object_dir = self.git_repository.git_path / "objects" / object.object_directory
        object_dir.mkdir(parents=True, exist_ok=True)
        object_path = self.git_repository.git_path / "objects" / object.object_path
        print(f"Saving object to {object_path}")
        with object_path.open("wb") as f:
            f.write(object.git_data)
