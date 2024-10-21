# MIT License
# 
# Copyright (c) 2024 Viktor Tyumenev
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 

import git

update_url = 'https://github.com/s2d1ent/processing_app_tgbot'

clone_path = '/home/viktor/Documents/processing_app_tgbot/update/'
update_path = '/home/viktor/Documents/processing_app_tgbot/src/'

version_file_repo = clone_path+'src/version'
version_file_local = update_path+'version'

local_version = str()
repo_version = str()
update = False
#git.Repo.clone_from(update_url, clone_path)

def compare_version():
    global update
    length = 0
    with open(version_file_local, 'r') as file:
        local_version = file.read()  # Чтение всего содержимого
    with open(version_file_repo, 'r') as file:
        repo_version = file.read()  # Чтение всего содержимого
    local_version = local_version.split('.')
    repo_version = repo_version.split('.')
    length = len(local_version) if len(local_version) < len(repo_version) else len(repo_version)
    for i in range(length-1, -1, -1):
        print(f"{int(repo_version[i])} : {int(local_version[i])}")
        if int(repo_version[i]) > int(local_version[i]): 
            update = True
        elif int(repo_version[i]) == int(local_version[i]): continue
        else:
            update = False

def get_update():
    global update
    

#compare_version()
if update:
    get_update()
else:
    print("Update don't needed")