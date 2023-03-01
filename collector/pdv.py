from common import utils

if __name__ == "__main__":
    config = utils.dot_env_config()
    full_service_name = config["full_service_name"]
    utils.invoke_function(function_name=f"{full_service_name}-func")
