# Static Code Analysis — Reflection

## 1. What is static code analysis, and why is it useful?

Static code analysis examines source code without running the program. In this lab, Pylint checked code quality and potential programming problems, Flake8 checked style and formatting, and Bandit identified potentially insecure coding patterns. These tools helped identify issues that might otherwise be missed during a normal run.

## 2. What were the main issues found in the original program?

The original payroll program had unsafe use of `eval()`, shell command execution through `os.system()`, MD5 hashing, and token generation using the standard `random` module. It also had a mutable default argument, a bare `except`, unused variables and imports, manual file closing, naming problems, and formatting issues. The baseline Pylint score was 5.32/10, and Bandit reported five findings: two high, one medium, and two low severity.

## 3. Which issues were most important to fix, and why?

The security findings were the highest priority. `eval()` can execute unintended code, and building a shell command can expose the program to command injection. MD5 is not appropriate for security-sensitive hashing, and `random` is not intended for security tokens. These were addressed before lower-risk style improvements.

## 4. How did the fixes improve the code?

The revised implementation replaces expression evaluation with a controlled numeric calculation, removes the shell command, uses SHA-256 for hashing, and uses `secrets` for token generation. It also avoids the mutable default list, validates penalty inputs, uses a context manager and explicit UTF-8 encoding for file output, removes unused code, and improves naming, documentation, and formatting.

## 5. What did you learn from using Pylint, Bandit, and Flake8?

I learned that different static-analysis tools focus on different aspects of a program. Pylint highlights code quality and maintainability issues, Bandit focuses on security risks, and Flake8 reports style and formatting violations. Running all three gives a broader review than relying on one tool alone.

## 6. What are the limitations of static code analysis?

Static analysis can identify suspicious patterns, but it cannot prove that a program is completely correct or secure. Some findings require human judgment, and tools may not understand the application's intended business rules. For that reason, static analysis should be combined with tests, code review, and careful validation of inputs and outputs.

## 7. How did you verify the fixes?

After modifying the source, I reran Pylint, Bandit, and Flake8 and reviewed their reports. The final scores and remaining findings should be recorded only after those commands have completed successfully.

- **Pylint after fixes:** ____________________
- **Bandit after fixes:** ____________________
- **Flake8 after fixes:** ____________________
