from mini_git.core import GitRepository


class InitCommand:
    def __init__(self):
        pass

    def execute(self):
        print("Init Command")
        git_repository = GitRepository.init()
        print("Git repository initialized at:", git_repository.git_path)
