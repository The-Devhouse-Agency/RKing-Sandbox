#Trying again, but with Python

# only modify files we're certain need to be renamed (to avoid accidentally renaming third party files or anything ambiguous)
# for ambiguous cases, simply alert. Can the actions generate code review responses?

import sys
import git
import git.diff
from github import Github

################ Module Vars ################

# Access the arguments
args_list = sys.argv[1:] #element 0 is the script name; we only want the arguments

repo_path = args_list[0]
pr_branch_name = args_list[1]
target_branch_name = args_list[2] #source of truth that we compare the PR against
created_by_header = args_list[3] #"//Created By:"
edited_by_header = args_list[4] #"//Edited By:"

repo = git.Repo(repo_path)
pr_commit: git.Commit = repo.branches[pr_branch_name].commit
target_commit: git.Commit = repo.branches[target_branch_name].commit

diff_index: git.diff.DiffIndex = pr_commit.diff(target_commit) # remember, b.diff(a)


################# Module Funcs #################

# Double strip in case the slicing exposes internal whitespace to the edge of the string
def can_overwrite_header_line(line_str, header) -> bool:
    return len(line_str.strip()[len(header):].strip()) <= 0

# get the first x characters where x is the size of the stripped leading whitespace
def get_indentation_whitespace(line_str: str) -> str:
    line_minus_leading_whitespace = line_str.lstrip()
    return line_str[:len(line_str) - len(line_minus_leading_whitespace)]

################# Main Execution #################

#for each file affected by this branch
for val in diff_index:
    file_diff: git.Diff = val
    
    ################# Validation #################

    #for each file, see if we can find the file's own entire history instead of just a branch diff
    file_path:str = file_diff.a_path # a as in a/b comparison
    change_type = file_diff.change_type

    if not file_path.endswith(".cs"): continue # we only care about c# scripts
    if change_type == "D": continue # we don't care about deleted files
    
    #TODO: Revisit what to do about this, if anything
    if change_type == "A":
        print("file was added; we can set Created By: and Edited By: fields")
    elif change_type == "M":
        print("file was modified; we can set Edited By: fields") #!we have no way to confirm who the original creator of the file is. 
    
    ################# Actual Logic #################
    
    # oldest-first list of unique commit author names
    # (converting it to a set first easily filters out duplicates)
    sorted_commit_authors: list = list(set(commit.author.name for commit in repo.iter_commits(paths=file_path))).reverse()
    
    combined_created_by_str = created_by_header + " " + sorted_commit_authors[0]
    combined_edited_by_str = edited_by_header + " " + (", ".join(sorted_commit_authors[1:]))
    
    # init with invalid marker for easy checking
    created_by_line_num = -1
    edited_by_line_num = -1
    
    #grab the file (on this branch) and update it
    with open(file_path, 'wt') as file:
        lines = file.readlines()
        
        # search for pre-existing "Created By" lines
        for i, line in enumerate(lines):
            if line.lower().strip().startswith(created_by_header.lower()): 
                created_by_line_num = i
                created_by_line_src_text = line
                break
        
        # search for pre-existing "Edited By" lines
        for i, line in enumerate(lines):
            if line.lower().strip().startswith(edited_by_header.lower()): 
                edited_by_line_num = i
                edited_by_line_src_text = line
                break
                
        # Update Lines
        
        # different logic cases based on what was (or wasn't) found
        if created_by_line_num >= 0:
            line_str = created_by_line_src_text

            if can_overwrite_header_line(line_str, created_by_header):
                lines[created_by_line_num] = get_indentation_whitespace(line_str) + combined_created_by_str
        else:
            #insert before first line (making this the new first line)
            lines.insert(0, combined_created_by_str) 
        
        if edited_by_line_num >= 0:
            line_str = edited_by_line_src_text
            
            if can_overwrite_header_line(line_str, edited_by_header):
                lines[edited_by_line_num] = get_indentation_whitespace(line_str) + combined_edited_by_str
        else:
            #insert before second line (making this the new second line)
            lines.insert(1, combined_edited_by_str) 
        
        file.writelines(lines)
    

        
    
        


