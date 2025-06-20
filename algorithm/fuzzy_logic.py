import numpy as np
from rdflib import Graph, Literal, RDF, URIRef, Namespace

class FuzzyLogic():
    FUZZY_RULES_TABLE = np.array([[1, 0, 0],
                                  [2, 1, 1],
                                  [4, 3, 2]])

    def __init__(self):
        self.membership_values_table = np.array([[0., 0., 0.],
                                                 [0., 0., 0.],
                                                 [0., 0., 0.]])
        self.fuzzified_decision = np.array([0., 0., 0., 0., 0.])
        self.fuzzy_sets_and_membership_values_of_height = {}
        self.fuzzy_sets_and_membership_values_of_weight = {}
        self.final_decision_on_body = None

    def do_fuzzification_of_height(self, height, sex):
        if sex == 0:
            if height < 160:
                self.fuzzy_sets_and_membership_values_of_height[0] = 1
            elif height >= 160 and height < 167.5:
                p1 = (2 * height - 320) / 15
                p0 = 1 - p1
                self.fuzzy_sets_and_membership_values_of_height[0] = p0
                self.fuzzy_sets_and_membership_values_of_height[1] = p1
            elif height >= 167.5 and height < 175:
                p2 = (2 * height - 335) / 15
                p1 = 1 - p2
                self.fuzzy_sets_and_membership_values_of_height[1] = p1
                self.fuzzy_sets_and_membership_values_of_height[2] = p2
            else:
                self.fuzzy_sets_and_membership_values_of_height[2] = 1
        else:
            if height < 150:
                self.fuzzy_sets_and_membership_values_of_height[0] = 1
            elif height >= 150 and height < 157.5:
                p1 = (2 * height - 300) / 15
                p0 = 1 - p1
                self.fuzzy_sets_and_membership_values_of_height[0] = p0
                self.fuzzy_sets_and_membership_values_of_height[1] = p1
            elif height >= 157.5 and height < 165:
                p2 = (2 * height - 315) / 15
                p1 = 1 - p2
                self.fuzzy_sets_and_membership_values_of_height[1] = p1
                self.fuzzy_sets_and_membership_values_of_height[2] = p2
            else:
                self.fuzzy_sets_and_membership_values_of_height[2] = 1

        print(f'Sex: {sex}')
        print(f'Height: {height}')
        print('Fuzzy Sets and their Membership Values of Height:')
        for key, value in self.fuzzy_sets_and_membership_values_of_height.items():
            print(f'Fuzzy Set: {key} - Membership Value: {value}')

    def do_fuzzification_of_weight(self, weight, sex):
        if sex == 0:
            if weight < 50:
                self.fuzzy_sets_and_membership_values_of_weight[0] = 1
            elif weight >= 50 and weight < 60:
                p1 = (2 * weight - 100) / 20
                p0 = 1 - p1
                self.fuzzy_sets_and_membership_values_of_weight[0] = p0
                self.fuzzy_sets_and_membership_values_of_weight[1] = p1
            elif weight >= 60 and weight < 70:
                p2 = (2 * weight - 120) / 20
                p1 = 1 - p2
                self.fuzzy_sets_and_membership_values_of_weight[1] = p1
                self.fuzzy_sets_and_membership_values_of_weight[2] = p2
            else:
                self.fuzzy_sets_and_membership_values_of_weight[2] = 1
        else:
            if weight < 45:
                self.fuzzy_sets_and_membership_values_of_weight[0] = 1
            elif weight >= 45 and weight < 50:
                p1 = (2 * weight - 90) / 10
                p0 = 1 - p1
                self.fuzzy_sets_and_membership_values_of_weight[0] = p0
                self.fuzzy_sets_and_membership_values_of_weight[1] = p1
            elif weight >= 50 and weight < 55:
                p2 = (2 * weight - 100) / 10
                p1 = 1 - p2
                self.fuzzy_sets_and_membership_values_of_weight[1] = p1
                self.fuzzy_sets_and_membership_values_of_weight[2] = p2
            else:
                self.fuzzy_sets_and_membership_values_of_weight[2] = 1

        print(f'Weight: {weight}')
        print(f'Fuzzy Sets and their Membership Values of Weight:')
        for key, value in self.fuzzy_sets_and_membership_values_of_weight.items():
            print(f'Fuzzy Set: {key} - Membership Value: {value}')

    def do_fuzzy_inference(self):
        fuzzy_sets_of_height = [fs for fs in self.fuzzy_sets_and_membership_values_of_height.keys()]
        membership_values_of_height = [mv for mv in self.fuzzy_sets_and_membership_values_of_height.values()]

        fuzzy_sets_of_weight = [fs for fs in self.fuzzy_sets_and_membership_values_of_weight.keys()]
        membership_values_of_weight = [mv for mv in self.fuzzy_sets_and_membership_values_of_weight.values()]

        for i in range(0, len(fuzzy_sets_of_weight)):
            for j in range(0, len(fuzzy_sets_of_height)):
                self.membership_values_table[fuzzy_sets_of_weight[i]][fuzzy_sets_of_height[j]] = min(
                    membership_values_of_weight[i], membership_values_of_height[j])

        print('Fuzzy Rules Table:')
        print(FuzzyLogic.FUZZY_RULES_TABLE)

        print('Membership Values Table:')
        print(self.membership_values_table)

        for i in range(0, 3):
            for j in range(0, 3):
                self.fuzzified_decision[FuzzyLogic.FUZZY_RULES_TABLE[i][j]] = max(
                    self.membership_values_table[i][j],
                    self.fuzzified_decision[FuzzyLogic.FUZZY_RULES_TABLE[i][j]])

        print('Fuzzified Decision:')
        print(self.fuzzified_decision)

    def do_defuzzification_of_body(self):
        max_val = 0
        self.final_decision_on_body = 0

        for i in range(0, 5):
            if self.fuzzified_decision[i] > max_val:
                max_val = self.fuzzified_decision[i]
                self.final_decision_on_body = i

        print(f'Final Decision on Body: {self.final_decision_on_body}')
        print('____________________________________________________________________')
        return self.final_decision_on_body

    def generate_semantic_description(self, person_id, height, weight, body_category):
        g = Graph()
        ex = Namespace("http://example.org/health#")
        g.bind("ex", ex)
        person = URIRef(f"http://example.org/person/{person_id}")
        g.add((person, RDF.type, ex.Person))
        g.add((person, ex.hasHeight, Literal(height)))
        g.add((person, ex.hasWeight, Literal(weight)))
        g.add((person, ex.hasBodyCategory, Literal(body_category)))

        print("\n\U0001F4D8 RDF Triples (Semantic Web Representation):")
        print(g.serialize(format="turtle"))

        return g

    def query_rdf_data(self, graph):
        query = """
            PREFIX ex: <http://example.org/health#>
            SELECT ?person ?height ?weight ?bodyCategory
            WHERE {
                ?person rdf:type ex:Person . 
                ?person ex:hasHeight ?height . 
                ?person ex:hasWeight ?weight . 
                ?person ex:hasBodyCategory ?bodyCategory . 
            }
        """
        results = graph.query(query)

        for row in results:
            print(f"Person: {row.person}, Height: {row.height}, Weight: {row.weight}, Body Category: {row.bodyCategory}")


if __name__ == "__main__":
    fl = FuzzyLogic()
    height = 160
    weight = 75
    fl.do_fuzzification_of_height(height, 0)
    fl.do_fuzzification_of_weight(weight, 0)
    fl.do_fuzzy_inference()
    result = fl.do_defuzzification_of_body()
    print(f"Final Decision on Body: {result}")

    rdf_graph = fl.generate_semantic_description("person1", height, weight, result)
    fl.query_rdf_data(rdf_graph)
