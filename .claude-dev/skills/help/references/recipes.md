# Recipes

Prompts to copy. Replace the names in angle brackets.

**New company, from scratch**

```
/resume-builder:resume-auto-mode full-pipeline <company>
```

**One project, from raw data to confirmed evidence**

```
/resume-builder:resume-auto-mode distill <company> <id>
/resume-builder:resume-auto-mode verify <company> <id>
```

**Work with no repo**

```
/resume-builder:resume-auto-mode distill <company> <id>
```

Answer "interview" when it asks how to build the file.

**Resume for one job ad**

```
/resume-builder:resume-auto-mode to-resume <yyyy-mon-company-role>
```

Paste the ad when it asks. Then `review-resume <slug>`.

**Change one thing**

```
/resume-builder:resume-auto-mode steer base <what to change>
```

**Prepare for an interview**

```
/resume-builder:resume-auto-mode to-brag <company>
```

**Not sure what's next**

```
/resume-builder:help <company>
```
