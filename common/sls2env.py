import json
import subprocess
from pathlib import Path


def unwrap(d, keys=[]):
    for k, v in d.items():
        new_keys = keys + [k]
        if isinstance(v, list):
            v = {str(i): v for i, v in enumerate(v)}
        if isinstance(v, dict):
            yield from unwrap(keys=new_keys, d=v)
        else:
            yield "_".join(new_keys), v


class Config:
    @classmethod
    def from_serverless(cls):
        result = subprocess.run(["serverless", "print", "--format json"], check=True, stdout=subprocess.PIPE)
        print(f"json2env result:\n{result.stdout}")
        config = json.loads(result.stdout)
        return cls(config)

    def __init__(self, config):
        self.config = config

    def to_dot_env(self, path: Path = None):
        path = path or Path(".env")
        result = [f'{k}="{v}"' for k, v in unwrap(d=self.config)]
        content = "\n".join(result)
        path.write_text(content)


def main():
    Config.from_serverless().to_dot_env()


if __name__ == '__main__':
    main()
