###############################################################
#Class encapsulating a user                                   #
###############################################################


class User:

    def __init__(self, nameid, state, firstlogin, infectiondate, curationdate):

        self.nameid = 'user_' + str(nameid)
        self.state = state
        self.firstlogin = firstlogin
        self.infectiondate = infectiondate
        self.curationdate = curationdate
        
    def Print(self):

        print('---------------User---------------')
        print('Name Id: ', str(self.nameid))
        print('State: ', str(self.state))
        print('First login: ', str(self.firstlogin)))
        print('Infection date: ', str(self.infectiondate)))
        print('Curation date: ', str(self.curationdate)))


