from pathlib import Path

from common import utils

if __name__ == "__main__":
    config = utils.dot_env_config(Path(__file__).parent / ".env")
    stage = config["stage"]
    utils.invoke_api_endpoint(f"{stage}-front")
