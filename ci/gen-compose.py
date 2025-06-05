import gen

content = {
    "services": {
        "shell": {
            "entrypoint": ["/bin/bash"],
            "image": "ghcr.io/williamjacksn/ansible",
            "init": True,
            "volumes": ["./:/app"],
        }
    }
}

gen.gen(content, "compose.yaml")
