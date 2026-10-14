# Static Code Analysis — Issues and Fixes

**File analyzed:** `employee_payroll_system.py`  
**Tools used:** Pylint, Bandit, Flake8  
**Baseline Pylint score:** 5.32/10  
**Baseline Bandit results:** 5 findings — 2 High, 1 Medium, 2 Low

> Line numbers below refer to the original file and the baseline reports generated for this lab.

| Issue | Type / Tool | Line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Unsafe `eval()` | Security — Bandit B307; Pylint W0123 | 42 | Evaluates an expression string and may execute arbitrary code. | Replace the expression argument with a numeric deduction rate and calculate net salary directly. |
| Shell command execution | Security — Bandit B605 | 58 | `os.system()` launches a shell command assembled using the filename. | Remove the shell invocation and use `print()` for the export confirmation. |
| Weak MD5 hash | Security — Bandit B324 | 47 | MD5 is unsuitable for security-sensitive hashing. | Use SHA-256 when a cryptographic hash is required. |
| Insecure random-token generation | Security — Bandit B311 | 51 | `random.randint()` is not designed for security-sensitive tokens. | Use Python's `secrets` module to generate the token. |
| Bare exception with `pass` | Code quality/security — Bandit B110; Pylint W0702; Flake8 E722 | 26–27 | Suppresses errors without distinguishing expected failures from programming errors. | Validate inputs and return a failure result for invalid employee IDs or penalties; avoid broad exception handling. |
| Mutable default argument | Code quality — Pylint W0102 | 15 | `transaction_logs=[]` can reuse the same list across function calls. | Use `None` as the default and initialize a list inside the function when needed. |
| Unused import | Code quality — Pylint W0611; Flake8 F401 | 6 | `math` is imported but not used. | Remove the unused import. |
| Unused variable | Code quality — Pylint W0612; Flake8 F841 | 31 | `statutory_buffer` is assigned but never used. | Remove it unless it has a defined business purpose. |
| Unused variable | Code quality — Pylint W0612; Flake8 F841 | 41 | `base` is assigned but the result is calculated using `eval()` instead. | Replace `eval()` with a direct calculation that uses the salary value. |
| File handling | Code quality — Pylint W1514, R1732 | 55–56 | File is opened without explicit encoding and manually closed. | Use `with open(filename, "w", encoding="utf-8") as file:`. |
| `None` comparison | Code quality — Pylint C0121; Flake8 E711 | 32 | Uses `== None` rather than an identity comparison. | Use `is None`. |
| Naming convention | Style — Pylint C0103 | 15 | `processSalary` does not follow Python's snake_case convention. | Rename it to `process_salary`. |
| Missing function docstrings | Documentation — Pylint C0116 | Multiple | Several functions do not describe their purpose. | Add a short docstring to each function. |
| Old-style string formatting | Style — Pylint C0209 | 19 | Uses `%` formatting where an f-string is appropriate. | Replace with an f-string. |
| Line too long | Style — Flake8 E501 | 19 | The line is 84 characters, exceeding Flake8's 79-character default. | Split the statement across lines. |
| Missing final newline | Style — Pylint C0304; Flake8 W292 | End of file | The file does not end with a newline. | Add a newline at the end of the file. |

## Verification status

The baseline findings above are taken from the initial reports. After applying fixes, rerun all three tools and record the actual results here:

- **Pylint after fixes:** ____________________
- **Bandit after fixes:** ____________________
- **Flake8 after fixes:** ____________________

Do not mark an issue as resolved until the after-fix reports confirm it.
