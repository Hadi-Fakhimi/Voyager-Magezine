# 🚀 Voyager Magazine

Welcome to the **Voyager Magazine** repository.

This repository contains all source materials, graphical outputs, and code samples related to the Voyager Magazine project.

---

# 📂 Repository Structure

The repository is divided into **three main sections**.

## 1. `docs`

This directory contains the **raw source files** of the magazine.

* Each chapter has its own dedicated folder.
* The content of every chapter is written as **Markdown (`.md`) files**.
* Topics and file organization must follow the tasks and headings defined in **Jira**.
* After completing your assigned content, push only the corresponding Markdown files into the appropriate chapter directory.

Example structure:

```text
docs/Web
├── RESTful API/
│   ├── restfull-api-1-1.md
│   ├── restfull-api-1-2.md
│   └── ...
├── HTTP/
├── Rate Limiting/
└── ...
```

---

## 2. `design-output`

This directory contains the **graphical design outputs** of each chapter.

When the visual design of a chapter is completed, the generated assets should be placed inside the corresponding chapter folder in this directory.

Example:

```text
design-output/
├── RESTful API/
├── HTTP/
└── ...
```

---

## 3. `code-sample`

This directory contains all code samples referenced throughout the magazine.

Each chapter should have its own folder containing the related source code.

Example:

```text
code-sample/Web
├── RESTful API/
├── HTTP/
└── ...
```

---

# 📝 File Naming Convention

Use descriptive and consistent file names.

Example:

```text
<chapter-name>/restfull-api-1-1.md
```
---

# 🌿 Git Workflow

Please follow these rules carefully before pushing any changes.

## Always Pull Before Push

Before every push:

```bash
git pull
```

Then push your changes:

```bash
git push
```

This reduces the chance of merge conflicts.

---

## Only Modify Your Assigned Section

Each contributor is responsible **only** for the section assigned to them.

* Do **not** modify files belonging to other contributors.
* Do **not** rename unrelated files.
* Do **not** move unrelated files.
* Do **not** reformat files outside your assigned section.

Even the smallest unnecessary modification may create repository conflicts.

---

## Markdown Files Only

Only upload files with the `.md` extension to the `docs` directory.

Uploading unrelated file types is **not allowed**.

If unrelated files are uploaded:

* They will be removed from the repository.
* The contributor responsible will be contacted and the issue will be addressed according to the project guidelines.

---

# 📚 Magazine Chapters

| Date                     | Chapter                        |
| ------------------------ | ------------------------------ |
| 8 – 23 July              | Web                            |
| 23 – 30 July             | Cybersecurity                  |
| 31 July – 7 August       | Hardware                       |
| 8 – 25 August            | AI                             |
| 26 August – 9 September  | Programming                    |
| 10 – 24 September        | GD                             |
| 25 September – 2 October | DevOps                         |
| Not Set                  | Where Technology and Art Meets |

---
# 🏷️ Contributor Badges Used on Top of Paper Works

The following badges identify contributors and the type of contribution made to each paper:

![Writer](https://img.shields.io/badge/Writer-Hadi_Fakhimi-blue)
![Writer](https://img.shields.io/badge/Writer-Mohammad_Fakhredin-purple)
![Writer](https://img.shields.io/badge/Writer-Mehdi_Naghian-pink)
![Writer](https://img.shields.io/badge/Writer-Yousef_Parhizkari-black)

![Graphical Design](https://img.shields.io/badge/Graphical_Design-Mostafa_Shekofteh-yellow)

![AI Assisted](https://img.shields.io/badge/AI_Assisted-Yes-red)

---
# 🤝 Contribution Rules

Before submitting your work, make sure that:

* Your files are placed in the correct directory.
* Your files follow the required naming convention.
* Only your assigned section has been modified.
* All documentation files are written in Markdown (`.md`).
* You have pulled the latest changes before pushing.

Following these guidelines helps keep the repository clean, organized, and conflict-free.

---

**Voyager Magazine**
