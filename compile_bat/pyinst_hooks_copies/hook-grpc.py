# https://github.com/googleapis/google-cloud-python/issues/5774

from PyInstaller.utils.hooks import collect_data_files
datas = collect_data_files('grpc')

