import unittest
import json
from protobuf_to_json import ProtobufParser, protobuf_debug_string_to_json, protobuf_debug_string_to_dict


class TestProtobufParser(unittest.TestCase):
    
    def test_simple_string_field(self):
        """Test parsing simple string fields"""
        debug_str = 'name: "John Doe"'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result, {"name": "John Doe"})
    
    def test_simple_integer_field(self):
        """Test parsing integer fields"""
        debug_str = 'age: 30'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result, {"age": 30})
    
    def test_simple_float_field(self):
        """Test parsing float fields"""
        debug_str = 'score: 95.5'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result, {"score": 95.5})
    
    def test_boolean_true(self):
        """Test parsing boolean true value"""
        debug_str = 'is_active: true'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result, {"is_active": True})
    
    def test_boolean_false(self):
        """Test parsing boolean false value"""
        debug_str = 'is_active: false'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result, {"is_active": False})
    
    def test_null_value(self):
        """Test parsing null value"""
        debug_str = 'data: null'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result, {"data": None})
    
    def test_unquoted_string(self):
        """Test parsing unquoted string values"""
        debug_str = 'status: ACTIVE'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result, {"status": "ACTIVE"})
    
    def test_multiple_fields(self):
        """Test parsing multiple fields"""
        debug_str = '''
        name: "Alice"
        age: 25
        is_admin: false
        '''
        result = protobuf_debug_string_to_dict(debug_str)
        expected = {
            "name": "Alice",
            "age": 25,
            "is_admin": False
        }
        self.assertEqual(result, expected)
    
    def test_nested_object(self):
        """Test parsing nested objects"""
        debug_str = '''
        name: "Bob"
        address {
            street: "123 Main St"
            city: "New York"
            zip: 10001
        }
        '''
        result = protobuf_debug_string_to_dict(debug_str)
        expected = {
            "name": "Bob",
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "zip": 10001
            }
        }
        self.assertEqual(result, expected)
    
    def test_deeply_nested_objects(self):
        """Test parsing deeply nested objects"""
        debug_str = '''
        user {
            profile {
                settings {
                    theme: "dark"
                    notifications: true
                }
                name: "Charlie"
            }
        }
        '''
        result = protobuf_debug_string_to_dict(debug_str)
        expected = {
            "user": {
                "profile": {
                    "settings": {
                        "theme": "dark",
                        "notifications": True
                    },
                    "name": "Charlie"
                }
            }
        }
        self.assertEqual(result, expected)
    
    def test_type_with_nested_content(self):
        """Test parsing type declarations with nested content"""
        debug_str = '''
        User {
            id: 123
            email: "user@example.com"
        }
        '''
        result = protobuf_debug_string_to_dict(debug_str)
        expected = {
            "User": {
                "id": 123,
                "email": "user@example.com"
            }
        }
        self.assertEqual(result, expected)
    
    def test_escaped_characters_in_string(self):
        """Test parsing strings with escape sequences"""
        debug_str = r'message: "Hello\nWorld\t\"quoted\""'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result, {"message": 'Hello\nWorld\t"quoted"'})
    
    def test_scientific_notation(self):
        """Test parsing numbers in scientific notation"""
        debug_str = 'value: 1.23e-4'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertAlmostEqual(result["value"], 0.000123, places=6)
    
    def test_negative_numbers(self):
        """Test parsing negative numbers"""
        debug_str = '''
        temperature: -15.5
        debt: -1000
        '''
        result = protobuf_debug_string_to_dict(debug_str)
        expected = {
            "temperature": -15.5,
            "debt": -1000
        }
        self.assertEqual(result, expected)
    
    def test_empty_string(self):
        """Test parsing empty string value"""
        debug_str = 'message: ""'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result, {"message": ""})
    
    def test_empty_object(self):
        """Test parsing empty nested object"""
        debug_str = '''
        data {
        }
        '''
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result, {"data": {}})
    
    def test_mixed_field_types(self):
        """Test parsing mixed field types in one object"""
        debug_str = '''
        string_field: "text"
        int_field: 42
        float_field: 3.14
        bool_field: true
        null_field: null
        unquoted_field: ENUM_VALUE
        nested_field {
            inner: "value"
        }
        '''
        result = protobuf_debug_string_to_dict(debug_str)
        expected = {
            "string_field": "text",
            "int_field": 42,
            "float_field": 3.14,
            "bool_field": True,
            "null_field": None,
            "unquoted_field": "ENUM_VALUE",
            "nested_field": {
                "inner": "value"
            }
        }
        self.assertEqual(result, expected)
    
    def test_whitespace_handling(self):
        """Test handling of various whitespace patterns"""
        debug_str = '''
            field1   :   "value1"   
            field2:123
            field3  :  true  
        '''
        result = protobuf_debug_string_to_dict(debug_str)
        expected = {
            "field1": "value1",
            "field2": 123,
            "field3": True
        }
        self.assertEqual(result, expected)
    
    def test_field_names_with_underscores(self):
        """Test field names containing underscores"""
        debug_str = '''
        user_name: "John"
        is_active_user: true
        total_score_value: 100
        '''
        result = protobuf_debug_string_to_dict(debug_str)
        expected = {
            "user_name": "John",
            "is_active_user": True,
            "total_score_value": 100
        }
        self.assertEqual(result, expected)
    
    def test_json_output_format(self):
        """Test that protobuf_debug_string_to_json returns valid JSON"""
        debug_str = '''
        name: "Test"
        value: 42
        '''
        json_str = protobuf_debug_string_to_json(debug_str)
        
        # Verify it's valid JSON by parsing it
        parsed = json.loads(json_str)
        expected = {
            "name": "Test",
            "value": 42
        }
        self.assertEqual(parsed, expected)
        
        # Verify it has indentation (pretty printed)
        self.assertIn('\n', json_str)
    
    def test_complex_real_world_example(self):
        """Test a complex real-world protobuf debug string"""
        debug_str = '''
        Person {
            id: 12345
            name: "John Smith"
            email: "john.smith@example.com"
            phones {
                number: "+1-555-0100"
                type: "MOBILE"
            }
            phones {
                number: "+1-555-0101"
                type: "HOME"
            }
            address {
                street: "123 Main Street"
                city: "Springfield"
                state: "IL"
                zip: 62701
                country: "USA"
                location {
                    latitude: 39.7817
                    longitude: -89.6501
                }
            }
            is_verified: true
            created_at: 1609459200
            metadata {
                source: "web_signup"
                version: 2
            }
        }
        '''
        result = protobuf_debug_string_to_dict(debug_str)
        
        # Verify structure
        self.assertIn("Person", result)
        person = result["Person"]
        self.assertEqual(person["id"], 12345)
        self.assertEqual(person["name"], "John Smith")
        self.assertTrue(person["is_verified"])
        
        # Verify nested structures
        self.assertIn("address", person)
        self.assertEqual(person["address"]["city"], "Springfield")
        self.assertIn("location", person["address"])
        self.assertEqual(person["address"]["location"]["latitude"], 39.7817)
        
        # Note: The current implementation doesn't handle repeated fields (multiple phones)
        # This would need additional logic to detect and handle as arrays
    
    def test_unicode_characters(self):
        """Test handling of unicode characters in strings"""
        debug_str = 'name: "Hello 世界 🌍"'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result, {"name": "Hello 世界 🌍"})
    
    def test_very_long_string(self):
        """Test parsing very long string values"""
        long_text = "a" * 1000
        debug_str = f'content: "{long_text}"'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result["content"], long_text)
    
    def test_special_characters_in_string(self):
        """Test various special characters in strings"""
        debug_str = r'text: "Special chars: !@#$%^&*()_+-=[]{}|;:,.<>?/"'
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertEqual(result["text"], "Special chars: !@#$%^&*()_+-=[]{}|;:,.<>?/")


class TestEdgeCases(unittest.TestCase):
    
    def test_empty_input(self):
        """Test parsing empty input"""
        result = protobuf_debug_string_to_dict("")
        self.assertEqual(result, {})
    
    def test_whitespace_only_input(self):
        """Test parsing input with only whitespace"""
        result = protobuf_debug_string_to_dict("   \n\t  ")
        self.assertEqual(result, {})
    
    def test_malformed_nested_object(self):
        """Test handling of unclosed nested objects"""
        debug_str = '''
        data {
            field: "value"
        '''
        # Should still parse what it can
        result = protobuf_debug_string_to_dict(debug_str)
        self.assertIn("data", result)
        self.assertEqual(result["data"]["field"], "value")
    
    def test_consecutive_nested_objects(self):
        """Test multiple nested objects at the same level"""
        debug_str = '''
        first {
            value: 1
        }
        second {
            value: 2
        }
        '''
        result = protobuf_debug_string_to_dict(debug_str)
        expected = {
            "first": {"value": 1},
            "second": {"value": 2}
        }
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)