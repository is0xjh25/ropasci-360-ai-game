import the_pink_coder.player as player

def main():
    player1 = player.Player("upper")
    # print(player.round)
    # print(player.possible_throw_position)
    player1.update(player1.action(),("THROW","r",(-4,0)))
    player1.update(player1.action(),("THROW","p",(-3,0)))
    player1.update(player1.action(),("THROW","p",(-3,0)))
    player1.update(player1.action(),("THROW","p",(-3,0)))
    player1.update(player1.action(),("THROW","p",(-3,0)))

    player1.update(player1.action(),("THROW","p",(-3,0)))
    player1.update(player1.action(),("THROW","p",(-3,0)))
    player1.update(player1.action(),("THROW","p",(-3,0)))
    player1.update(player1.action(),("THROW","p",(-3,0)))
    
    # print(player.board)
    