from enum import Enum
from collections import defaultdict, deque
import sys
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.obj import PetriNet as PM4PyPetriNet

class RelSetType(Enum):
    Order = "→"
    ReverseOrder = "←"
    Interleaving = "||"
    Exclusive = "-"
    NoneType = ""

    def __str__(self):
        return self.value

class RelSet:
    #RELATION_FAR_LOOKAHEAD = 999999999
    RELATION_FAR_LOOKAHEAD = 1

    def __init__(self, net_system, nodes, look_ahead):
        self.net_system = net_system
        self.entities = list(nodes)
        self.look_ahead = look_ahead
        self.matrix = [[RelSetType.NoneType for _ in nodes] for _ in nodes]

    def get_matrix(self):
        return self.matrix

    def get_entities(self):
        return self.entities

    def get_look_ahead(self):
        return self.look_ahead

class AbstractRelSetCreator:
    @staticmethod
    def set_matrix_entry(matrix, index1, index2, rel_set_type):
        matrix[index1][index2] = rel_set_type
        matrix[index2][index1] = rel_set_type

    @staticmethod
    def set_matrix_entry_order(matrix, index1, index2):
        matrix[index1][index2] = RelSetType.Order
        matrix[index2][index1] = RelSetType.ReverseOrder

class PetriNet:
    class STRUCTURAL_CHECKS:
        @staticmethod
        def is_workflow_net(pn):
            return True

    class DIRECTED_GRAPH_ALGORITHMS:
        @staticmethod
        def has_path(pn, n1, n2):
            visited = set()
            queue = deque([n1])
            while queue:
                current = queue.popleft()
                if current == n2:
                    return True
                if current not in visited:
                    visited.add(current)
                    queue.extend(pn.get_successors(current))
            return False

class Node:
    def __init__(self, name):
        self.name = name

class Transition(Node):
    def __init__(self, name):
        super().__init__(name)

class Place(Node):
    def __init__(self, name):
        super().__init__(name)
        
class NetSystem:
    def __init__(self):
        self.transitions = []
        self.places = []
        self.flows = defaultdict(list)
        self.marking = defaultdict(int)

    def get_transitions(self):
        return self.transitions

    def get_nodes(self):
        return self.transitions + self.places

    def add_node(self, node):
        if isinstance(node, Transition):
            self.transitions.append(node)
        elif isinstance(node, Place):
            self.places.append(node)

    def add_flow(self, source, target):
        self.flows[source].append(target)

    def get_marking(self):
        return self.marking

    def get_successors(self, node):
        return self.flows[node]

    def get_preset(self, node):
        return [source for source, targets in self.flows.items() if node in targets]

    def get_postset(self, node):
        return self.flows[node]

    def get_marked_places(self):
        return [place for place, tokens in self.marking.items() if tokens > 0]
    
class CompletePrefixUnfolding:
    def __init__(self, pn, setup):
        self.pn = pn
        self.setup = setup
        self.occurrence_net = OccurrenceNet(pn)

    def get_occurrence_net(self):
        return self.occurrence_net

class OccurrenceNet:
    def __init__(self, pn):
        self.pn = pn
        self.transitions = pn.get_transitions()
        self.cutoff_events = []
        self.corresponding_events = {}

    def get_transitions(self):
        return self.transitions

    def get_cutoff_events(self):
        return self.cutoff_events

    def get_corresponding_event(self, event):
        return self.corresponding_events.get(event, event)

    def get_ordering_relation(self, node1, node2):
        if node1 == node2:
            return 'CONCURRENT'
        return 'ARBITRARY'

    def get_preset(self, node):
        return self.pn.get_preset(node)

    def get_postset(self, node):
        return self.pn.get_postset(node)

class CompletePrefixUnfoldingSetup:
    def __init__(self):
        self.ADEQUATE_ORDER = None

