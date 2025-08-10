#include <iostream>
#include <google/protobuf/message.h>
#include <google/protobuf/util/json_util.h>
#include "protobuf_to_json.cpp"

// 更推荐的方法：使用 protobuf 官方的 JSON 转换功能
std::string protobufToJsonOfficial(const google::protobuf::Message& message) {
    std::string json_string;
    google::protobuf::util::JsonPrintOptions options;
    options.add_whitespace = true;
    options.always_print_primitive_fields = true;
    options.preserve_proto_field_names = true;
    
    auto status = google::protobuf::util::MessageToJsonString(message, &json_string, options);
    
    if (status.ok()) {
        return json_string;
    } else {
        return "Error converting to JSON: " + status.ToString();
    }
}

int main() {
    // 示例1：使用自定义函数转换 ShortDebugString
    std::string debugStr = "name: \"John\" age: 30 address { street: \"Main St\" number: 123 }";
    std::string json = protobufDebugStringToJson(debugStr);
    std::cout << "Custom conversion:\n" << json << std::endl;
    
    // 示例2：更复杂的例子
    std::string complexDebugStr = "users { id: 1 name: \"Alice\" active: true } users { id: 2 name: \"Bob\" active: false } count: 2";
    std::string complexJson = protobufDebugStringToJson(complexDebugStr);
    std::cout << "\nComplex example:\n" << complexJson << std::endl;
    
    // 注意：如果你有实际的 protobuf Message 对象，建议使用官方的 MessageToJsonString
    // YourProtoMessage message;
    // std::string officialJson = protobufToJsonOfficial(message);
    
    return 0;
}