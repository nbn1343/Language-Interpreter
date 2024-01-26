from Interpreter.Header import Header
from Interpreter.Row import Row

class Relation:
    def __init__(self, name: str, header: Header, rows: set = None) -> None:
        self.name: str = name
        self.original_header: Header = header 
        self.header: Header = header
        if rows is None:
            rows = set()
        self.rows: set[Row] = rows
    
    def __str__(self) -> str:
        output_str:str = ""
        for row in sorted(self.rows):
            if len(row.values) == 0:
                continue
            sep: str = ""
            output_str += "  "
            for i in range(len(self.header.values)):
                output_str += sep
                output_str += self.header.values[i]
                output_str += "="
                output_str += row.values[i]
                sep = ", "
            output_str += "\n"

        return output_str
    
        
    def add_row(self, row: Row) -> None:
        if len(row.values) != len(self.header.values):
            raise ValueError(f"Row was not the same length as Header.")
        self.rows.add(row)
    
    def select1(self, value: str, colIndex: int) -> 'Relation':
        new_name = ""
        new_header = self.header
        new_tuples = set(row for row in self.rows if row.values[colIndex] == value)

        return Relation(new_name, new_header, new_tuples)
    
    def select2(self, index1: int, index2: int) -> 'Relation':
        new_name = self.name 
        if len(self.original_header.values) <= 2:
            new_header = Header([self.header.values[index1], self.header.values[index2]])
            new_tuples = set([row for row in self.rows if row.values[index1] == row.values[index2]])

            return Relation(new_name, new_header, new_tuples)
        else:
            new_header = self.original_header
            new_tuples = set([row for row in self.rows if row.values[index1] == row.values[index2]])

            return Relation(new_name, new_header, new_tuples)
        
    
    def rename(self, new_header: Header) -> 'Relation':
        new_name = self.name  
        new_tuples = self.rows  
    
        return Relation(new_name, new_header, new_tuples)

    def project(self, col_indexes: list[int]) -> 'Relation':
        new_name = self.name  # You may choose to keep the same name
        new_header = Header([self.header.values[i] for i in col_indexes])
        new_tuples = set(Row([row.values[i] for i in col_indexes]) for row in self.rows)
    
        return Relation(new_name, new_header, new_tuples)
    
    def can_join_rows(self, row1: Row, row2: Row, overlap: list[tuple[int,int]]) -> bool:
        for x, y in overlap:
            if row1.values[x] != row2.values[y]:
                return False
        return True
        
    def join_rows(self, row1: Row, row2: Row, unique_cols_1: list[int]) -> Row:
        new_row_values: list[str] = []
        for x in unique_cols_1:
            new_row_values.append(row1.values[x])
        new_row_values.extend(row2.values)
        return Row(new_row_values)
    
    def join_headers(self, header1: Header, header2: Header, unique_cols_1: list[int]) -> Header:
        new_header_values: list[str] = []
        for x in unique_cols_1:
            new_header_values.append(header1.values[x])
        new_header_values.extend(header2.values)
        return Header(new_header_values)
    
    def natural_join(self, other: 'Relation') -> 'Relation':
        r1: Relation = self
        r2: Relation = other
        
        overlap: list[tuple(int,int)] = []
        unique_cols_1: list[int] = []
        
        # calculate the correct values for overlap, and unique_cols_
        for x in range(len(r1.header.values)):
            is_unique = True
            for y in range(len(r2.header.values)):
                if r1.header.values[x] == r2.header.values[y]:
                    overlap.append(tuple([x,y]))
                    is_unique = False
            if is_unique:
                unique_cols_1.append(x)
                    
        # make the header h for the result relation
        #     (combine r1's header with r2's header)
        h: Header = self.join_headers(r1.header, r2.header, unique_cols_1)
        result: Relation = Relation(r1.name + "|x|" + r2.name, h, set())
        for t1 in r1.rows:
            for t2 in r2.rows:
                if self.can_join_rows(t1,t2,overlap):
                    result_row = self.join_rows(t1,t2,unique_cols_1)
                    result.add_row(result_row)
                
        
        return result
    

    def union(self, other: 'Relation') -> 'Relation':
        # Ensure that the headers are compatible
        # if self.header != other.header:
        #     raise ValueError("Headers of relations are not compatible for union operation.")

        # Create a new relation with the same name and header
        result_name = f"{''}"
        result_header = self.header
        result_relation = Relation(result_name, result_header, set())

        # Add all rows from the first relation
        for row in self.rows:
            result_relation.add_row(row)

        # # Add rows from the second relation that are not already present
        for row in other.rows:
            if row not in self.rows:
                result_relation.add_row(row)


        return result_relation