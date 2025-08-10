# Protobuf ShortDebugString to JSON Converter

将 Protocol Buffers 的 ShortDebugString 输出转换为 JSON 格式的 C++ 函数。

## 功能

`protobufDebugStringToJson` 函数可以将 protobuf 的 debug string 格式转换为标准 JSON：

```cpp
// 输入: name: "John" age: 30 address { street: "Main St" number: 123 }
// 输出: {"name":"John","age":30,"address":{"street":"Main St","number":123}}
```

## 使用方法

```cpp
#include "protobuf_to_json.cpp"

std::string debugStr = "name: \"John\" age: 30";
std::string json = protobufDebugStringToJson(debugStr);
```

## 编译

如果使用官方 protobuf 库：
```bash
g++ -std=c++11 example.cpp -lprotobuf -o example
```

仅使用自定义转换函数：
```bash
g++ -std=c++11 protobuf_to_json.cpp your_code.cpp -o your_program
```

## 注意事项

- 这个函数是基于文本解析的简单实现
- 如果你有实际的 protobuf Message 对象，建议使用 `google::protobuf::util::MessageToJsonString`
- 该函数处理基本类型、嵌套对象、数组等常见情况，但可能无法处理所有边缘情况