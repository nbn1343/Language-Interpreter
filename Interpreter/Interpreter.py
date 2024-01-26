from Interpreter.Relation import Relation
from Interpreter.Row import Row
from Interpreter.Header import Header
from typing import Dict
from Parser.project_2_classes.datalog_program import DatalogProgram
from Parser.project_2_classes.predicate import Predicate
from Parser.project_2_classes.parser import Parser

 

class Interpreter:
    def __init__(self) -> None:
        self.output_str: str = ""
        self.database: Dict[str, Relation] = {}
        self.datalog_program = DatalogProgram
        self.dependency_graph_storage: Dict[str, list[str]] = {}
        self.reverse_dependency_graph_storage: Dict[str,list[str]] = {}
        pass
    
    def run(self, datalog_program: DatalogProgram) -> str:
        self.datalog_program: DatalogProgram = datalog_program
        self.interpret_schemes()
        self.interpret_facts()
        # self.interpret_rules()
        self.output_str += self.dependency_graph()
        self.reverse_dependency_graph()
        # post_order = self.dfs_forest()
        # sccs = self.find_sccs()
        self.output_str += "\n"
        self.output_str += self.interpret_rules()
        self.output_str += self.interpret_queries()
        return self.output_str
    
    def interpret_schemes(self) -> None:
        self.database: Dict[str, Relation] = {}

        for scheme in self.datalog_program.schemes:
            header = Header(scheme.parameters)
            relation = Relation(scheme.name, header)
            self.database[scheme.name] = relation
        # print(relation)

        return None
    
    def interpret_facts(self) -> None:
        for fact in self.datalog_program.facts:
            relation = self.database[fact.name]

            if relation is not None:
                new_tuple = Row(fact.parameters)
                relation.add_row(new_tuple)

            else:
                print(f"Warning: Fact predicate '{fact.name}' not found in the database.")

        return None
    
    def interpret_queries(self) -> None:
        output_str = ["\nQuery Evaluation"]
        for query in self.datalog_program.queries:
            result_relation = self.evaluate_predicate(query)
            output_str.append(f"{query.to_string()}? ")

            if not result_relation.rows:
                output_str[-1] += "No"
            else:
                output_str[-1] += f"Yes({len(result_relation.rows)})"

                for row in sorted(result_relation.rows):
                    formatted_values = ", ".join(f"{attr}={val}" for attr, val in zip(result_relation.header.values, row.values))
                    if formatted_values:
                        output_str.append("  " + formatted_values)

        return "\n".join(output_str)
        
    
    def evaluate_predicate(self, predicate: Predicate) -> Relation:
        relation = self.database.get(predicate.name)

        
        if relation is None:
            print(f"Warning: Relation '{predicate.name}' not found in the database.")
            return Relation("", Header([]))
        bindings = {}
        headers = []
        column_indexes = []
        for i, param in enumerate(predicate.parameters):
            if "'" in param:           
                relation = relation.select1(param, i)
            else:
                if param in headers:
                    relation = relation.select2(bindings[param],i)
                else:
                    bindings[param] = i
                    headers.append(param)
                    column_indexes.append(i)


        

        # project_indices = list(bindings.values())

        relation = relation.project(column_indexes)
        relation = relation.rename(Header(headers))
        
        return relation
    
    def dependency_graph(self) -> str:
        output_lines = ["Dependency Graph"]
        for i, rule in enumerate(self.datalog_program.rules):
            rule_str = i

            if rule_str not in self.dependency_graph_storage:
                self.dependency_graph_storage[rule_str] = set()

            for body_predicate in rule.body_predicates:
                for j, other_rule in enumerate(self.datalog_program.rules):
                    other_rule_str = j
                    if body_predicate.name == other_rule.head_predicate.name:
                        self.dependency_graph_storage[rule_str].add(other_rule_str)
                
        for rule, dependencies in sorted(self.dependency_graph_storage.items()):
            formatted_dependencies = [f"R{dep}" for dep in dependencies]
            output_lines.append(f"R{rule}:{','.join(formatted_dependencies)}")
        return "\n".join(output_lines)
    
    def reverse_dependency_graph(self) -> None:
        for rule, dependencies in self.dependency_graph_storage.items():
            for dependency in dependencies:
                if dependency not in self.reverse_dependency_graph_storage:
                    self.reverse_dependency_graph_storage[dependency] = set()
                self.reverse_dependency_graph_storage[dependency].add(rule)

            # Add rules with no dependencies to the reverse graph with an empty set
            if rule not in self.reverse_dependency_graph_storage:
                self.reverse_dependency_graph_storage[rule] = set()



    def dfs_forest(self) -> list[str]:
        post_order = []
        visited = set()
        real_stack = []

        def dfs(node):
            nonlocal visited, post_order, real_stack


            if node in visited:
                return
            visited.add(node)

            neighbors = sorted(self.reverse_dependency_graph_storage.get(node, []))
            for neighbor in neighbors:
                if neighbor not in visited:
                    dfs(neighbor)

            real_stack.append(node)

            return


        for node in sorted(list(self.reverse_dependency_graph_storage.keys())):
            if node not in visited:
                dfs(node)
        while len(real_stack) > 0:
            post_order.append(real_stack.pop())

        return post_order


        
    def find_sccs(self) -> list[set[str]]:
        post_order = self.dfs_forest()
        visited = set()
        sccs = []

        def dfs_scc(node, scc):
            nonlocal visited

            visited.add(node)
            scc.add(node)

            for neighbor in self.dependency_graph_storage.get(node, []):
                if neighbor not in visited:
                    dfs_scc(neighbor, scc)

        for node in post_order:
            if node not in visited:
                scc = set()
                dfs_scc(node, scc)
                sccs.append(scc)

        return sccs



    def interpret_rules(self) -> str:
        sccs = self.find_sccs()
        visited_scc = set()

        output_lines = ["\nRule Evaluation\n"]

        pass_counter = 0
        max_passes = 100  
        self_dependent = False


        for rule_id,rule_dependencies in self.dependency_graph_storage.items():
            if rule_id in rule_dependencies:
                self_dependent = True
        

        if len(self.dependency_graph_storage) == 1 and not self_dependent:
            
       
            for rule_id, rule_dependencies in self.dependency_graph_storage.items():
                rule = self.datalog_program.rules[rule_id]  
                result_relation = self.evaluate_rule(rule)
                head_string = rule.head_predicate.to_string()
                body_strings = [body.to_string() for body in rule.body_predicates]                           
                rule_str = f"{head_string} :- {','.join(body_strings)}."
                output_lines.append(f"SCC: R{rule_id}\n")
                output_lines.append(rule_str + "\n")
                output_lines.append(result_relation.__str__())
                output_lines.append(f"1 passes: R{rule_id}\n")
        else:
            for scc in sccs:
                passes = 0
                scc_tuple = tuple(scc)
                if scc_tuple not in visited_scc:
                    output_lines.append(f"SCC: {','.join(sorted(map(lambda x: f'R{x}', scc)))}\n")
                    changes_occurred = True  
                    while pass_counter < max_passes and changes_occurred:
                        passes += 1
                        changes_occurred = False
                        special_case_condition_met = False 
                        for rule_id in sorted(scc):
                            rule = self.datalog_program.rules[rule_id]  
                            
                            self_dependent = rule_id in self.dependency_graph_storage[rule_id]

                            
                            dependencies = self.dependency_graph_storage[rule_id]
                            depends_on_others = any(dep not in visited_scc for dep in dependencies)

                            if len(scc) == 1 and not self_dependent:
                                result_relation = self.evaluate_rule(rule)
                                head_string = rule.head_predicate.to_string()
                                body_strings = [body.to_string() for body in rule.body_predicates]                           
                                rule_str = f"{head_string} :- {','.join(body_strings)}."
                                output_lines.append(rule_str + "\n")
                                output_lines.append(result_relation.__str__())
                                # passes += 1
                                
                                if len(result_relation.rows) > 0:
                                    special_case_condition_met = True
                                    
                            elif not self_dependent or depends_on_others:
                                result_relation = self.evaluate_rule(rule)
                                head_string = rule.head_predicate.to_string()
                                body_strings = [body.to_string() for body in rule.body_predicates]                           
                                rule_str = f"{head_string} :- {','.join(body_strings)}."
                                output_lines.append(rule_str + "\n")
                                output_lines.append(result_relation.__str__())
                                # passes += 1
                                

                                if len(result_relation.rows) > 0:
                                    changes_occurred = True
                                    
                                    

                        visited_scc.add(scc_tuple)
                        

                        if special_case_condition_met:
                            break  
                    if changes_occurred:
                        pass_counter += 1

                    output_lines.append(f"{passes} passes: {','.join(sorted(map(lambda x: f'R{x}', scc)))}\n")

        return "".join(output_lines)


    def evaluate_rule(self, rule: Predicate) -> int:
        # Step 1: Evaluate the predicates on the right-hand side of the rule (the body predicates):
        intermediate_results = []
        for body_predicate in rule.body_predicates:
            result = self.evaluate_predicate(body_predicate)
            intermediate_results.append(result)
        
            

        # Step 2: Join the relations that result:
        if len(intermediate_results) > 1:
            joined_result = self.join_relations(intermediate_results)
        else:
            joined_result = intermediate_results[0]

        # Step 3: Project the columns that appear in the head predicate:
        projected_result = self.project_columns(joined_result, rule.head_predicate)

        # Step 4: Rename the relation to make it union-compatible:
        renamed_result = self.rename_relation(projected_result, rule.head_predicate)
        # print(renamed_result)

        # Step 5: Union with the relation in the database:
        union_result = self.union_relations(renamed_result, rule.head_predicate.name)

        return union_result
    

    def join_relations(self, relations: list['Relation']) -> 'Relation':
        # Implement the logic to join multiple relations
        result = relations[0]
        for i in range(1, len(relations)):
            result = result.natural_join(relations[i])
        return result
    
    def project_columns(self, relation: 'Relation', head_predicate: Predicate) -> 'Relation':
        # Implement the logic to project columns based on the head predicate
        # Assuming head_predicate.parameters contains variable names
        head_variables = head_predicate.parameters

    # Extract variable names from result relation header
        result_variables = relation.header.values

        # project_indices = list(result_variables.values())

    # Identify the column indexes corresponding to head variables in the result relation
        col_indexes = [result_variables.index(variable) for variable in head_variables]

    # Use the existing 'project' method to perform the projection
        new_result = relation.project(col_indexes)
        # print(new_result)

        return new_result

    def rename_relation(self, relation: 'Relation', head_predicate: Predicate) -> 'Relation':
        # Implement the logic to rename columns in the relation
        # Assuming head_predicate.parameters contains variable names
        existing_relation = self.database[head_predicate.name]
        new_header = Header(existing_relation.original_header.values)
        return relation.rename(new_header)

    def union_relations(self, relation: 'Relation', relation_name: str) -> 'Relation':
        if relation_name in self.database:
            existing_relation = self.database[relation_name]
            new_rows = set()
            for row in relation.rows:
                if row not in existing_relation.rows:
                    existing_relation.rows.add(row)
                    new_rows.add(row)
            return Relation(existing_relation.name, existing_relation.header, new_rows)
        else:
        # Handle case where relation_name is not in the database
            self.database[relation_name] = relation  # Add the new relation to the database
            return relation

    def get_relation(self, relation_name: str) -> 'Relation':
        # Implement the logic to get the relation from the database
        if relation_name in self.database:
            return self.database[relation_name]
        else:
            # Handle case where relation_name is not in the database
            return Relation("Empty", Header([]), set())