# Keep the function signature,
# but replace its body with your implementation.
#
# Note that this is the driver function.
# Please write a well-structured implemention by creating other functions outside of this one,
# each of which has a designated purpose.
#
# As a good programming practice,
# please do not use any script-level variables that are modifiable.
# This is because those variables live on forever once the script is imported,
# and the changes to them will persist across different invocations of the imported functions.

#---------------------------------------------------------------------------------------------------------

# In order to confirm that my program was not calling any other commands, I ran my program with strace -f,
# effectively allowing me to view all of the processes that were created during a full run of my program.
# By manually parsing through the calls I can see that I open, read, access, close, etc. but do NOT call any 
# external commands. I also added the -e trace=process flag to look for any processes being created by my current
# process, but only found the exit call at the end of my program. To confirm that I was not using any git commands,
# I looked through the results of cat topo-test.tr | grep "git" > a.txt after running the strace command, effectively
# filtering all results of the trace and manually confirming no external git commands were called.



import os 
import sys
import zlib

#Commit Node Class - for each commit, stores the hash, a list of branch names associated with it, 
#a set of parent commit hashes and a set of child commit hashes
class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.branches = list()
        self.parents = set()
        self.children = set()


#Function to return the path to the nearest .git directory (searching upwards)
def discover_git_directory():
    #Initialize variables to point to current directory
    curr_path = "."

    # #Loop through current and all parent directories
    while (os.path.abspath(curr_path) != "/"):
        
        #If we have a .git entry in this directory and it refers to a directory.
        if (".git" in os.listdir(curr_path) and os.path.isdir(curr_path + "/.git")):
            return curr_path

        #Move up a directory
        curr_path = "../" + curr_path

    #If unable to find .git, print desired error and return empty path
    sys.stderr.write("Not inside a Git repository\n")
    return ""


#Function to return the branches within the parameter .git directory
def get_branches(path):
    path += "/.git/refs/heads"

    #If issue finding location of the branches, throw an error
    if (not os.path.isdir(path)):
        sys.stderr.write("No refs/heads directory within Git repository\n")
        return ""

    branch_data = dict()
    #Get all the files in the refs/heads folder
    for root, dirs, files in os.walk(path):
        #Open each file in the refs/heads folder and get the hash
        for file in files:
            opened_file = open(os.path.join(root, file), 'rb')
            branch_hash = opened_file.read().decode('utf-8')
            branch_hash = branch_hash.strip('\n')

            #Get the branch name
            branch_name = os.path.join(root, file)[len(path):]

            #If this commit hasn't been added to our dictonary, create a new entry and map it to the branch name
            if branch_hash not in branch_data.keys():
                branch_data[branch_hash] = [branch_name]

            #If this commit maps to an different branch, then add this branch to the hash's storage
            else:
                branch_data[branch_hash].append(branch_name)
    return branch_data

#Function to get the relevant commit data for the provided branch starting points
def get_commit_data(path, branch_data):
    path += "/.git/objects/"

    #Initializing return variables
    commit_data = dict()
    earliest_commits = set()

    #Loop through each of the branches
    for branch_commit in branch_data.keys():
        #If we've already looked at this commit when looking at other branches, add the branch name and move to next branch
        if branch_commit in commit_data.keys():
            commit_data[branch_commit].branches = set(branch_data[branch_commit])

        #If we haven't seen this commit before, process it
        else:
            #Create new Commit Node with hash
            commit_data[branch_commit] = CommitNode(branch_commit)

            #Add the branch name to the CommitNode
            commit_data[branch_commit].branches.extend(branch_data[branch_commit])

            #Grab earliest commits for this branch and populate commit_data with parents using depth first traversal
            branch_earliest_commits = populate_depth_first_traversal(path, branch_commit, commit_data)

            #Add the earliest commits from this branch to our storage
            earliest_commits = earliest_commits.union(branch_earliest_commits)
    
    #Sort earliest commits for consistancy
    earliest_commits = sorted(earliest_commits)
    return commit_data, earliest_commits

#Function to traverse a tree given a starting branch commit and tree structure to build upon as parameters
def populate_depth_first_traversal(path, branch_commit, commit_data):
    #Initialize commit stack with branch commit
    commit_stack = [commit_data[branch_commit]]
    earliest_commits = set()

    #While the stack is not empty, continue processing commits and adding to tree
    while (len(commit_stack) > 0):
        deepest_commit = commit_stack.pop()

        #Get parents for current commit
        commit_parents = read_commit_parents(path, deepest_commit)

        #If no parents for commit, add it to the set of earliest commits
        if (len(commit_parents) == 0):
            earliest_commits.add(deepest_commit.commit_hash)

        #If parents present, set them in our commit node
        else:
            deepest_commit.parents = commit_parents
            #Loop through parents
            for parent in commit_parents:
                #If parent is already in our commit graph, add current node to parent's children
                if parent in commit_data.keys():
                    temp = commit_data[parent].children
                    temp.add(deepest_commit.commit_hash)
                    commit_data[parent].children = set(sorted(temp))
                
                #If we haven't seen the parent before, process it
                else:
                    #Create a parent node and add the current node to it's children
                    commit_data[parent] = CommitNode(parent)
                    temp = commit_data[parent].children
                    temp.add(deepest_commit.commit_hash)
                    commit_data[parent].children = set(sorted(temp))

                    #Add the parent node to the stack to be processed next
                    commit_stack.append(commit_data[parent])

    #Sort earliest commits for consistency
    earliest_commits = sorted(earliest_commits)
    return earliest_commits