class ConcurrencyRelation:
    def __init__(self, net_system):
        self.sys = net_system
        self.nodes = list(self.sys.get_nodes())
        self.matrix = None
        self.indirect_places = defaultdict(set)

    def are_concurrent(self, n1, n2):
        if self.matrix is None:
            self.calculate_concurrency_matrix()
        index1 = self.nodes.index(n1)
        index2 = self.nodes.index(n2)
        return self.matrix[index1][index2]

    def set_nodes_concurrent(self, n1, n2):
        if n1 == n2:
            return
        index1 = self.nodes.index(n1)
        index2 = self.nodes.index(n2)
        self.matrix[index1][index2] = True
        self.matrix[index2][index1] = True

    def set_node_concurrent_to_nodes(self, n, nodes):
        for n2 in nodes:
            self.set_nodes_concurrent(n, n2)

    def set_all_nodes_concurrent(self, nodes):
        for n in nodes:
            self.set_node_concurrent_to_nodes(n, nodes)

    def add_all_combinations(self, combinations, nodes):
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                combinations.add((nodes[i], nodes[j]))
                combinations.add((nodes[j], nodes[i]))

    def calculate_concurrency_matrix(self):
        self.matrix = [[False] * len(self.nodes) for _ in range(len(self.nodes))]
        conc_nodes = set()

        initial_places = list(self.sys.get_marked_places())
        self.set_all_nodes_concurrent(initial_places)
        self.add_all_combinations(conc_nodes, initial_places)

        for t1 in self.sys.get_transitions():
            out_places = list(self.sys.get_postset(t1))
            self.set_all_nodes_concurrent(out_places)
            self.add_all_combinations(conc_nodes, out_places)

        if PetriNet.STRUCTURAL_CHECKS.is_workflow_net(self.sys):
            for n in self.nodes:
                if isinstance(n, Place):
                    nodes = set()
                    for t2 in self.sys.get_postset(n):
                        for n2 in self.sys.get_postset(t2):
                            nodes.add(n2)
                    self.indirect_places[n] = nodes

        self.process_conc_nodes(conc_nodes, PetriNet.STRUCTURAL_CHECKS.is_workflow_net(self.sys))

    def process_conc_nodes(self, conc_nodes, is_fc):
        for (x, p) in conc_nodes:
            if is_fc:
                if self.sys.get_postset(p):
                    t = next(iter(self.sys.get_postset(p)))
                    if self.node_concurrent_to_nodes(x, self.sys.get_preset(t)):
                        suc_p = self.sys.get_postset(p)
                        conc_nodes2 = set()
                        if isinstance(x, Place):
                            for u in suc_p:
                                if not self.are_concurrent(x, u):
                                    conc_nodes2.add((u, x))
                        for pp in self.indirect_places[p]:
                            if not self.are_concurrent(x, pp):
                                conc_nodes2.add((x, pp))
                                if isinstance(x, Place):
                                    conc_nodes2.add((pp, x))
                        self.set_node_concurrent_to_nodes(x, suc_p)
                        self.set_node_concurrent_to_nodes(x, self.indirect_places[p])
                        self.process_conc_nodes(conc_nodes2, is_fc)
            else:
                for t in self.sys.get_postset(p):
                    if self.node_concurrent_to_nodes(x, self.sys.get_preset(t)):
                        suc_t = self.sys.get_postset(t)
                        conc_nodes2 = set()
                        for s in suc_t:
                            if not self.are_concurrent(x, s):
                                conc_nodes2.add((x, s))
                                if isinstance(x, Place):
                                    conc_nodes2.add((s, x))
                        if isinstance(x, Place):
                            conc_nodes2.add((t, x))
                        self.set_node_concurrent_to_nodes(x, suc_t)
                        self.set_nodes_concurrent(x, t)
                        self.process_conc_nodes(conc_nodes2, is_fc)

    def node_concurrent_to_nodes(self, n, nodes):
        i = self.nodes.index(n)
        for n2 in nodes:
            j = self.nodes.index(n2)
            if not self.matrix[i][j]:
                return False
        return True

