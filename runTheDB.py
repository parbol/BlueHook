from JanusAPI.JanusServer import JanusServer


if __name__ == "__main__":

    janus = JanusServer('ws://localhost:8182/gremlin', 0)
    janus.insertMatch('person_1', 'person_2', 1, 0, 2, 6, 3.5, 2.1, 9, 10)

