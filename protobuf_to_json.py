import json
import re
from typing import Any, Dict, List, Union, Optional


class ProtobufParser:
    def __init__(self, debug_string: str):
        self.input = debug_string
        self.pos = 0
    
    def parse(self) -> Dict[str, Any]:
        result = {}
        self.skip_whitespace()
        
        # Parse all top-level items
        while self.pos < len(self.input):
            self.skip_whitespace()
            if self.pos >= len(self.input):
                break
                
            # Check if it starts with a type name (like "User {")
            if self.is_alpha(self.peek()):
                start_pos = self.pos
                type_name = self.read_identifier()
                self.skip_whitespace()
                
                if self.peek() == '{':
                    self.pos += 1  # consume '{'
                    nested = self.parse_object()
                    result[type_name] = nested
                    self.skip_whitespace()
                    if self.peek() == '}':
                        self.pos += 1  # consume '}'
                elif self.peek() == ':':
                    # It's a regular field
                    self.pos = start_pos  # backtrack
                    field_name = self.read_identifier()
                    self.skip_whitespace()
                    if self.peek() == ':':
                        self.pos += 1  # consume ':'
                        self.skip_whitespace()
                        value = self.read_value()
                        result[field_name] = value
                else:
                    break
            else:
                break
        
        return result
    
    def parse_fields(self, result: Dict[str, Any]) -> None:
        while self.pos < len(self.input):
            self.skip_whitespace()
            
            if self.peek() == '}' or self.pos >= len(self.input):
                break
            
            # Read field name
            field_name = self.read_identifier()
            if not field_name:
                break
            
            self.skip_whitespace()
            
            # Check for ':' or '{'
            if self.peek() == ':':
                self.pos += 1  # consume ':'
                self.skip_whitespace()
                
                # Read value
                value = self.read_value()
                result[field_name] = value
            elif self.peek() == '{':
                # Field with nested object (like "address {")
                self.pos += 1  # consume '{'
                nested = self.parse_object()
                result[field_name] = nested
                self.skip_whitespace()
                if self.peek() == '}':
                    self.pos += 1  # consume '}'
    
    def parse_object(self) -> Dict[str, Any]:
        obj = {}
        self.parse_fields(obj)
        return obj
    
    def read_value(self) -> Any:
        self.skip_whitespace()
        c = self.peek()
        
        if c == '"':
            return self.read_quoted_string()
        elif c == '{':
            self.pos += 1  # consume '{'
            nested = self.parse_object()
            self.skip_whitespace()
            if self.peek() == '}':
                self.pos += 1  # consume '}'
            return nested
        elif c and (c.isdigit() or c in '-.'):
            return self.read_number()
        elif self.is_alpha(c):
            word = self.read_identifier()
            if word == 'true':
                return True
            elif word == 'false':
                return False
            elif word == 'null':
                return None
            else:
                return word  # unquoted string
        
        return None
    
    def read_quoted_string(self) -> str:
        result = []
        self.pos += 1  # skip opening quote
        
        while self.pos < len(self.input) and self.input[self.pos] != '"':
            if self.input[self.pos] == '\\' and self.pos + 1 < len(self.input):
                self.pos += 1
                # Handle escape sequences
                escape_char = self.input[self.pos]
                if escape_char == 'n':
                    result.append('\n')
                elif escape_char == 't':
                    result.append('\t')
                elif escape_char == 'r':
                    result.append('\r')
                elif escape_char == '\\':
                    result.append('\\')
                elif escape_char == '"':
                    result.append('"')
                else:
                    result.append(escape_char)
            else:
                result.append(self.input[self.pos])
            self.pos += 1
        
        if self.pos < len(self.input):
            self.pos += 1  # skip closing quote
        
        return ''.join(result)
    
    def read_number(self) -> Union[int, float]:
        num_str = []
        has_decimal = False
        
        while self.pos < len(self.input):
            c = self.input[self.pos]
            if c.isdigit() or c in '.+-eE':
                if c == '.':
                    has_decimal = True
                num_str.append(c)
                self.pos += 1
            else:
                break
        
        num_str = ''.join(num_str)
        
        if has_decimal or 'e' in num_str.lower():
            return float(num_str)
        else:
            return int(num_str)
    
    def read_identifier(self) -> str:
        result = []
        
        # Must start with alpha or underscore
        if self.pos < len(self.input) and self.is_alpha(self.input[self.pos]):
            while self.pos < len(self.input):
                c = self.input[self.pos]
                if c.isalnum() or c == '_':
                    result.append(c)
                    self.pos += 1
                else:
                    break
        
        return ''.join(result)
    
    def skip_whitespace(self) -> None:
        while self.pos < len(self.input) and self.input[self.pos].isspace():
            self.pos += 1
    
    def peek(self) -> Optional[str]:
        if self.pos < len(self.input):
            return self.input[self.pos]
        return None
    
    def is_alpha(self, c: Optional[str]) -> bool:
        return c is not None and (c.isalpha() or c == '_')


def protobuf_debug_string_to_json(debug_string: str) -> str:
    """
    Convert a protobuf debug string to JSON format.
    
    Args:
        debug_string: The protobuf debug string to convert
    
    Returns:
        A JSON string representation of the parsed data
    """
    parser = ProtobufParser(debug_string)
    result = parser.parse()
    return json.dumps(result, indent=2)


def protobuf_debug_string_to_dict(debug_string: str) -> Dict[str, Any]:
    """
    Convert a protobuf debug string to a Python dictionary.
    
    Args:
        debug_string: The protobuf debug string to convert
    
    Returns:
        A dictionary representation of the parsed data
    """
    parser = ProtobufParser(debug_string)
    return parser.parse()


# Example usage and test cases
if __name__ == "__main__":
    # Test case 1: Simple fields
    test1 = """
    name: "John Doe"
    age: 30
    is_active: true
    """
    
    print("Test 1 - Simple fields:")
    result1 = protobuf_debug_string_to_dict(test1)
    print(json.dumps(result1, indent=2))
    print()
    
    # Test case 2: Nested object
    test2 = """
    name: "John Doe"
    address {
        street: "123 Main St"
        city: "New York"
        zip: 10001
    }
    """
    
    print("Test 2 - Nested object:")
    result2 = protobuf_debug_string_to_dict(test2)
    print(json.dumps(result2, indent=2))
    print()
    
    # Test case 3: Type with nested content
    test3 = """
    User {
        id: 123
        name: "Alice"
        email: "alice@example.com"
    }
    """
    
    print("Test 3 - Type with nested content:")
    result3 = protobuf_debug_string_to_dict(test3)
    print(json.dumps(result3, indent=2))
    print()
    
    # Test case 4: Complex nested structure
    test4 = """
    user_id: 456
    profile {
        name: "Bob Smith"
        age: 25
        settings {
            notifications: true
            theme: "dark"
        }
    }
    score: 95.5
    """
    
    print("Test 4 - Complex nested structure:")
    result4 = protobuf_debug_string_to_dict(test4)
    print(json.dumps(result4, indent=2))