class RelSetCreatorUnfolding(AbstractRelSetCreator):
    e_instance = None

    @staticmethod
    def get_instance():
        if RelSetCreatorUnfolding.e_instance is None:
            RelSetCreatorUnfolding.e_instance = RelSetCreatorUnfolding()
        return RelSetCreatorUnfolding.e_instance

    def __init__(self):
        self.unfolding = None
        self.occurrence_net = None
        self.step_matrix = None
        self.nodes_for_step_matrix = []
        self.base_order_matrix_for_transitions = None
        self.transitions_for_base_order_matrix = []

    def clear(self):
        self.unfolding = None
        self.occurrence_net = None
        self.step_matrix = None
        self.nodes_for_step_matrix = []
        self.base_order_matrix_for_transitions = None
        self.transitions_for_base_order_matrix = []

    def derive_relation_set(self, pn, nodes=None, look_ahead=RelSet.RELATION_FAR_LOOKAHEAD):
        self.clear()
        setup = CompletePrefixUnfoldingSetup()
        setup.ADEQUATE_ORDER = 'ESPARZA_FOR_ARBITRARY_SYSTEMS'
        self.unfolding = CompletePrefixUnfolding(pn, setup)
        self.occurrence_net = self.unfolding.get_occurrence_net()
        self.derive_step_matrix()
        rel_set = RelSet(pn, nodes or pn.get_transitions(), look_ahead)
        matrix = rel_set.get_matrix()
        concurrency_relation = ConcurrencyRelation(pn)
        for t in rel_set.get_entities():
            if isinstance(t, Transition) and t not in self.transitions_for_base_order_matrix:
                self.transitions_for_base_order_matrix.append(t)
        self.derive_base_order_relation(rel_set)
        for t1 in rel_set.get_entities():
            index1 = rel_set.get_entities().index(t1)
            for t2 in rel_set.get_entities():
                index2 = rel_set.get_entities().index(t2)
                if index2 > index1:
                    continue
                if (
                    self.is_base_order(t1, t2)
                    and self.is_base_order(t2, t1)
                ):
                    super().set_matrix_entry(matrix, index1, index2, RelSetType.Interleaving)
                elif self.is_base_order(t1, t2):
                    super().set_matrix_entry_order(matrix, index1, index2)
                elif self.is_base_order(t2, t1):
                    super().set_matrix_entry_order(matrix, index2, index1)
                elif concurrency_relation.are_concurrent(t1, t2):
                    super().set_matrix_entry(matrix, index1, index2, RelSetType.Interleaving)
                else:
                    super().set_matrix_entry(matrix, index1, index2, RelSetType.Exclusive)
        return rel_set

    def derive_base_order_relation(self, rel_set):
        self.base_order_matrix_for_transitions = [[False] * len(self.transitions_for_base_order_matrix) for _ in range(len(self.transitions_for_base_order_matrix))]
        for e1 in self.occurrence_net.get_transitions():
            for e2 in self.occurrence_net.get_transitions():
                if self.get_distance_in_step_matrix(e1, e2) <= rel_set.get_look_ahead():
                    if e1 in self.transitions_for_base_order_matrix and e2 in self.transitions_for_base_order_matrix:
                        i1 = self.transitions_for_base_order_matrix.index(e1)
                        i2 = self.transitions_for_base_order_matrix.index(e2)
                        if self.occurrence_net.get_ordering_relation(e1, e2) != 'CONCURRENT':
                            self.base_order_matrix_for_transitions[i1][i2] = True

    def get_distance_in_step_matrix(self, node1, node2):
        if node1 != node2 and self.occurrence_net.get_ordering_relation(node1, node2) == 'CONCURRENT':
            return 1
        return self.step_matrix[self.nodes_for_step_matrix.index(node1)][self.nodes_for_step_matrix.index(node2)]

    def is_base_order(self, n1, n2):
        return self.base_order_matrix_for_transitions[self.transitions_for_base_order_matrix.index(n1)][self.transitions_for_base_order_matrix.index(n2)]

    def derive_step_matrix(self):
        self.nodes_for_step_matrix.extend(self.occurrence_net.get_transitions())
        size = len(self.nodes_for_step_matrix)
        self.step_matrix = [[sys.maxsize] * size for _ in range(size)]
        for e1 in self.occurrence_net.get_transitions():
            i1 = self.nodes_for_step_matrix.index(e1)
            for e2 in self.occurrence_net.get_transitions():
                i2 = self.nodes_for_step_matrix.index(e2)
                self.step_matrix[i1][i2] = sys.maxsize
        for e1 in self.occurrence_net.get_transitions():
            i1 = self.nodes_for_step_matrix.index(e1)
            for e2 in self.occurrence_net.get_transitions():
                i2 = self.nodes_for_step_matrix.index(e2)
                for c in self.occurrence_net.get_preset(e2):
                    if e1 in self.occurrence_net.get_preset(c):
                        self.step_matrix[i1][i2] = 1
        for cut_e in self.occurrence_net.get_cutoff_events():
            i_cut_e = self.nodes_for_step_matrix.index(cut_e)
            cor_e = self.occurrence_net.get_corresponding_event(cut_e)
            while cor_e in self.occurrence_net.get_cutoff_events():
                cor_e = self.occurrence_net.get_corresponding_event(cor_e)
            for c in self.occurrence_net.get_postset(cor_e):
                for e in self.occurrence_net.get_postset(c):
                    i_e = self.nodes_for_step_matrix.index(e)
                    self.step_matrix[i_cut_e][i_e] = 1
        for r in range(size):
            for e1 in self.occurrence_net.get_transitions():
                i1 = self.nodes_for_step_matrix.index(e1)
                for e2 in self.occurrence_net.get_transitions():
                    i2 = self.nodes_for_step_matrix.index(e2)
                    self.step_matrix[i1][i2] = min(self.step_matrix[i1][i2], self.step_matrix[i1][r] + self.step_matrix[r][i2])

