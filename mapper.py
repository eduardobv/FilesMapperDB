import os
import json
from my_logging import setup_logger
from repository import Repository

class Mapper:
    def __init__(self, config, logger):
        self.root = config["root"]
        self.isFlagFiles = config["isFlagFiles"]
        self.repo = Repository(config["db"], config["db_info"])
        self.logger = logger

    def convert_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB")
        i = 0
        p = 1024
        while size_bytes >= p and i < len(size_name)-1:
            size_bytes /= p
            i += 1
        return f"{size_bytes:.2f} {size_name[i]}"

    def count_files_and_size(self, path):
        total_files = 0
        total_size = 0
        for root, dirs, files in os.walk(path):
            total_files += len(files)
            for f in files:
                fp = os.path.join(root, f)
                if os.path.isfile(fp):
                    total_size += os.path.getsize(fp)
        return total_files, total_size

    def process(self):
        try:
            for root, dirs, files in os.walk(self.root):
                # Procesar directorios
                for d in dirs:
                    try:
                        dir_path = os.path.join(root, d)
                        files_count, size_bytes = self.count_files_and_size(dir_path)
                        size_str = self.convert_size(size_bytes)
                        category = state = priority = resolution = None
                        sub_info = self.repo.get_subscription_info(d)
                        if sub_info:
                            category, state, priority, resolution = sub_info
                        self.repo.insert_record(d, size_str, size_bytes, files_count, root, category, state, priority, resolution)
                        self.logger.info(f"Inserted directory: {d} with {files_count} files and size {size_str}")
                    except Exception as e:
                        self.logger.error(f"Error procesando directorio {d}: {e}")

                # Procesar archivos si el flag está activo
                if self.isFlagFiles:
                    for f in files:
                        try:
                            file_path = os.path.join(root, f)
                            size_bytes = os.path.getsize(file_path)
                            size_str = self.convert_size(size_bytes)
                            self.repo.insert_record(f, size_str, size_bytes, 0, root)
                            self.logger.info(f"Inserted file: {f} with size {size_str}")
                        except Exception as e:
                            self.logger.error(f"Error procesando archivo {f}: {e}")
            self.repo.close()
        except Exception as e:
            self.logger.error(f"Error general en process: {e}")

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    logger = setup_logger('log')
    mapper = Mapper(config, logger)
    mapper.process()
