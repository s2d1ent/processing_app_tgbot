import git

update_url = 'https://github.com/s2d1ent/processing_app_tgbot'
update_path = './update'

git.Repo.clone_from(update_url, update_path)

def compare_version():
    None

def get_update():
    None