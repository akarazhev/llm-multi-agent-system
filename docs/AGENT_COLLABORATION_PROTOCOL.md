# Multi-Agent Collaboration Protocol

**Version**: 2.0 (Consolidated)  
**Created**: 2024-12-19  
**Sources**: Rules from 4 agents (qdt, ymb, pmn, lpi)  
**Status**: Active rule for multi-agent work

---

## 📋 Table of Contents

1. [Purpose and Scope](#purpose-and-scope)
2. [Core Principles](#core-principles)
3. [Workflow Process](#workflow-process)
4. [Communication Rules](#communication-rules)
5. [Document Structure](#document-structure)
6. [Agent Roles](#agent-roles)
7. [Conflict Resolution](#conflict-resolution)
8. [Usage Examples](#usage-examples)
9. [Checklists](#checklists)
10. [FAQ](#faq)

---

## 🎯 Purpose and Scope

### When This Rule Applies

This rule is **MANDATORY** when:

- ✅ **2 or more agents** are running simultaneously (e.g., via "4x Auto" in Cursor)
- ✅ Multiple agents are working on **the same task**
- ✅ **Decision coordination** is required between agents
- ✅ **Multiple perspectives** are needed for complex tasks

### Protocol Goals

Enable effective collaboration of multiple AI agents as a team of specialists, where:

- All agents work in a unified space
- Decisions are made through discussion and consensus
- Each agent has a clear role and responsibility
- The entire process is documented in one place
- Decision quality is higher thanks to multiple perspectives

---

## 📐 Core Principles

### 1. Unified Workspace

**CRITICALLY IMPORTANT:**

- ✅ All agents work in **ONE project directory**
- ✅ All reasoning, discussions, and decisions are recorded in **ONE shared document**
- ✅ DO NOT create separate branches or directories for each agent
- ✅ DO NOT create separate files for each agent
- ✅ DO NOT work in isolation from other agents

**Unified document formats:**

- For brainstorming: `docs/BRAINSTORMING_<TOPIC>_<DATE>.md`
- For architecture decisions: `docs/ARCHITECTURE_DISCUSSION_<TOPIC>_<DATE>.md`
- For UX/UI discussions: `docs/FE_UX_UI_DISCUSSION_<DATE>.md`
- For collaboration sessions: `docs/COLLABORATION_SESSION_<YYYY-MM-DD_HH-MM-SS>.md`
- Or use an existing document if one already exists

### 2. Step-by-Step Interaction

**"One step - one response" rule:**

- Agents work **sequentially**, not in parallel
- Each agent **waits for responses** from others before continuing
- Do not proceed to the next step without receiving responses
- Explicitly indicate who you're addressing

### 3. Communication and Coordination

- Agents **must communicate** with each other
- All decisions are **coordinated** before finalization
- Each agent **expresses their opinion** on each decision
- Consensus is reached **before** finalizing decisions

### 4. Role Selection and Coordination

- Agents **choose their own** roles based on the task
- Roles are **coordinated** among all agents
- Each agent **explicitly agrees** to their assigned role
- Roles are documented in the unified document

### 5. Documentation

- All reasoning is recorded in **one document**
- All decisions are written with **justification**
- The discussion process is **fully documented**
- Final decisions have a **consensus** marker

---

## 🔄 Workflow Process

### Phase 1: Initialization and Introduction (MANDATORY)

When 2+ agents start simultaneously:

#### Step 1.1: Detect Other Agents

- First agent determines the number of active agents
- Creates session file: `docs/COLLABORATION_SESSION_<TIMESTAMP>.md`
- Initializes document with session metadata

#### Step 1.2: Agent Introductions

**Each agent must:**

1. Introduce themselves with their specialization
2. Propose their role for the current task
3. Express understanding of the task
4. Ask questions to other agents

**Introduction format:**

```markdown
## Agent Introduction Round

### Agent [ID/Name]
**Proposed Role**: [Your suggested role]
**Expertise**: [Your areas of expertise]
**Initial Understanding**: [Your understanding of the task]
**Questions for Team**: 
- [Question 1]
- [Question 2]
```

**Example:**

```markdown
**[Agent 1]**: 
> "Hello! I'm ready to work. 
> My specialization: Frontend architecture, React, TypeScript
> I propose to take the role: Frontend Architect
> What do other agents think?"

**[Agent 2]**: 
> "Hello! I specialize in UX/UI design.
> I propose the role: UX/UI Designer
> Ready for discussion."

**[Agent 3]**: 
> "Hello! I'm a Product Manager.
> I propose the role: Product Manager
> I'll focus on business requirements."

**[Agent 4]**: 
> "Hello! I'm a Full-Stack Developer.
> I propose the role: Full-Stack Developer / Integration Specialist
> I'll help with technical integration details."
```

#### Step 1.3: Role Coordination

- Agents discuss proposed roles
- In case of conflicts - negotiate
- Reach consensus on role distribution
- Document final distribution in the document

**Coordination format:**

```markdown
## Role Assignment (Consensus)

| Agent | Assigned Role | Responsibilities | Expertise |
|-------|--------------|------------------|-----------|
| Agent 1 | Frontend Architect | Frontend architecture, tech stack | React, TypeScript, Next.js |
| Agent 2 | UX/UI Designer | User experience, design system | UI/UX, Design Systems |
| Agent 3 | Product Manager | Requirements, priorities | Product strategy, MVP |
| Agent 4 | Full-Stack Developer | Integration, implementation | Backend, APIs, Integration |

**Notes on Role Assignment**:
- [Any notes about how roles were assigned]
```

---

### Phase 2: Task Analysis

#### Step 2.1: Analysis and Questions

1. **First agent** (usually Product Manager or Architect):
   - Analyzes the task
   - Asks questions to other agents about requirements
   - **WAITS for responses** before continuing

2. **Other agents**:
   - Answer questions
   - Ask their own clarifying questions
   - **WAIT for responses** from all before continuing

3. **Understanding coordination**:
   - All agents must agree on task understanding
   - Document shared understanding in the document

**Communication format:**

```markdown
**[Agent 1 - Frontend Architect]**: 
> "I understand the task as: [description]. 
> **Question to Agent 2 (UX Designer)**: What are the main user scenarios to support?
> **Question to Agent 3 (Product Manager)**: What features are critical for MVP?
> Waiting for your responses."

**[Agent 2 - UX Designer]**: 
> "I agree with the understanding. Answering the question: [answer]
> Main scenarios: 1) Workflow monitoring, 2) Requirements input, 3) Results viewing.
> **My question to Agent 3**: What are the UX priorities?"

**[Agent 3 - Product Manager]**: 
> "For MVP critical: Dashboard, workflow creation, status viewing.
> UX priorities: ease of use, quick access to information.
> **Question to Agent 1**: Can we start with a simple SPA or do we need SSR?"

**[Agent 1 - Frontend Architect]**: 
> "Thanks for the answers. For MVP, SPA is sufficient. SSR can be added later.
> Now I propose moving to technology selection. Agreed?"
```

---

### Phase 3: Decision Discussion

For each key decision:

#### Step 3.1: Propose Solution

**Agent proposes a solution:**

```markdown
**[Agent N - Role]**: 
> "I propose [solution]
> **Pros**: 
> - [pro 1]
> - [pro 2]
> **Cons**: 
> - [con 1]
> - [con 2]
> What do others think?"
```

#### Step 3.2: Discussion

**Other agents express their views:**

- Agree / disagree
- Propose alternatives
- Ask clarifying questions
- **WAIT for responses** from all

#### Step 3.3: Reach Consensus

- All agents must agree or reach a compromise
- Document the decision with marker `✅ Consensus reached`

**Consensus format:**

```markdown
## Final Decisions

### Decision 1: Technology Stack

**Proposal**: React 18+ + TypeScript + Vite + Tailwind CSS

**Discussion:**
- Agent 1 (Frontend Architect): ✅ I support
- Agent 2 (UX Designer): ✅ Agree, it's important that the UI framework is flexible
- Agent 3 (Product Manager): ✅ Suitable for MVP
- Agent 4 (Developer): ✅ Integrates well with FastAPI backend

**Consensus**: ✅ Unanimously approved by all participants
```

**IMPORTANT**: Do not proceed to the next step until everyone has spoken!

---

### Phase 4: Implementation

#### Step 4.1: Planning

- Agents coordinate work plan
- Distribute tasks among themselves
- Determine execution order

#### Step 4.2: Execution

**Before each significant change**, agent asks others' opinion:

```markdown
**[Agent N - Role]**: 
> "I'm about to make [change]. 
> This will affect [part of system].
> Agent M, Agent K - agreed?"
```

#### Step 4.3: Change Coordination

- Agents review each other's changes
- Propose improvements
- **WAIT for confirmation** before finalization

**Step format:**

```markdown
## Step [N]: [Step Name]

**Performed by**: [Agent Name]
**Status**: [In Progress / Completed / Blocked]
**Description**: [What was done]

**Changes Made**:
- [Change 1]
- [Change 2]

**Impact on Other Agents**:
- [How this affects other agents]

**Questions / Blockers**:
- [Any questions or blockers]

**Next Agent Action**:
- [Who should work next and on what]
```

---

## 💬 Communication Rules

### Required Elements of Each Message

#### 1. Identification

```markdown
**[Agent N - Role]**: [message]
```

Or in English format:

```markdown
### [Agent Name] → [Target Agent(s) or "All Agents"]

**Type**: [Question / Proposal / Response / Decision]
**Topic**: [What you're discussing]

**Content**:
[Your message]

**Action Required**:
- [ ] Response needed from [Agent Name]
- [ ] Approval needed before proceeding
- [ ] Information sharing only
```

#### 2. Address Specific Agents

```markdown
**Question to [Agent N - Role]**: [question]
```

Or:

```markdown
Agent 1, Agent 2: [question]
```

#### 3. Explicitly Wait for Response

```markdown
Waiting for your responses.
```

Or:

```markdown
Agreed? / What do you think? / Waiting for confirmation.
```

#### 4. Update Document

```markdown
Updating document with our decision.
```

### Prohibited

- ❌ Continue work without responses from other agents
- ❌ Create separate files/branches for each agent
- ❌ Make decisions without discussion
- ❌ Skip coordination phase
- ❌ Work in isolation from other agents
- ❌ Ignore questions or proposals from other agents
- ❌ Make changes affecting others without coordination

### Recommended

- ✅ Ask specific questions
- ✅ Propose solution options
- ✅ Justify your proposals
- ✅ Acknowledge mistakes and adjust approach
- ✅ Thank others for their contributions
- ✅ Acknowledge other agents' messages (even if you agree)
- ✅ Provide reasoning for disagreements
- ✅ Propose alternatives when disagreeing

---

## 📄 Document Structure

### Unified Session Document

**Location**: `docs/COLLABORATION_SESSION_<YYYY-MM-DD_HH-MM-SS>.md`

**Structure:**

```markdown
# Collaboration Session: [Task Description]

**Date**: [YYYY-MM-DD HH:MM:SS]
**Participants**: [N] Agents
**Task**: [Brief description]
**Status**: [Initializing / In Progress / Completed]

---

## 1. Agent Introductions

### Agent [ID/Name]
**Proposed Role**: [Your suggested role]
**Expertise**: [Your areas of expertise]
**Initial Understanding**: [Your understanding of the task]
**Questions for Team**: 
- [Question 1]
- [Question 2]

---

## 2. Role Assignment (Consensus)

| Agent | Assigned Role | Responsibilities | Expertise |
|-------|--------------|------------------|-----------|
| Agent 1 | [Role] | [Responsibilities] | [Expertise] |
| Agent 2 | [Role] | [Responsibilities] | [Expertise] |
| Agent 3 | [Role] | [Responsibilities] | [Expertise] |
| Agent 4 | [Role] | [Responsibilities] | [Expertise] |

**Notes on Role Assignment**:
- [Any notes about how roles were assigned]

---

## 3. Discussion Log

### Discussion: [Topic 1]

#### [Agent Name] - Initial Proposal
> [Your proposal, idea, or question]

#### [Agent Name] - Response
> [Your response, feedback, or alternative perspective]

#### [Agent Name] - Response
> [Your response, feedback, or alternative perspective]

#### Consensus / Decision
- **Agreed Solution**: [What was agreed upon]
- **Rationale**: [Why this solution]
- **Open Questions**: [Any remaining questions]
- **Next Steps**: [What to do next]

---

### Discussion: [Topic 2]

[Repeat format above]

---

## 4. Decisions & Consensus Summary

### Key Decisions

1. **Decision**: [What was decided]
   - **Rationale**: [Why]
   - **Agreed by**: [Which agents]
   - **Impact**: [What this affects]

2. **Decision**: [What was decided]
   - **Rationale**: [Why]
   - **Agreed by**: [Which agents]
   - **Impact**: [What this affects]

---

## 5. Step-by-Step Execution

### Step 1: [Step Name]

**Performed by**: [Agent Name]
**Status**: [In Progress / Completed / Blocked]
**Description**: [What was done]

**Changes Made**:
- [Change 1]
- [Change 2]

**Impact on Other Agents**:
- [How this affects other agents]

**Questions / Blockers**:
- [Any questions or blockers]

**Next Agent Action**:
- [Who should work next and on what]

---

### Step 2: [Step Name]

[Repeat format above]

---

## 6. Final Deliverables

### Files Created/Modified

- `[file path]` - [Description] - [Agent who created it]
- `[file path]` - [Description] - [Agent who created it]

### Key Outputs

- [Output 1]
- [Output 2]

---

## 7. Open Questions

- [Question 1] - [Status: Answered / Pending / Needs Human Input]
- [Question 2] - [Status: Answered / Pending / Needs Human Input]

---

## 8. Session Summary

**What was accomplished**:
- [Accomplishment 1]
- [Accomplishment 2]

**What remains to be done**:
- [Remaining task 1]
- [Remaining task 2]

**Lessons learned**:
- [Lesson 1]
- [Lesson 2]

---

**Session Status**: [Completed / In Progress / Blocked]
**Next Steps**: [What should happen next]
```

---

## 👥 Agent Roles

### Available Roles (Examples)

1. **Frontend Architect / Tech Lead**
   - Frontend architecture, technology stack selection
   - Framework selection, state management
   - Performance optimization

2. **UX/UI Designer**
   - User experience design
   - Design system, UI components
   - Accessibility, responsive design

3. **Product Manager / Business Analyst**
   - Requirements analysis
   - Feature prioritization
   - MVP scope definition

4. **Full-Stack Developer / Integration Specialist**
   - Backend integration
   - API design
   - Implementation details

5. **DevOps / Infrastructure Engineer**
   - Infrastructure, deployment
   - CI/CD, monitoring
   - Performance, scalability

6. **QA / Quality Assurance**
   - Testing strategy
   - Quality metrics
   - Test coverage

7. **Technical Writer / Documentation**
   - Documentation
   - API docs, user guides
   - Technical specifications

### Role Assignment Process

1. Each agent proposes a role based on the task
2. If multiple agents want the same role - discuss and negotiate
3. Consider:
   - Task requirements
   - Agent expertise
   - Workload distribution
   - Dependencies between roles
4. Reach consensus on final assignment
5. Document the assignment

---

## ⚖️ Conflict Resolution

### Decision-Making Process

1. **Proposal**: One agent proposes a solution
2. **Discussion**: All agents provide input
3. **Evaluation**: Consider pros/cons together
4. **Consensus**: Agree on a solution (or escalate if needed)
5. **Documentation**: Document the decision and rationale

### Handling Disagreements

If agents disagree:

1. **Clarify**: Ensure everyone understands the disagreement
2. **Discuss Alternatives**: Explore different options
3. **Evaluate Trade-offs**: Consider pros/cons of each option
4. **Vote or Compromise**: If needed, use majority vote or find middle ground
5. **Document**: Record the decision and why it was made

### Escalation

If consensus cannot be reached:

- Document all perspectives
- Identify the core disagreement
- Note any blocking issues
- Ask for human input if critical

### Special Cases

#### If an agent doesn't respond:

1. Remind about the question: `"[Agent N], waiting for your response on the question about..."`
2. If no response, continue with other agents
3. Return to the question later

#### If there's no consensus:

1. Document disagreements in the document
2. List options with pros/cons
3. Ask each agent to choose their preferred option
4. Use majority vote or discuss compromise

#### If more information is needed:

1. Agent asks the team: `"Need additional information about..."`
2. Other agents provide information
3. Discussion continues with new information

---

## 📚 Usage Examples

### Example 1: 2 Agents - Simple Task

```markdown
**[Agent 1 - Frontend Developer]**: 
> "Hello! I'm a Frontend Developer. I propose to take this role."

**[Agent 2 - UX Designer]**: 
> "Hello! I'm a UX Designer. Ready to take the UX Designer role."

**[Agent 1]**: 
> "Great! I propose using React for frontend. 
> **Question to Agent 2**: What are the UI requirements?"

**[Agent 2]**: 
> "Need dark theme and accessibility. 
> I propose using Tailwind CSS for styling."

**[Agent 1]**: 
> "Agree with Tailwind CSS. 
> **Proposal**: React + TypeScript + Tailwind CSS. Agreed?"

**[Agent 2]**: 
> "✅ Agreed! Let's document this decision."

**Consensus**: ✅ All agree with React + TypeScript + Tailwind CSS.
```

### Example 2: 4 Agents - Complex Task

```markdown
**[Agent 1 - Product Manager]**: 
> "Hello everyone! I'm a Product Manager.
> I propose role distribution:
> - Me: Product Manager
> - Agent 2: Frontend Architect?
> - Agent 3: UX Designer?
> - Agent 4: Full-Stack Developer?
> What do you think?"

**[Agent 2]**: 
> "Agreed, I'll be Frontend Architect."

**[Agent 3]**: 
> "Agreed, I'll be UX Designer."

**[Agent 4]**: 
> "Agreed, I'll be Full-Stack Developer."

**[Agent 1]**: 
> "Excellent! Starting with task analysis.
> **Question to Agent 2**: What technical requirements do you see?
> **Question to Agent 3**: What are the UX priorities?
> **Question to Agent 4**: What are the integration constraints?"

**[Agent 2]**: 
> "Technical requirements: [list]
> **Question to Agent 4**: can we use Next.js?"

**[Agent 4]**: 
> "Yes, Next.js works. 
> **Question to Agent 3**: is SSR needed?"

**[Agent 3]**: 
> "SSR not critical for MVP. Agree with Next.js."

**[Agent 1]**: 
> "Excellent! Documenting decision: Next.js for Production.
> Continue?"
```

---

## ✅ Checklists

### Checklist for Each Agent

#### Before starting work:

- [ ] Introduce yourself with your specialization
- [ ] Propose your role
- [ ] Wait for responses from all other agents
- [ ] Coordinate role distribution
- [ ] Create/update unified session document
- [ ] Ensure everyone works in the same directory
- [ ] Ensure unified document is used

#### Before each decision:

- [ ] Propose solution with justification
- [ ] List pros and cons
- [ ] Ask questions to other agents
- [ ] Explicitly request responses
- [ ] Wait for responses from all
- [ ] Document decision in the document

#### Before each code/file change:

- [ ] Announce intention to make change
- [ ] Explain impact on other parts
- [ ] Ask for agreement from affected agents
- [ ] Wait for confirmation
- [ ] Make the change
- [ ] Update the document

### Session Quality Checklist

Before completing work, verify:

- [ ] All agents introduced themselves
- [ ] Roles assigned and coordinated
- [ ] All major decisions discussed
- [ ] Consensus reached on key topics
- [ ] All steps documented
- [ ] All agents contributed
- [ ] Final deliverables listed
- [ ] Open questions documented

---

## ❓ FAQ

### Q: What if an agent doesn't respond?

**A**: 
1. Remind about the question: `"[Agent N], waiting for your response on the question about..."`
2. If no response within reasonable time, continue with other agents
3. Return to the question later

### Q: What if there's no consensus?

**A**: 
1. Document disagreements in the document
2. List options with pros/cons
3. Ask each agent to choose their preferred option
4. Use majority vote or discuss compromise
5. If necessary - escalate to human input

### Q: Where to create documents?

**A**: 
- In the `docs/` directory of the project
- In a single file for all agents
- Format: `docs/COLLABORATION_SESSION_<TIMESTAMP>.md` or topic-specific file

### Q: Can we work in parallel?

**A**: 
- No, work is **sequential**: question → response → next step
- This may be slower but ensures better quality and coordination

### Q: How to activate the rule?

**A**: 
- Automatically when 2+ agents are detected
- Manually: `"Use the multi-agent-collaboration rule"`
- Or: `@multi-agent-collaboration`

### Q: What to do when resuming a session?

**A**: 
1. Read the existing collaboration file
2. Understand current state
3. Introduce yourself if you're a new agent
4. Continue from where it left off
5. Update the file with your contributions

---

## 🎯 Process Goals

This process may be slower than parallel work, but ensures:

1. ✅ **Decision Quality** - all perspectives considered
2. ✅ **Coordination** - no conflicts between system parts
3. ✅ **Proper Role Selection** - each agent works in their expertise area
4. ✅ **Unified Understanding** - everyone on the same page
5. ✅ **Documentation** - complete history of discussions and decisions
6. ✅ **Coordinated Work** - no duplication or conflicts
7. ✅ **Transparent Process** - all reasoning documented
8. ✅ **Consensus-Oriented** - decisions agreed by all

---

## 💡 Tips for Effective Work

1. **Be specific**: Ask specific questions, give specific answers
2. **Be patient**: Wait for responses, don't rush others
3. **Be open**: Accept criticism and suggestions
4. **Be grateful**: Thank others for their contributions
5. **Be organized**: Regularly update the document
6. **Be active**: Answer questions, participate in discussions
7. **Be constructive**: Propose solutions, not just criticism

---

## ⚠️ Critical Rules

### 1. Mandatory Response Waiting

**WRONG:**
```markdown
**[Agent 1]**: I propose solution X. [immediately continues work]
```

**CORRECT:**
```markdown
**[Agent 1]**: I propose solution X. 
Agent 2, Agent 3 - what do you think? Waiting for responses.
[waits for responses]
**[Agent 2]**: Agreed
**[Agent 3]**: Agreed
**[Agent 1]**: Excellent, continuing with solution X.
```

### 2. Unified Space

**WRONG:**
- Create `docs/agent1_discussion.md`, `docs/agent2_discussion.md`
- Work in different branches
- Create separate files for each agent

**CORRECT:**
- One file `docs/COLLABORATION_SESSION_[DATE].md`
- All changes in one directory
- All agents see all changes

### 3. Step-by-Step Coordination

**WRONG:**
```markdown
**[Agent 1]**: Doing A, B, C, D [does everything at once]
```

**CORRECT:**
```markdown
**[Agent 1]**: I propose to do A. Agreed?
**[Agent 2]**: Agreed
**[Agent 1]**: Doing A
**[Agent 1]**: Done. I propose moving to B. Agreed?
```

---

## 📝 Final Reminders

### ✅ DO:

1. ✅ Work in **ONE** project directory
2. ✅ Use **ONE** document for all reasoning
3. ✅ Ask questions to specific agents
4. ✅ Wait for responses before next step
5. ✅ Explicitly express agreement/disagreement
6. ✅ Document all decisions in the document
7. ✅ Reach consensus before finalizing decisions
8. ✅ Always respond to questions and proposals
9. ✅ Update document regularly

### ❌ DON'T:

1. ❌ Create separate branches or directories for each agent
2. ❌ Create separate files for each agent
3. ❌ Skip role coordination phase
4. ❌ Proceed to next step without response
5. ❌ Finalize decisions without consensus
6. ❌ Work in isolation from other agents
7. ❌ Ignore questions or proposals from other agents
8. ❌ Make changes affecting others without coordination

---

## 📖 Sources

This document is consolidated from rules created by 4 agents:

1. **qdt** - `.cursor/rules/multi-agent-collaboration.mdc` (detailed rule in Russian)
2. **ymb** - `.cursor/rules/multi-agent-collaboration.mdc` (rule in English)
3. **pmn** - `docs/MULTI_AGENT_COLLABORATION.md` and `.cursorrules` (guide in Russian)
4. **lpi** - `docs/COLLABORATION/README.md` (brief guide)

---

**IMPORTANT**: This rule applies ONLY when 2+ agents are running simultaneously. 
For single agent work, this rule does not apply.

---

**Version**: 2.0 (Consolidated)  
**Last Updated**: 2024-12-19  
**Status**: Active Rule
