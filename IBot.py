class IBot(object):
    def GetMove(self, game, letter):
        """Gets the move with given current game state"""
        raise NotImplementedError("GetMove needs to be implemented!")