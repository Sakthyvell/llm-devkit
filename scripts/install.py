#!/usr/bin/env python3
"""Install llm-devkit skills into supported global agent locations."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


PREFIX = "llm-devkit"

@dataclass(frozen=True)
class Skill:
    category: str
    skill: str
    source_dir: Path
    source_file: Path
    rel_source: Path
    frontmatter: list[str]
    body: str
    metadata: dict[str, str]

    @property
    def generated_name(self) -> str:
        return f"{PREFIX}-{self.category}-{self.skill}"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def home_path(*parts: str) -> Path:
    return Path.home().joinpath(*parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install llm-devkit global skills.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Show changes without writing files.")
    mode.add_argument("--clean", action="store_true", help="Remove generated llm-devkit skills.")
    return parser.parse_args()


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def parse_frontmatter(path: Path) -> tuple[list[str], str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path}: missing YAML frontmatter")

    end_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_index = index
            break

    if end_index is None:
        raise ValueError(f"{path}: frontmatter is not closed")

    frontmatter = lines[1:end_index]
    body = "".join(lines[end_index + 1 :]).lstrip("\n")
    metadata: dict[str, str] = {}

    for line in frontmatter:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", stripped)
        if not match:
            raise ValueError(f"{path}: unsupported frontmatter line: {stripped}")
        key, value = match.groups()
        metadata[key] = value.strip().strip('"').strip("'")

    return frontmatter, body, metadata


def discover_skills(root: Path) -> list[Skill]:
    skills_root = root / "skills"
    if not skills_root.exists():
        raise ValueError("missing skills/ directory")

    invalid_plural = sorted(skills_root.glob("*/*/SKILLS.md"))
    if invalid_plural:
        names = ", ".join(rel(path, root) for path in invalid_plural)
        raise ValueError(f"invalid skill filename; use SKILL.md: {names}")

    paths = sorted(skills_root.glob("*/*/SKILL.md"))
    if not paths:
        raise ValueError("no skills found at skills/<category>/<skill>/SKILL.md")

    discovered: list[Skill] = []
    generated_names: set[str] = set()
    valid_name = re.compile(r"^[a-z0-9-]+$")

    for source_file in paths:
        source_dir = source_file.parent
        skill = source_dir.name
        category = source_dir.parent.name
        rel_source = source_file.relative_to(root)

        if not valid_name.fullmatch(category):
            raise ValueError(f"{rel_source}: invalid category name {category!r}")
        if not valid_name.fullmatch(skill):
            raise ValueError(f"{rel_source}: invalid skill name {skill!r}")

        frontmatter, body, metadata = parse_frontmatter(source_file)
        if metadata.get("name") != skill:
            raise ValueError(f"{rel_source}: frontmatter name must equal folder name {skill!r}")
        if not metadata.get("description"):
            raise ValueError(f"{rel_source}: description is required")

        item = Skill(
            category=category,
            skill=skill,
            source_dir=source_dir,
            source_file=source_file,
            rel_source=rel_source,
            frontmatter=frontmatter,
            body=body,
            metadata=metadata,
        )
        if item.generated_name in generated_names:
            raise ValueError(f"{rel_source}: duplicate generated name {item.generated_name}")
        generated_names.add(item.generated_name)
        discovered.append(item)

    return discovered


def rewrite_frontmatter(skill: Skill) -> str:
    lines = list(skill.frontmatter)
    replaced = False
    for index, line in enumerate(lines):
        if re.match(r"^\s*name\s*:", line):
            newline = "\n" if line.endswith("\n") else ""
            lines[index] = f"name: {skill.generated_name}{newline}"
            replaced = True
            break
    if not replaced:
        raise ValueError(f"{skill.rel_source}: name is required")

    return f"---\n{''.join(lines)}---\n\n{skill.body}"


def generated_skill_paths(skill: Skill) -> tuple[Path, Path]:
    return (
        home_path(".claude", "skills", skill.generated_name),
        home_path(".agents", "skills", skill.generated_name),
    )


def copy_skill_dir(skill: Skill, target: Path, root: Path, dry_run: bool) -> None:
    status = "replace" if target.exists() else "create"
    print(f"{status}: {target}")
    if dry_run:
        return

    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(skill.source_dir, target)
    generated_skill = target / "SKILL.md"
    generated_skill.write_text(rewrite_frontmatter(skill), encoding="utf-8")


def cursor_export(skills: list[Skill]) -> str:
    parts = ["# llm-devkit Skills\n"]
    for skill in skills:
        parts.extend(
            [
                f"## @{skill.generated_name}\n",
                f"Use this workflow when I mention `@{skill.generated_name}`.\n",
                skill.body.rstrip(),
                "",
            ]
        )
    return "\n".join(parts).rstrip() + "\n"


def write_manifest(skills: list[Skill], root: Path, dry_run: bool) -> None:
    dist = root / "dist"
    manifest_path = dist / "manifest.json"
    cursor_path = dist / "cursor-user-rules.md"
    manifest = {
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "skills": [
            {
                "source": skill.rel_source.as_posix(),
                "generated_name": skill.generated_name,
                "claude_path": str(generated_skill_paths(skill)[0]),
                "codex_path": str(generated_skill_paths(skill)[1]),
            }
            for skill in skills
        ],
    }

    print(f"write: {cursor_path}")
    print(f"write: {manifest_path}")
    if dry_run:
        return

    dist.mkdir(parents=True, exist_ok=True)
    cursor_path.write_text(cursor_export(skills), encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def install(root: Path, dry_run: bool) -> int:
    skills = discover_skills(root)
    print(f"validated {len(skills)} skill(s)")

    for skill in skills:
        claude_path, codex_path = generated_skill_paths(skill)
        copy_skill_dir(skill, claude_path, root, dry_run)
        copy_skill_dir(skill, codex_path, root, dry_run)

    write_manifest(skills, root, dry_run)
    return 0


def remove_path(path: Path, dry_run: bool) -> None:
    if not path.exists():
        return
    print(f"remove: {path}")
    if dry_run:
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def clean(root: Path, dry_run: bool = False) -> int:
    manifest_path = root / "dist" / "manifest.json"
    seen: set[Path] = set()

    if manifest_path.exists():
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        for item in data.get("skills", []):
            for key in ("claude_path", "codex_path"):
                value = item.get(key)
                if value:
                    seen.add(Path(value).expanduser())

    for base in (home_path(".claude", "skills"), home_path(".agents", "skills")):
        if base.exists():
            for path in sorted(base.glob(f"{PREFIX}-*")):
                seen.add(path)

    for path in sorted(seen):
        remove_path(path, dry_run)

    remove_path(root / "dist" / "cursor-user-rules.md", dry_run)
    remove_path(manifest_path, dry_run)
    return 0


def main() -> int:
    args = parse_args()
    root = repo_root()

    try:
        if args.clean:
            return clean(root)
        return install(root, dry_run=args.dry_run)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
