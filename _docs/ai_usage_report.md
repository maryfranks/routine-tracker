# AI Usage & Methodology Report: Building an Agentic DevOps Workflow

This was my first project working with agents. I let the agents generate absolutely everything, including documentation. I worked entirely with gemini and used the lite model. For a first project to learn about agents, I deliberately chose the `nearly free` approach. The lite model did take a long time and didn't write the best code but the quality of code was not as important as the experience working with agents. I have an app that functions the way that I expect and I was really impressed that the agent was able to do that. 

I losely followed a couple of tutorials for this project. The goal was to define specialized agent instructions and allow the agents to do their prescribed jobs with little to no intervention by me. I both love and hate this process. The code is kind of impossible to look at (one of the tutorials notes its hard to look at agent generated code because he has "opinions about code" that claude doesn't share and I found that very relatable). I want to find a way to make it write more human readable and less verbose code going forward. The documentation is overly verbose and not as informative as I would have liked. I wonder if the agents measure productivity by how many lines they add. I deliberately left it so that I have a benchmark to come back to after I've learned how to work better with agents. 

Agents don't seem terribly concerned with consitency either. I want to develop more templates and get some useful skills in my repositories. The roles I defined were not as effective as I wanted, more research on how other people handle them is necessary. I plan to develop more carefully curated roles for the next project and to take note of repetitive prompting so that I can make more skills. 

The information below was produced when I asked the agent to summarize how we had been working together. I did some minor editing for accuracy. 

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
1. **Upfront Constraints:** Put tool rules (e.g. `uv`, shell paths) into root instructions immediately to stop agents from falling back to old habits. 
2. **Better Roles, Earlier:** Docs, tests, and code each need specialized handling, and agents produce much better work when given tight, explicit directions from the start. Enforcing strict role rules for both documentation and code right out of the gate would cut down on wasted iteration loops.