#Return the parents of a given commit hash
def read_commit_parents(path, commit):
    commit_hash = commit.commit_hash

    #Set the path of the specific commit object
    path += commit_hash[0:2] + "/" + commit_hash[2:]

    #Initialize the parents set to return
    parents = set()

    #If not able to find the commit object, then throw an error
    # if (not os.path.isfile(path)):
    #     sys.stderr.write("Expected commit object with hash: " + commit_hash +  " within Git repository \n")
    #     sys.exit(1)

    #If we can find the file, open it and decompress the result
    #else:
    compressed = open(path, 'rb').read()
    decompressed = zlib.decompress(compressed).decode("utf-8")

    #Replace line endings with a space
    decompressed = decompressed.replace("\n", " ")

    #Split the file contents on spaces
    commit_details = decompressed.split(" ")

    #Search for the string "parent" within the split file contents and store the hash(es) that immediately follows it
    for i in range(1, len(commit_details)):
        if (commit_details[i - 1] == "parent"):
            parents.add(commit_details[i])
        elif (commit_details[i] == "author"):
            break
    
    #Sort the parents for consistency
    parents = sorted(parents)
    return parents

#Perform the topological sort on the commits provided with a full commit graph and the commits to start with as parameters
def topo_sort(commit_data, earliest_commits):
    #Initialize variables for return and processing
    output = list()
    processed = dict()
    #Initializing the stack to process with the earliest nodes (such that they will be at the bottom and processed last)
    commit_stack = list(earliest_commits)

    #Looping through the stack of commits to process
    while (len(commit_stack) > 0):
        #Peek at the top of the stack and mark the node as processed
        curr_commit = commit_stack[-1]
        processed[curr_commit] = True

        #Create a list to store any unprocessed children from the current commit
        unprocessed_children = list()
        #Loop through the children of the current commit and check if they have been processed (added to the stack) yet.
        #If not, then add them to a list.
        for child in sorted(commit_data[curr_commit].children):
            if child not in processed.keys():
                unprocessed_children.append(child)
        
        #If there are still children we haven't processed, add the first of them to the list (effectively allowing
        #us to do a depth first traversal)
        if (len(unprocessed_children) > 0):
            commit_stack.append(unprocessed_children[0])

        #If this commit didn't have any children, we can add it to the output and remove it from the stack
        else:
            commit_stack.pop()
            output.append(curr_commit)

    #Return topographically sorted commits
    return output

def topo_order_commits():
    #Get desired git directory
    git_directory = discover_git_directory()
    
    #If empty directory, exit with error status 
    if (not git_directory):
        sys.exit(1)

    #Get branch information for given git directory
    branches_data = get_branches(git_directory)

    #Throw an error if issue with the branch data
    if (not branches_data):
        sys.exit(1)
    
    #Get the commit tree and list of earliest commits given the branches and the git directory
    commit_data, earliest_commits = get_commit_data(git_directory, branches_data)

    #Get a topologically sorted traversal of the git commit tree
    sorted_commits = topo_sort(commit_data, earliest_commits)

    #Assume the first commit is not sticky
    sticky = False
    
    #Loop through the sorted topologically sorted traversal
    for i in range(0, len(sorted_commits)):
        curr_commit = sorted_commits[i]

        #If we are dealing with a sticky start, write a "=", then write the children separated by whitespace
        #and a new line
        if (sticky):
            sys.stdout.write("=")
            sys.stdout.write(" ".join(sorted(commit_data[curr_commit].children)))
            sys.stdout.write("\n")
            sticky = False

        #If there are branches at the current commit, write the commit hash, followed by space separated branches
        #and a new line
        if (len(commit_data[curr_commit].branches) > 0):
            sys.stdout.write(curr_commit + " ")
            sys.stdout.write(" ".join(sorted([branch[1:] for branch in commit_data[curr_commit].branches])))
            sys.stdout.write("\n")

        #If there are no branches at the current commit, simply write the hash and a new line
        else:
            sys.stdout.write(curr_commit)
            sys.stdout.write("\n")
        
        #If we are not at the end of the topologically sorted commits, and the next commit is not a parent of 
        #the current commit, we have a sticky end. Print the parents of the current commit, followed by a "="
        #and a blank line.
        if (i < len(sorted_commits) - 1) and (sorted_commits[i + 1] not in commit_data[curr_commit].parents):
            sys.stdout.write(" ".join(sorted(commit_data[curr_commit].parents)) + "=\n\n")
            sticky = True
        

if __name__ == '__main__':
    topo_order_commits()