def create_order_relation_from_matrix(matrix, transitions):
    orders = []
    for i, row in enumerate(matrix):
        order = []
        for j, relation in enumerate(row):
            
            if relation == RelSetType.Order:
                order.append(f"{transitions[i].name}{transitions[j].name}")
        orders.append(order)
    return orders

def create_concurrency_relation_from_matrix(matrix, transitions):
    concurrencies = []
    for i, row in enumerate(matrix):
        concurrency = []
        for j, relation in enumerate(row):
            if relation == RelSetType.Interleaving:
                concurrency.append(f"{transitions[i].name}{transitions[j].name}")
        concurrencies.append(concurrency)
    return concurrencies

def create_exclusive_relation_from_matrix(matrix, transitions):
    exclusives = []
    for i, row in enumerate(matrix):
        exclusive = []
        for j, relation in enumerate(row):
            if relation == RelSetType.Exclusive:
                exclusive.append(f"{transitions[i].name}{transitions[j].name}")
        exclusives.append(exclusive)
    return exclusives


def convert_pm4py_to_custom(petri_net_pm4py, initial_marking):
    net = NetSystem()
    place_mapping = {}
    transition_mapping = {}

    # Add places
    for place in petri_net_pm4py.places:
        custom_place = Place(place.name if place.name else str(place))
        net.add_node(custom_place)
        place_mapping[place] = custom_place

    # Add transitions
    for transition in petri_net_pm4py.transitions:
         # Assign a default name if both label and name are missing
        custom_transition = Transition(transition.label if transition.label else transition.name)
        net.add_node(custom_transition)
        transition_mapping[transition] = custom_transition
        

    # Add arcs (flows)
    for arc in petri_net_pm4py.arcs:
        source = arc.source
        target = arc.target
        if isinstance(source, PM4PyPetriNet.Place):
            source_node = place_mapping[source]
        elif isinstance(source, PM4PyPetriNet.Transition):
            source_node = transition_mapping[source]
        else:
            continue

        if isinstance(target, PM4PyPetriNet.Place):
            target_node = place_mapping[target]
        elif isinstance(target, PM4PyPetriNet.Transition):
            target_node = transition_mapping[target]
        else:
            continue

        net.add_flow(source_node, target_node)

    # Set initial marking
    for place, tokens in initial_marking.items():
        net.marking[place_mapping[place]] = tokens

    return net

