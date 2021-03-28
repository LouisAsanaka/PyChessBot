import os
import chess.engine as engine


class ChessEngine:

    def __init__(self, binary_dir, config: dict = None):
        self.binary_dir = binary_dir
        self.engine: engine.SimpleEngine = None
        if config is None:
            self.config = {
                "nodes": 100000,
                "movetime": 2000,
                "threads": 4
            }
        else:
            self.config = config

    def set_option(self, key, value):
        self.config[key] = value

    def get_option(self, key):
        return self.config[key]
            
    def start_engine(self):
        if self.engine is not None:
            self.engine.quit()
        self.engine = engine.SimpleEngine.popen_uci(os.path.join(self.binary_dir, "engine.exe"))
        self.engine.configure({
            'Threads': self.get_option("threads")
        })

    def stop_engine(self):
        self.engine.close()
        
    def evaluate(self, position):
        if self.engine is None:
            self.start_engine()
        info = self.engine.analyse(position, engine.Limit(
            nodes=self.get_option("nodes"), time=self.get_option("movetime")))
        print(info["pv"])
        return info["pv"][0]
