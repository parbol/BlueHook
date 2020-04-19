###############################################################
#Class encapsulating a user                                   #
###############################################################


class User:

    def __init__(self, nameid, state, firstlogin, infectiondate, curationdate):

        self.nameid = nameid
        self.state = state
        self.firstlogin = firstlogin
        self.infectiondate = infectiondate
        self.curationdate = curationdate
        

