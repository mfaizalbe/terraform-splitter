---
name: verify
description: How to run and drive terraform-splitter to observe behavior end-to-end.
---

Single-file CLI, no build step, no deps beyond stdlib.

## Run it

```bash
cd <dir containing main.tf>
python3 /path/to/terraform_splitter.py
```

It always operates on the current working directory (searches cwd/subdirs for
`main.tf`, skipping hidden dirs like `.terraform`/`.git`). No CLI args.

## Useful scenarios to drive

- Happy path: a `main.tf` with `terraform`, `provider`, `variable`, `data`,
  `output`, `locals`, and a couple of `resource` blocks of different types
  (e.g. `aws_s3_bucket`, `aws_instance`, `google_compute_instance`) — check
  the resulting `*.tf` files land next to `main.tf` and `main.tf` gets
  renamed to `main.tf.bak`.
- Re-run on the same directory after copying `main.tf.bak` back to
  `main.tf` — checks for duplicate-content regressions in the per-file
  handles.
- Heredoc content (`user_data = <<-EOT ... EOT`) containing a stray `{`/`}`
  — checks brace-counting doesn't misfire on template bodies.
- Empty directory (no `main.tf` anywhere) — expect
  `error: no main.tf found` on stderr/stdout and exit code 1.

## Gotchas

- This sandbox's `ls` is aliased to something that can hang; use `find` or
  the `Read`/dedicated file tools instead when inspecting output dirs.
- Each Bash tool invocation resets cwd afterward ("Shell cwd was reset") —
  don't rely on `cd` persisting across separate tool calls; use absolute
  paths or `cd ... &&` within a single command.
