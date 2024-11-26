import configparser
import multiprocessing

from aiwolf_nlp_common import util

import main
from lib.log import LogInfo


def execute_game(inifile: configparser.ConfigParser, name: str, log_info: LogInfo):
    while True:
        sock = util.get_socket(inifile=inifile, name=name)
        sock.connect()

        received = None

        for _ in range(inifile.getint("game", "num")):
            received = main.main(
                sock=sock,
                inifile=inifile,
                received=received,
                name=name,
                log_info=log_info,
            )

        sock.close()

        if not inifile.getboolean("connection", "keep_connection"):
            break


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")

    config_path = "./res/config.ini"

    inifile = util.read_config_file(config_file_path=config_path)

    log_info = LogInfo()

    agent_num = int(inifile.get("agent", "num"))
    processes = list()

    print("agent_num:" + str(agent_num))

    for i in range(agent_num):
        process = multiprocessing.Process(
            name="p" + str(i + 1),
            target=execute_game,
            args=(inifile, inifile.get("agent", "name" + str(i + 1)), log_info),
        )
        processes.append(process)
        processes[i].start()

    for process in processes:
        process.join()
