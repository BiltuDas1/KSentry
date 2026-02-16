import datetime


PULL_OUTDATED_UPSTREAM = """
### Your branch is outdated with `origin/{upstream_branch_name}` branch

Do the following steps to update your branch:
- Set the remote repo as upstream

  ```bash
  git remote add upstream git@github.com:{upstream_repo}.git
  ```

- Fetch the upstream for changes

  ```bash
  git fetch upstream {upstream_branch_name}
  ```

- Pull and Rebase upstream to your branch

  ```bash
  git pull upstream {upstream_branch_name} --rebase
  ```

- If Merge Conflict occurred, fix them and then run

  ```bash
  git add <conflicted_filename>
  ```

- After you have fixed all the conflicts, run

  ```bash
  git rebase --continue
  ```

- Finally, push the changes

  ```bash
  git push origin HEAD --force-with-lease
  ```
"""

PULL_OUTDATED_UPSTREAM_AGAIN = (
  "Still not updated with `origin/{upstream_branch_name}`, Please try again"
)

SECRET_FOUND = """
### Warning: Secrets found in this PR ⚠️

{secrets_data}
"""

SECRET_CODEBLOCK = """
---
**{filename}:**
```
{line_num} | {redact_code}
```
"""

SCOREBOARD = """
## 🎉 PR Successfully Merged!

Congratulations @{username}! Your contribution has been merged into the main branch. 

### 🏆 Scorecard Update
| Category | Details |
| :--- | :--- |
| **Issue Level** | {difficulty_level} |
| **Points Awarded** | `{points}` |
| **New Total Score** | **{total_score} pts** |

> [!TIP]
> **What's Next?**
> You can now pick up another issue! Remember, a single mentee can be allotted a maximum of {num_of_issues} issues at a time. Check the [Issue Board]({project_link}/issues) for more.
"""

ISSUE_MAX_ASSIGNED = """
@{username} It looks like you've reached the limit of {threadsold} active issues. Finish up your current work first so we can get it merged, then you can jump right back in here!
"""
