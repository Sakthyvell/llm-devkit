#!/usr/bin/env python3
"""Import mini rule sets from ciembor/agent-rules-books as knowledge skills."""

from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path


BOOKS = [
    (
        "a-philosophy-of-software-design",
        "A Philosophy of Software Design",
        "John Ousterhout",
        "API design, module depth, information hiding, and complexity-reducing refactors.",
    ),
    (
        "clean-architecture",
        "Clean Architecture",
        "Robert C. Martin",
        "stable boundaries, dependency direction, and separating policy from frameworks or databases.",
    ),
    (
        "clean-code",
        "Clean Code",
        "Robert C. Martin",
        "readability, naming, small functions, responsibilities, tests, and everyday code review.",
    ),
    (
        "code-complete",
        "Code Complete",
        "Steve McConnell",
        "disciplined construction, routine design, defensive programming, testing, and maintainability.",
    ),
    (
        "designing-data-intensive-applications",
        "Designing Data-Intensive Applications",
        "Martin Kleppmann",
        "data ownership, events, streams, replication, consistency, transactions, and schema evolution.",
    ),
    (
        "domain-driven-design",
        "Domain-Driven Design",
        "Eric Evans",
        "domain modeling, ubiquitous language, bounded contexts, and strategic design.",
    ),
    (
        "domain-driven-design-distilled",
        "Domain-Driven Design Distilled",
        "Vaughn Vernon",
        "lightweight DDD with subdomains, bounded contexts, context maps, and basic tactical patterns.",
    ),
    (
        "implementing-domain-driven-design",
        "Implementing Domain-Driven Design",
        "Vaughn Vernon",
        "aggregates, domain events, context integration, application services, and implementation-level DDD.",
    ),
    (
        "patterns-of-enterprise-application-architecture",
        "Patterns of Enterprise Application Architecture",
        "Martin Fowler",
        "enterprise layering, service layer, repositories, units of work, mappers, DTOs, and transaction patterns.",
    ),
    (
        "refactoring",
        "Refactoring",
        "Martin Fowler",
        "behavior-preserving structural improvement, code smells, tests, and small safe refactor steps.",
    ),
    (
        "refactoring-guru",
        "Refactoring.Guru",
        "Refactoring.Guru",
        "practical smell diagnosis, refactoring technique selection, and controlled cleanup.",
    ),
    (
        "release-it",
        "Release It!",
        "Michael T. Nygard",
        "production reliability, timeouts, retries, circuit breakers, bulkheads, observability, and overload.",
    ),
    (
        "the-pragmatic-programmer",
        "The Pragmatic Programmer",
        "Andrew Hunt and David Thomas",
        "pragmatic engineering, DRY knowledge, orthogonality, automation, feedback, and adaptability.",
    ),
    (
        "working-effectively-with-legacy-code",
        "Working Effectively with Legacy Code",
        "Michael Feathers",
        "safe legacy changes, characterization tests, dependency breaking, and incremental risk reduction.",
    ),
]


@dataclass(frozen=True)
class Book:
    id: str
    title: str
    author: str
    use_for: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Path to a clone of ciembor/agent-rules-books.")
    return parser.parse_args()


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def write_catalog(root: Path, books: list[Book]) -> None:
    lines = [
        "# Knowledge Standards Catalog",
        "",
        "Book-inspired engineering rule sets imported from `ciembor/agent-rules-books`.",
        "Use the `mini.md` files as focused, task-scoped guidance; prefer one to three at a time.",
        "",
        "| id | title | use for |",
        "| --- | --- | --- |",
    ]
    for book in books:
        lines.append(f"| `{book.id}` | {book.title} | {book.use_for} |")
    lines.append("")
    lines.append("Source: https://github.com/ciembor/agent-rules-books")
    lines.append("License: MIT; see `standards/LICENSE.agent-rules-books`.")
    (root / "standards" / "catalog.md").write_text("\n".join(lines), encoding="utf-8")


def write_usage(root: Path) -> None:
    text = """# Knowledge Standards Usage

Use these standards as optional, task-scoped engineering guidance.

- Prefer `mini.md` for normal planning, implementation, refactoring, and review.
- Load at most three standards for one task unless the user explicitly asks for more.
- If standards overlap, choose the one most specific to the work instead of loading both.
- Treat the standards as decision pressure, not as a replacement for local code conventions.
- Do not apply a standard globally just because it exists in this repository.

Invocation examples:

- `plan with clean-code`
- `plan with refactoring, working-effectively-with-legacy-code`
- `review with release-it`
- `orient with domain-driven-design-distilled`

When a user names a standard, load `standards/<id>/mini.md` or invoke the matching installed skill `llm-devkit-knowledge-<id>`.
See `standards/catalog.md` for valid ids.
"""
    (root / "standards" / "USAGE.md").write_text(text, encoding="utf-8")


def write_skill(root: Path, book: Book, mini_text: str) -> None:
    skill_dir = root / "skills" / "knowledge" / book.id
    skill_dir.mkdir(parents=True, exist_ok=True)
    body = f"""---
name: {book.id}
description: Apply the {book.title} knowledge standard as task-scoped engineering guidance. Use when the user explicitly invokes this knowledge skill, says `with {book.id}`, or asks for {book.use_for}
---

Use this as an active engineering standard for the current task only.

- Apply these rules alongside local project conventions and user instructions.
- Prefer concrete, scoped improvements over broad rewrites.
- If combined with other knowledge standards, reconcile conflicts in favor of the most task-specific rule.
- Do not quote or summarize the source as book notes; use it to shape planning, implementation, and review decisions.

Imported from `ciembor/agent-rules-books` (`{book.id}.mini.md`), MIT licensed.

{mini_text.rstrip()}
"""
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")


def import_books(source: Path) -> None:
    if not source.exists():
        raise SystemExit(f"source path does not exist: {source}")

    root = repo_root()
    books = [Book(*item) for item in BOOKS]
    standards_root = root / "standards"
    standards_root.mkdir(exist_ok=True)

    for book in books:
        upstream_mini = source / book.id / f"{book.id}.mini.md"
        if not upstream_mini.exists():
            raise SystemExit(f"missing upstream mini file: {upstream_mini}")
        target_dir = standards_root / book.id
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(upstream_mini, target_dir / "mini.md")
        write_skill(root, book, upstream_mini.read_text(encoding="utf-8"))

    license_path = source / "LICENSE"
    if license_path.exists():
        shutil.copyfile(license_path, standards_root / "LICENSE.agent-rules-books")
    write_catalog(root, books)
    write_usage(root)


def main() -> int:
    args = parse_args()
    import_books(args.source)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
