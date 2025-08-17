from mini_git.services import RepoContext, AddService


class AddCommand:
    def __init__(self):
        pass

    def execute(self, path):
        print("Add Command")
        if not path:
            print("No files specified to add.")
            return
        # ファイルの親ディレクトリからリポジトリを探索
        repo_context = RepoContext.require_repo(path.parent if path.is_file() else path)
        add_service = AddService(repo_context.object_store)
        add_service.add_object(path)
