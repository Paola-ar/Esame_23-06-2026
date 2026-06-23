from database.dao import Dao
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()

        self._users_list = []
        self.load_all_users()
        self.id_user_map = {}

        #self.tot_bus_rew_by_user = {}

        #self.user_bus = []



    def load_all_users(self):
        self._users_list = Dao.read_all_users()
        self.id_user_map = {u.user_id:u for u in self._users_list}
        print(f"Users: {self.id_user_map}")

    def build_graph(self,n_min_bus):
        self.nodes = Dao.get_users_min_bus(n_min_bus,self.id_user_map)
        print(f"Users min_bus: {self.nodes}")
        #nodes = []
        #for u_id in user_min_bus:
        #    if u_id in self.id_user_map:
        #        nodo = self.id_user_map[u_id]
        #        nodes.append(nodo)
        self._graph.add_nodes_from(self.nodes)
        print(self._graph.number_of_nodes())


        #self.user_bus = Dao.get_user_bus()

        self.connessioni = Dao.get_connessioni(self.id_user_map,self.nodes)
        for v,w in self.connessioni:
            if v in self.nodes and w in self.nodes:
                dictv = Dao.get_tot_bus_rew(v)
                peso_v = dictv[v]
                dictw = Dao.get_tot_bus_rew(w)
                peso_w = dictw[w]
                peso = peso_v+peso_w
                self._graph.add_edge(v,w,weight=peso)

    def get_connessi(self):
        utenti_connessi = []
        peso_tot = 0
        for n in self.nodes:
            for v in self._graph.neighbors(n):
                peso_tot += self._graph[n][v]["weight"]
            utenti_connessi.append((n,peso_tot))
        return utenti_connessi

    def compute_best_path(self, lun):
        self._best_path = []
        self._best_Score = 0
        self._ricorsione()









