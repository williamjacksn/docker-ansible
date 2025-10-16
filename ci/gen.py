import json
import pathlib

ACTIONS_CHECKOUT = {"name": "Check out repository", "uses": "actions/checkout@v5"}
CONTAINER_IMAGE = "ghcr.io/williamjacksn/ansible"
DEFAULT_BRANCH = "main"
IMAGE_PUSH_EVENTS = ["push", "workflow_dispatch"]
IMAGE_PUSH_IF = " || ".join(f"github.event_name == '{e}'" for e in IMAGE_PUSH_EVENTS)
THIS_FILE = pathlib.PurePosixPath(
    pathlib.Path(__file__).relative_to(pathlib.Path.cwd())
)


def gen(content: dict, target: str) -> None:
    pathlib.Path(target).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(target).write_text(
        json.dumps(content, indent=2, sort_keys=True), newline="\n"
    )


def gen_compose() -> None:
    target = "compose.yaml"
    description = f"This file ({target}) was generated from {THIS_FILE}"
    content = {
        "services": {
            "shell": {
                "entrypoint": ["/bin/bash"],
                "environment": {"DESCRIPTION": description},
                "image": CONTAINER_IMAGE,
                "init": True,
                "volumes": ["./:/app"],
            }
        }
    }
    gen(content, target)


def gen_dependabot() -> None:
    target = ".github/dependabot.yaml"
    content = {
        "version": 2,
        "updates": [
            {
                "package-ecosystem": e,
                "allow": [{"dependency-type": "all"}],
                "directory": "/",
                "schedule": {"interval": "weekly"},
            }
            for e in ["docker", "github-actions", "uv"]
        ],
    }
    gen(content, target)


def gen_workflow_build() -> None:
    target = ".github/workflows/build-container-image.yaml"
    content = {
        "env": {
            "description": f"This workflow ({target}) was generated from {THIS_FILE}"
        },
        "name": "Build the container image",
        "on": {
            "pull_request": {"branches": [DEFAULT_BRANCH]},
            "push": {"branches": [DEFAULT_BRANCH]},
            "workflow_dispatch": {},
        },
        "permissions": {},
        "jobs": {
            "build": {
                "name": "Build the container image",
                "permissions": {"packages": "write"},
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "name": "Set up Docker Buildx",
                        "uses": "docker/setup-buildx-action@v3",
                    },
                    {
                        "name": "Build the container image",
                        "uses": "docker/build-push-action@v6",
                        "with": {
                            "cache-from": "type=gha",
                            "cache-to": "type=gha,mode=max",
                            "tags": f"{CONTAINER_IMAGE}:latest",
                        },
                    },
                    {
                        "name": "Log in to GitHub container registry",
                        "if": IMAGE_PUSH_IF,
                        "uses": "docker/login-action@v3",
                        "with": {
                            "password": "${{ github.token }}",
                            "registry": "ghcr.io",
                            "username": "${{ github.actor }}",
                        },
                    },
                    {
                        "name": "Push latest image to registry",
                        "if": IMAGE_PUSH_IF,
                        "uses": "docker/build-push-action@v6",
                        "with": {
                            "cache-from": "type=gha",
                            "push": True,
                            "tags": f"{CONTAINER_IMAGE}:latest",
                        },
                    },
                ],
            }
        },
    }
    gen(content, target)


def gen_workflow_ruff() -> None:
    target = ".github/workflows/ruff.yaml"
    content = {
        "name": "Ruff",
        "on": {
            "pull_request": {"branches": [DEFAULT_BRANCH]},
            "push": {"branches": [DEFAULT_BRANCH]},
        },
        "permissions": {"contents": "read"},
        "env": {
            "description": f"This workflow ({target}) was generated from {THIS_FILE}"
        },
        "jobs": {
            "ruff-check": {
                "name": "Run ruff check",
                "runs-on": "ubuntu-latest",
                "steps": [
                    ACTIONS_CHECKOUT,
                    {"name": "Run ruff check", "run": "sh ci/ruff-check.sh"},
                ],
            },
            "ruff-format": {
                "name": "Run ruff format",
                "runs-on": "ubuntu-latest",
                "steps": [
                    ACTIONS_CHECKOUT,
                    {"name": "Run ruff format", "run": "sh ci/ruff-format.sh"},
                ],
            },
        },
    }
    gen(content, target)


def main() -> None:
    gen_compose()
    gen_dependabot()
    gen_workflow_build()
    gen_workflow_ruff()


if __name__ == "__main__":
    main()
