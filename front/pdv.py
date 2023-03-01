from common import utils

if __name__ == "__main__":
    config = utils.dot_env_config()
    stage = config["stage"]
    utils.invoke_api_endpoint(f"{stage}-front")
