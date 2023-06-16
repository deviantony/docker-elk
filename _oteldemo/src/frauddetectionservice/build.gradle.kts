// Copyright The OpenTelemetry Authors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import org.jetbrains.kotlin.gradle.tasks.KotlinCompile
import com.google.protobuf.gradle.*

plugins {
    kotlin("jvm") version "1.7.20"
    application
    id("java")
    id("idea")
    id("com.google.protobuf") version "0.9.1"
    id("com.github.johnrengelman.shadow") version "7.1.2"
}

group = "io.opentelemetry"
version = "1.0"


val grpcVersion = "1.50.0"
val protobufVersion = "3.16.1"


repositories {
    mavenCentral()
    gradlePluginPortal()
}



dependencies {
    implementation("com.google.protobuf:protobuf-java:3.21.7")
    testImplementation(kotlin("test"))
    implementation(kotlin("script-runtime"))
    implementation("org.apache.kafka:kafka-clients:3.3.1")
    implementation("com.google.api.grpc:proto-google-common-protos:2.9.6")
    implementation("io.grpc:grpc-protobuf:${grpcVersion}")
    implementation("io.grpc:grpc-stub:${grpcVersion}")
    implementation("io.grpc:grpc-netty:${grpcVersion}")
    implementation("io.grpc:grpc-services:${grpcVersion}")
    implementation("io.opentelemetry:opentelemetry-api:1.19.0")
    implementation("io.opentelemetry:opentelemetry-sdk:1.19.0")
    implementation("io.opentelemetry:opentelemetry-extension-annotations:1.18.0")
    implementation("org.apache.logging.log4j:log4j-core:2.19.0")
    implementation("org.slf4j:slf4j-api:2.0.3")
    implementation("com.google.protobuf:protobuf-kotlin:3.21.8")

    if (JavaVersion.current().isJava9Compatible) {
        // Workaround for @javax.annotation.Generated
        // see: https://github.com/grpc/grpc-java/issues/3633
        implementation("javax.annotation:javax.annotation-api:1.3.1")
    }
}

tasks.test {
    useJUnitPlatform()
}

tasks.withType<KotlinCompile> {
    kotlinOptions.jvmTarget = "1.8"
}

protobuf {
    protoc {
        artifact = "com.google.protobuf:protoc:3.21.7"
    }
    plugins {

        id("grpc") {
            artifact = "io.grpc:protoc-gen-grpc-java:1.50.2"
        }
    }
    generateProtoTasks {
        ofSourceSet("main").forEach {
            it.plugins {
                // Apply the "grpc" plugin whose spec is defined above, without
                // options. Note the braces cannot be omitted, otherwise the
                // plugin will not be added. This is because of the implicit way
                // NamedDomainObjectContainer binds the methods.
                id("grpc") { }
            }
        }
    }
}

application {
    mainClass.set("frauddetectionservice.MainKt")
}

tasks.jar {
    manifest.attributes["Main-Class"] = "frauddetectionservice.MainKt"
}
