#include <string>
#include <map>
#include <vector>
#include <memory>
#include <sstream>
#include <cctype>
#include <variant>
#include <iostream>

// Python-like dict implementation using std::variant
class PyDict {
public:
    using Value = std::variant<
        std::nullptr_t,                    // null
        bool,                               // boolean
        int,                                // integer
        double,                             // float
        std::string,                        // string
        std::shared_ptr<PyDict>,            // nested dict
        std::vector<std::shared_ptr<PyDict>> // list of dicts
    >;
    
private:
    std::map<std::string, Value> data;
    
public:
    void set(const std::string& key, const Value& value) {
        data[key] = value;
    }
    
    Value get(const std::string& key) const {
        auto it = data.find(key);
        if (it != data.end()) {
            return it->second;
        }
        return nullptr;
    }
    
    std::string toJson() const {
        std::stringstream ss;
        ss << "{";
        bool first = true;
        
        for (const auto& [key, value] : data) {
            if (!first) {
                ss << ",";
            }
            first = false;
            
            ss << "\"" << key << "\":";
            ss << valueToJson(value);
        }
        
        ss << "}";
        return ss.str();
    }
    
private:
    std::string valueToJson(const Value& value) const {
        return std::visit([](const auto& v) -> std::string {
            using T = std::decay_t<decltype(v)>;
            
            if constexpr (std::is_same_v<T, std::nullptr_t>) {
                return "null";
            } else if constexpr (std::is_same_v<T, bool>) {
                return v ? "true" : "false";
            } else if constexpr (std::is_same_v<T, int>) {
                return std::to_string(v);
            } else if constexpr (std::is_same_v<T, double>) {
                // Format double without trailing zeros
                std::stringstream ss;
                ss << v;
                return ss.str();
            } else if constexpr (std::is_same_v<T, std::string>) {
                return "\"" + v + "\"";
            } else if constexpr (std::is_same_v<T, std::shared_ptr<PyDict>>) {
                return v ? v->toJson() : "null";
            } else if constexpr (std::is_same_v<T, std::vector<std::shared_ptr<PyDict>>>) {
                std::stringstream ss;
                ss << "[";
                bool first = true;
                for (const auto& item : v) {
                    if (!first) ss << ",";
                    first = false;
                    ss << (item ? item->toJson() : "null");
                }
                ss << "]";
                return ss.str();
            }
            return "null";
        }, value);
    }
};

// Parser for protobuf debug string
class ProtobufParser {
private:
    std::string input;
    size_t pos;
    
public:
    ProtobufParser(const std::string& str) : input(str), pos(0) {}
    
    std::shared_ptr<PyDict> parse() {
        auto result = std::make_shared<PyDict>();
        skipWhitespace();
        
        // Check if it starts with a type name (like "User {")
        if (isAlpha(peek())) {
            std::string typeName = readIdentifier();
            skipWhitespace();
            
            if (peek() == '{') {
                pos++; // consume '{'
                auto nested = parseObject();
                result->set(typeName, nested);
                skipWhitespace();
                if (peek() == '}') {
                    pos++; // consume '}'
                }
            } else {
                // It's a regular field
                pos -= typeName.length(); // backtrack
                parseFields(result);
            }
        } else {
            parseFields(result);
        }
        
        return result;
    }
    
private:
    void parseFields(std::shared_ptr<PyDict> dict) {
        while (pos < input.length()) {
            skipWhitespace();
            
            if (peek() == '}' || pos >= input.length()) {
                break;
            }
            
            // Read field name
            std::string fieldName = readIdentifier();
            if (fieldName.empty()) break;
            
            skipWhitespace();
            
            // Expect ':'
            if (peek() == ':') {
                pos++; // consume ':'
                skipWhitespace();
                
                // Read value
                auto value = readValue();
                dict->set(fieldName, value);
            } else if (peek() == '{') {
                // Field with nested object (like "address {")
                pos++; // consume '{'
                auto nested = parseObject();
                dict->set(fieldName, nested);
                skipWhitespace();
                if (peek() == '}') {
                    pos++; // consume '}'
                }
            }
        }
    }
    
    std::shared_ptr<PyDict> parseObject() {
        auto obj = std::make_shared<PyDict>();
        parseFields(obj);
        return obj;
    }
    
    PyDict::Value readValue() {
        skipWhitespace();
        char c = peek();
        
        if (c == '"') {
            return readQuotedString();
        } else if (c == '{') {
            pos++; // consume '{'
            auto nested = parseObject();
            skipWhitespace();
            if (peek() == '}') {
                pos++; // consume '}'
            }
            return nested;
        } else if (std::isdigit(c) || c == '-' || c == '.') {
            return readNumber();
        } else if (isAlpha(c)) {
            std::string word = readIdentifier();
            if (word == "true") return true;
            if (word == "false") return false;
            if (word == "null") return nullptr;
            return word; // unquoted string
        }
        
        return nullptr;
    }
    
    std::string readQuotedString() {
        std::string result;
        pos++; // skip opening quote
        
        while (pos < input.length() && input[pos] != '"') {
            if (input[pos] == '\\' && pos + 1 < input.length()) {
                pos++;
                result += input[pos];
            } else {
                result += input[pos];
            }
            pos++;
        }
        
        if (pos < input.length()) {
            pos++; // skip closing quote
        }
        
        return result;
    }
    
    PyDict::Value readNumber() {
        std::string numStr;
        bool hasDecimal = false;
        
        while (pos < input.length() && 
               (std::isdigit(input[pos]) || input[pos] == '.' || 
                input[pos] == '-' || input[pos] == 'e' || input[pos] == 'E' || input[pos] == '+')) {
            if (input[pos] == '.') {
                hasDecimal = true;
            }
            numStr += input[pos];
            pos++;
        }
        
        if (hasDecimal || numStr.find('e') != std::string::npos || numStr.find('E') != std::string::npos) {
            return std::stod(numStr);
        } else {
            return std::stoi(numStr);
        }
    }
    
    std::string readIdentifier() {
        std::string result;
        
        while (pos < input.length() && (isAlpha(input[pos]) || std::isdigit(input[pos]) || input[pos] == '_')) {
            result += input[pos];
            pos++;
        }
        
        return result;
    }
    
    void skipWhitespace() {
        while (pos < input.length() && std::isspace(input[pos])) {
            pos++;
        }
    }
    
    char peek() const {
        if (pos < input.length()) {
            return input[pos];
        }
        return '\0';
    }
    
    bool isAlpha(char c) const {
        return std::isalpha(c) || c == '_';
    }
};

// Main conversion function
std::string protobufDebugStringToJson(const std::string& debugString) {
    ProtobufParser parser(debugString);
    auto dict = parser.parse();
    return dict->toJson();
}