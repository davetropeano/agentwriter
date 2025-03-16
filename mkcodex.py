import zipfile
import frontmatter
import os
import glob

def levelize_markdown(content):
    """
    attempt to make sure headings are level 2 and beyond logically. Will presume that content doesn't have an H1 but only H2 and beyond
    """
    res = content.replace('#### ', '##### ')
    res = res.replace('### ', '#### ')
    res = res.replace('## ', '### ')
    return res

def process(path):
    entry = f'{path}/**/entry.md'
    for file in glob.glob(entry, recursive=True):
        post = frontmatter.load(file)
        print(f'## {post.metadata['name']}\n')
        print(levelize_markdown(post.content))
        print()

if __name__ == "__main__":
    with zipfile.ZipFile('nc-codex.zip', 'r') as zip_ref:
        zip_ref.extractall('nc-codex')

    root = './nc-codex'
    paths = ['characters', 'locations', 'other']
    for path in paths:
        print(f'# {path.capitalize()}\n')
        process(f'{root}/{path}')
