```markdown
# Major-OS-AMA-OS--Command Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches you the core development patterns and conventions used in the `Major-OS-AMA-OS--Command` TypeScript codebase. You'll learn how to structure files, write imports/exports, and follow the repository's coding and testing standards. This guide also provides step-by-step workflows and suggested commands for common development tasks.

## Coding Conventions

### File Naming
- Use **snake_case** for all file names.
  - Example:  
    ```
    command_handler.ts
    user_input_parser.ts
    ```

### Import Style
- Use **relative imports** for referencing other modules.
  - Example:
    ```typescript
    import { parse_input } from './input_parser';
    ```

### Export Style
- Use **named exports** for all exported functions, classes, or constants.
  - Example:
    ```typescript
    export function execute_command() { ... }
    export const COMMAND_LIST = [ ... ];
    ```

### Commit Messages
- Freeform style; no strict prefixes.
- Average commit message length: ~40 characters.
  - Example:
    ```
    Add support for new command syntax
    ```

## Workflows

### Adding a New Command
**Trigger:** When you need to introduce a new command to the system  
**Command:** `/add-command`

1. Create a new file using snake_case (e.g., `my_new_command.ts`).
2. Implement the command logic using named exports.
    ```typescript
    export function my_new_command(args: string[]) {
      // Command logic here
    }
    ```
3. Import your command in the main command registry using a relative import.
    ```typescript
    import { my_new_command } from './my_new_command';
    ```
4. Add your command to the command list or handler.
5. Write a corresponding test file (e.g., `my_new_command.test.ts`).

### Running Tests
**Trigger:** When you want to verify code correctness  
**Command:** `/run-tests`

1. Identify test files by the `*.test.*` pattern (e.g., `command_handler.test.ts`).
2. Use the project's test runner (framework unknown; check project docs or scripts).
3. Run all tests and review output for failures.

### Refactoring a Module
**Trigger:** When improving or restructuring existing code  
**Command:** `/refactor-module`

1. Locate the module file (e.g., `old_module.ts`).
2. Rename or split files using snake_case.
3. Update all relative imports referencing the module.
4. Ensure all exports remain named.
5. Update or add tests as needed.
6. Commit changes with a clear, concise message.

## Testing Patterns

- Test files use the `*.test.*` naming convention.
  - Example: `user_input_parser.test.ts`
- Testing framework is not specified; check project scripts or documentation.
- Place tests alongside or near the modules they test.
- Example test file structure:
  ```typescript
  import { parse_input } from './input_parser';

  describe('parse_input', () => {
    it('should parse valid input', () => {
      // test logic
    });
  });
  ```

## Commands
| Command         | Purpose                                         |
|-----------------|-------------------------------------------------|
| /add-command    | Scaffold and register a new command module      |
| /run-tests      | Run all tests in the codebase                   |
| /refactor-module| Refactor or restructure an existing module      |
```