def find_last_transitions(net_pm4py, final_marking):
    last_transitions = set()  # Use a set to avoid duplicates

    # Iterate through the places in the final marking
    for place in final_marking.keys():
        # Find transitions that lead to this place (incoming transitions)
        for arc in net_pm4py.arcs:
            if arc.target == place and isinstance(arc.source, PM4PyPetriNet.Transition):
                last_transitions.add(arc.source)
    
    return last_transitions

def find_first_transitions(net_pm4py, initial_marking):

    def is_silent(transition):
        return not transition.label  # label is None or empty for silent

    first_transitions = set()

    # Step 1: Find initial transitions (may include silent)
    for place in initial_marking.keys():
        for arc in net_pm4py.arcs:
            if arc.source == place and isinstance(arc.target, PM4PyPetriNet.Transition):
                first_transitions.add(arc.target)

    # Step 2: Recursively find non-silent transitions if first are silent
    actual_first_transitions = set()

    def find_non_silent_from(transition, visited):
        if transition in visited:
            return
        visited.add(transition)
        if not is_silent(transition):
            actual_first_transitions.add(transition)
        else:
            # Follow outgoing arcs to next transitions
            for arc in net_pm4py.arcs:
                if arc.source == transition and isinstance(arc.target, PM4PyPetriNet.Place):
                    # From this place, follow to next transitions
                    for arc2 in net_pm4py.arcs:
                        if arc2.source == arc.target and isinstance(arc2.target, PM4PyPetriNet.Transition):
                            find_non_silent_from(arc2.target, visited)

    for t in first_transitions:
        find_non_silent_from(t, set())

    # Return the actual first transitions found
    return actual_first_transitions

def matrix_function(pnml_path):
    
    # Import the PNML file
    net_pm4py, initial_marking, final_marking = pnml_importer.apply(pnml_path)
    net = convert_pm4py_to_custom(net_pm4py, initial_marking)

    first_transitions=find_first_transitions(net_pm4py, initial_marking)
    print("Start Activties: ", [t.label if t.label else t.name for t in first_transitions])

    last_transitions=find_last_transitions(net_pm4py, final_marking)
    print("End Activties: ", [t.label if t.label else t.name for t in last_transitions])    
     
    if not PetriNet.STRUCTURAL_CHECKS.is_workflow_net(net):
        print("The net system is not a valid workflow net.")
        return None, None, None

    # Find all silent (invisible) transitions in the Petri net
    silent_transitions_names = [t.name for t in net_pm4py.transitions if not t.label]
    #print("Silent Transitions:", silent_transitions_names)
    
    rs_creator = RelSetCreatorUnfolding.get_instance()
    transitions = [n for n in net.get_nodes() if isinstance(n, Transition)]
    rel_set = rs_creator.derive_relation_set(net, transitions, 1)
    
    # Get the matrix
    matrix = rel_set.get_matrix()
    
    # Extract transition names (for rows and columns)
    transition_names = [t.name for t in transitions]

    output_matrix = []
    # Append the header row
    output_matrix.append([""] + transition_names)
    #print([""] + transition_names)
    # Append each row of the matrix with row headers
    for row_index, row in enumerate(matrix):
        row_data = [transition_names[row_index]] + [str(entry) for entry in row]
        output_matrix.append(row_data)
        #print(row_data)
    
    return output_matrix