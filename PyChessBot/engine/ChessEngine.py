import chess, chess.uci

class ChessEngine:

    def __init__(self, GUIWrapper):
        self.engine = None
        self.GUIWrapper = GUIWrapper
            
    def startEngine(self):
        if self.engine != None:
            self.engine.quit()
        self.engine = chess.uci.popen_engine("..\\bin\\stockfish_10_x64.exe")
        self.engine.setoption({
            'Threads': 8
        })
        self.engine.uci()
        self.engine.ucinewgame()
        print(self.engine.name)
        
    def evaluatePosition(self, position):
        if self.engine == None:
            self.startEngine()
        self.engine.position(position)
        
        engineMove = self.engine.go(nodes = self.GUIWrapper.nodeCount.get(), movetime = self.GUIWrapper.timeSlider.get())[0]
        
        return engineMove