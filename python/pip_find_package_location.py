from pip._internal.commands.show import search_packages_info

next(search_packages_info(["botocore"])).location
