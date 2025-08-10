#include <string>
#include <sstream>
#include <vector>
#include <cctype>

std::string protobufDebugStringToJson(const std::string& debugString) {
    std::stringstream result;
    bool inQuotes = false;
    bool expectingValue = false;
    bool needComma = false;
    
    for (size_t i = 0; i < debugString.length(); ++i) {
        char c = debugString[i];
        
        // Handle quotes
        if (c == '"') {
            inQuotes = !inQuotes;
            result << c;
            if (!inQuotes && expectingValue) {
                expectingValue = false;
                needComma = true;
            }
            continue;
        }
        
        // Inside quotes, copy everything
        if (inQuotes) {
            result << c;
            continue;
        }
        
        // Skip whitespace outside quotes
        if (std::isspace(c)) {
            continue;
        }
        
        // Handle colon
        if (c == ':') {
            result << "\":";
            expectingValue = true;
            needComma = false;
            continue;
        }
        
        // Handle opening brace
        if (c == '{') {
            if (expectingValue) {
                // This is a value object
                result << c;
                expectingValue = false;
                needComma = false;
            } else {
                // This is after a field name (like "User {")
                result << "\":{";
                expectingValue = false;
                needComma = false;
            }
            continue;
        }
        
        // Handle closing brace
        if (c == '}') {
            result << c;
            needComma = true;
            continue;
        }
        
        // Handle field names and values
        if (std::isalpha(c) || c == '_') {
            if (expectingValue) {
                // This is a value (could be true/false/null or unquoted string)
                std::string word;
                size_t j = i;
                while (j < debugString.length() && 
                       (std::isalnum(debugString[j]) || debugString[j] == '_' || 
                        debugString[j] == '.' || debugString[j] == '@' || debugString[j] == '-')) {
                    word += debugString[j];
                    j++;
                }
                
                // Check if it's a special keyword
                if (word == "true" || word == "false" || word == "null") {
                    result << word;
                } else {
                    result << "\"" << word << "\"";
                }
                
                i = j - 1;
                expectingValue = false;
                needComma = true;
            } else {
                // This is a field name
                if (needComma) {
                    result << ",";
                }
                result << "\"";
                while (i < debugString.length() && 
                       (std::isalnum(debugString[i]) || debugString[i] == '_')) {
                    result << debugString[i];
                    i++;
                }
                i--;
                needComma = false;
            }
            continue;
        }
        
        // Handle numbers
        if (std::isdigit(c) || (c == '-' && expectingValue)) {
            if (needComma && !expectingValue) {
                result << ",";
            }
            
            size_t j = i;
            while (j < debugString.length() && 
                   (std::isdigit(debugString[j]) || debugString[j] == '.' || 
                    debugString[j] == '-' || debugString[j] == 'e' || debugString[j] == 'E' || 
                    debugString[j] == '+')) {
                result << debugString[j];
                j++;
            }
            i = j - 1;
            expectingValue = false;
            needComma = true;
            continue;
        }
    }
    
    return "{" + result.str() + "}";
}