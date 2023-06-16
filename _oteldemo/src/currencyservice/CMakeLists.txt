cmake_minimum_required(VERSION 3.1)
project(currency-service)

find_package(Protobuf REQUIRED)
find_package(gRPC CONFIG REQUIRED)
find_package(opentelemetry-cpp CONFIG REQUIRED)

set(PROTO_PATH "${CMAKE_CURRENT_SOURCE_DIR}/proto")
set(GENERATED_PROTOBUF_PATH "${CMAKE_BINARY_DIR}/generated/proto")
set(GENERATED_HEALTH_PROTOBUF_PATH "${GENERATED_PROTOBUF_PATH}/grpc/health/v1")

file(MAKE_DIRECTORY "${GENERATED_PROTOBUF_PATH}")

set(DEMO_PROTO "${PROTO_PATH}/demo.proto")
set(DEMO_PB_CPP_FILE "${GENERATED_PROTOBUF_PATH}/demo.pb.cc")
set(DEMO_PB_H_FILE "${GENERATED_PROTOBUF_PATH}/demo.pb.h")
set(DEMO_GRPC_PB_CPP_FILE "${GENERATED_PROTOBUF_PATH}/demo.grpc.pb.cc")
set(DEMO_GRPC_PB_H_FILE "${GENERATED_PROTOBUF_PATH}/demo.grpc.pb.h")
set(HEALTH_PROTO "${PROTO_PATH}/grpc/health/v1/health.proto")
set(HEALTH_PB_CPP_FILE "${GENERATED_HEALTH_PROTOBUF_PATH}/health.pb.cc")
set(HEALTH_PB_H_FILE "${GENERATED_HEALTH_PROTOBUF_PATH}/health.pb.h")
set(HEALTH_GRPC_PB_CPP_FILE "${GENERATED_HEALTH_PROTOBUF_PATH}/health.grpc.pb.cc")
set(HEALTH_GRPC_PB_H_FILE "${GENERATED_HEALTH_PROTOBUF_PATH}/health.grpc.pb.h")

foreach(IMPORT_DIR ${PROTOBUF_IMPORT_DIRS})
  list(APPEND PROTOBUF_INCLUDE_FLAGS "-I${IMPORT_DIR}")
endforeach()

find_program(gRPC_CPP_PLUGIN_EXECUTABLE grpc_cpp_plugin)

add_custom_command(
    OUTPUT ${DEMO_PB_H_FILE}
           ${DEMO_PB_CPP_FILE}
           ${DEMO_GRPC_PB_CPP_FILE}
           ${DEMO_GRPC_PB_H_FILE}
           ${HEALTH_PB_H_FILE}
           ${HEALTH_PB_CPP_FILE}
           ${HEALTH_GRPC_PB_CPP_FILE}
           ${HEALTH_GRPC_PB_H_FILE}

    COMMAND
      ${PROTOBUF_PROTOC_EXECUTABLE} ARGS "--experimental_allow_proto3_optional"
      "--proto_path=${PROTO_PATH}" ${PROTOBUF_INCLUDE_FLAGS}
      "--cpp_out=${GENERATED_PROTOBUF_PATH}"
      "--grpc_out=generate_mock_code=true:${GENERATED_PROTOBUF_PATH}"
      --plugin=protoc-gen-grpc="${gRPC_CPP_PLUGIN_EXECUTABLE}" ${DEMO_PROTO} ${HEALTH_PROTO})

message(STATUS "gRPC_CPP_PLUGIN_EXECUTABLE=${gRPC_CPP_PLUGIN_EXECUTABLE}")

add_library(demo-proto ${DEMO_PB_H_FILE}
           ${DEMO_PB_CPP_FILE}
           ${DEMO_GRPC_PB_CPP_FILE}
           ${DEMO_GRPC_PB_H_FILE}
           ${HEALTH_PB_H_FILE}
           ${HEALTH_PB_CPP_FILE}
           ${HEALTH_GRPC_PB_CPP_FILE}
           ${HEALTH_GRPC_PB_H_FILE})

target_link_libraries(demo-proto gRPC::grpc++ protobuf::libprotobuf)
include_directories("${GENERATED_PROTOBUF_PATH}" "${OPENTELEMETRY_CPP_INCLUDE_DIRS}")

add_executable(currencyservice src/server.cpp)
add_dependencies(currencyservice demo-proto)
target_link_libraries(
    currencyservice demo-proto protobuf::libprotobuf
     ${OPENTELEMETRY_CPP_LIBRARIES} opentelemetry_trace opentelemetry_common 
     opentelemetry_exporter_otlp_grpc opentelemetry_exporter_otlp_grpc_client 
     opentelemetry_proto opentelemetry_otlp_recordable opentelemetry_resources 
     opentelemetry_metrics opentelemetry_exporter_otlp_grpc_metrics gRPC::grpc++)

install(TARGETS currencyservice DESTINATION bin)
