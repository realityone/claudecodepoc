#include <iostream>
#include <string>
#include <cassert>
#include "protobuf_to_json.cpp"

void testUserConversion() {
    // 输入的 protobuf ShortDebugString
    std::string input = "User { id: 123 name: \"John Doe\" email: \"john.doe@example.com\" }";
    
    // 期望的 JSON 输出
    std::string expected = "{\"User\":{\"id\":123,\"name\":\"John Doe\",\"email\":\"john.doe@example.com\"}}";
    
    // 执行转换
    std::string result = protobufDebugStringToJson(input);
    
    // 验证结果
    if (result == expected) {
        std::cout << "✓ Test passed!" << std::endl;
        std::cout << "Input:    " << input << std::endl;
        std::cout << "Expected: " << expected << std::endl;
        std::cout << "Result:   " << result << std::endl;
    } else {
        std::cout << "✗ Test failed!" << std::endl;
        std::cout << "Input:    " << input << std::endl;
        std::cout << "Expected: " << expected << std::endl;
        std::cout << "Result:   " << result << std::endl;
        assert(false);
    }
}

void testAdditionalCases() {
    // 测试用例 1: 简单字段
    {
        std::string input = "id: 123 name: \"John\"";
        std::string expected = "{\"id\":123,\"name\":\"John\"}";
        std::string result = protobufDebugStringToJson(input);
        assert(result == expected);
        std::cout << "✓ Simple fields test passed" << std::endl;
    }
    
    // 测试用例 2: 嵌套对象
    {
        std::string input = "user { id: 1 name: \"Alice\" }";
        std::string expected = "{\"user\":{\"id\":1,\"name\":\"Alice\"}}";
        std::string result = protobufDebugStringToJson(input);
        assert(result == expected);
        std::cout << "✓ Nested object test passed" << std::endl;
    }
    
    // 测试用例 3: 布尔值
    {
        std::string input = "active: true verified: false";
        std::string expected = "{\"active\":true,\"verified\":false}";
        std::string result = protobufDebugStringToJson(input);
        assert(result == expected);
        std::cout << "✓ Boolean values test passed" << std::endl;
    }
    
    // 测试用例 4: 混合类型
    {
        std::string input = "count: 42 ratio: 3.14 message: \"Hello World\"";
        std::string expected = "{\"count\":42,\"ratio\":3.14,\"message\":\"Hello World\"}";
        std::string result = protobufDebugStringToJson(input);
        assert(result == expected);
        std::cout << "✓ Mixed types test passed" << std::endl;
    }
    
    // 测试用例 5: 多层嵌套
    {
        std::string input = "data { user { id: 1 profile { age: 25 } } }";
        std::string expected = "{\"data\":{\"user\":{\"id\":1,\"profile\":{\"age\":25}}}}";
        std::string result = protobufDebugStringToJson(input);
        assert(result == expected);
        std::cout << "✓ Multi-level nesting test passed" << std::endl;
    }
}

int main() {
    std::cout << "Running unit tests for protobufDebugStringToJson..." << std::endl;
    std::cout << "====================================================" << std::endl;
    
    // 运行主要测试
    testUserConversion();
    
    std::cout << "\nRunning additional test cases..." << std::endl;
    std::cout << "---------------------------------" << std::endl;
    
    // 运行额外测试用例
    testAdditionalCases();
    
    std::cout << "\n✓ All tests passed successfully!" << std::endl;
    
    return 0;
}