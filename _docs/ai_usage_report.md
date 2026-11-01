# AI Usage & Methodology Report: Building an Agentic DevOps Workflow

This was my first project working with agents. I let the agents generate absolutely everything, including documentation. The information below was produced when I asked the agent to summarize how we had been working together. I did some minor editing for accuracy. 

## 1. Token Management
* **Atomic Tasks:** Breaking work into single-issue tickets keeps context windows clean and stops tokens from burning on irrelevant history.
* **Targeted Files:** Agents only load the specific files needed for the active task instead of pulling in the whole repo.

## 2. Setting Boundaries Between Roles
* **Separation of Duties:** PM and engineering roles have strict limits. The PM agent doesn't look at raw code, keeping it focused entirely on specs and tickets.
* **Clear Job Descriptions:** Keeping roles distinct prevents the planning and coding phases from bleeding together into a mess.

## 3. Keeping Strategy and Execution Separate
* **Using the Web UI for Planning:** High-level planning and prompt testing happen in the web interface. Since it can't touch your local files, it's a safe sandbox for iteration.
* **Using the Terminal for Coding:** Validated prompts move to the containerized terminal for actual work, keeping you in full control of the codebase.

## 4. Retrospective: What To Do Differently
1. **Upfront Constraints:** Put tool rules (`uv`, shell paths) into root instructions immediately to stop agents from falling back to old habits. 
2. **Better Roles, Earlier:** Docs, tests, and code each need specialized handling, and agents produce much better work when given tight, explicit directions from the start. Enforcing strict role rules for both documentation and code right out of the gate would cut down on wasted iteration loops.