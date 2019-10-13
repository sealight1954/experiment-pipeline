# Overview

## Coordinator
- coordinator.py
    - parallel executor of multiple sequential run
- bash_coordinator.py
    - parallel executor of bash scripts
- pipeline coordinator
    - pipeline which represents following:
        ```
        task 1
            task 1-1 depends on task 1
            task 1-2 depends on task 1
        task 2 depends on task 1-1, 1-2
            task 2-1
            task 2-2
        ```