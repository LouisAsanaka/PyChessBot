import chess.uci as uci


class ChessEngine:

    def __init__(self, config: dict = None):
        self.engine: uci.Engine = None
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
        self.engine = uci.popen_engine("..\\bin\\stockfish_10_x64.exe")
        self.engine.setoption({
            'Threads': self.get_option("threads")
        })
        self.engine.uci()
        self.engine.ucinewgame()
        print(self.engine.name)

    def stop_engine(self):
        self.engine.quit()
        
    def evaluate(self, position):
        if self.engine is None:
            self.start_engine()
        self.engine.position(position)
        
        engine_move = self.engine.go(nodes=self.get_option("nodes"), movetime=self.get_option("movetime"))[0]
        return engine_move
