# CLAUDE.md — C++ Project Template / C++ 项目模板

> Copy this to your C++ project root and customize.
> 将此文件复制到 C++ 项目根目录并进行自定义。

## Project Overview / 项目概述

<!-- Describe your project / 描述你的项目 -->
[Project Name] is a [C++ application/library/service] that [primary function].

## Tech Stack / 技术栈

- **C++ Standard / C++ 标准**: [C++17 / C++20 / C++23]
- **Compiler / 编译器**: [GCC 13+ / Clang 16+ / MSVC 2022]
- **Build System / 构建系统**: CMake 3.25+
- **Package Manager / 包管理器**: [Conan 2.x / vcpkg / None]
- **Framework / 框架**: [Boost / Qt / gRPC / None]
- **Database / 数据库**: [PostgreSQL via libpq / SQLite / None]
- **Testing / 测试**: [Google Test / Catch2 / doctest]
- **Linting / 代码检查**: clang-tidy
- **Formatting / 代码格式化**: clang-format
- **Static Analysis / 静态分析**: [cppcheck / clang-analyzer]
- **Memory Analysis / 内存分析**: [AddressSanitizer / Valgrind]

## Commands / 常用命令

```bash
# Build / 构建
cmake -B build -DCMAKE_BUILD_TYPE=Release    # Configure release build / 配置 Release 构建
cmake --build build -j$(nproc)                # Build with all cores / 用所有核心构建
cmake -B build -DCMAKE_BUILD_TYPE=Debug       # Configure debug build / 配置 Debug 构建

# Testing / 测试
cd build && ctest --output-on-failure         # Run all tests / 运行所有测试
ctest -R "test_name"                          # Run specific test / 运行特定测试
ctest --rerun-failed                          # Re-run failed tests / 重跑失败测试

# Code Quality / 代码质量
clang-tidy src/**/*.cpp --fix                 # Lint and auto-fix / 检查并自动修复
clang-format -i src/**/*.cpp src/**/*.h       # Format code / 格式化代码
cppcheck --enable=all src/                    # Static analysis / 静态分析

# Sanitizers (Debug build) / 消毒器（Debug 构建）
cmake -B build -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_CXX_FLAGS="-fsanitize=address,undefined" # ASAN + UBSAN
cmake -B build -DCMAKE_BUILD_TYPE=Debug \
  -DCMAKE_CXX_FLAGS="-fsanitize=thread"             # TSAN (线程检测)

# Valgrind / 内存检测
valgrind --leak-check=full ./build/bin/myapp  # Memory leak check / 内存泄漏检测

# Package Manager / 包管理
conan install . --build=missing               # Install deps via Conan / Conan 安装依赖
vcpkg install                                  # Install deps via vcpkg / vcpkg 安装依赖

# Documentation / 文档
doxygen Doxyfile                               # Generate docs / 生成文档
```

## Architecture / 项目架构

```
project/
├── CMakeLists.txt         # Root CMake config / 根 CMake 配置
├── conanfile.txt          # Conan dependencies / Conan 依赖
├── .clang-tidy            # Lint rules / 检查规则
├── .clang-format          # Format rules / 格式规则
│
├── include/               # Public headers / 公共头文件
│   └── project/
│       ├── core.h         # Core module / 核心模块
│       ├── utils.h        # Utilities / 工具函数
│       └── types.h        # Shared types / 共享类型
│
├── src/                   # Source files / 源文件
│   ├── core/
│   │   ├── core.cpp
│   │   └── core_internal.h   # Internal headers / 内部头文件
│   ├── utils/
│   │   └── utils.cpp
│   └── main.cpp           # Entry point / 入口文件
│
├── tests/                 # Test files / 测试文件
│   ├── CMakeLists.txt
│   ├── test_core.cpp
│   └── test_utils.cpp
│
├── cmake/                 # CMake modules / CMake 模块
│   ├── CompilerWarnings.cmake
│   └── Sanitizers.cmake
│
├── third_party/           # Vendored deps / 第三方依赖（直接包含）
└── docs/                  # Documentation / 文档
```

## Code Conventions / 编码规范

### Core Principles / 核心原则

- **RAII everywhere / 到处使用 RAII** — resources are managed by objects, not manual new/delete
- **Smart pointers only / 仅用智能指针** — `std::unique_ptr` by default, `std::shared_ptr` only when truly shared
- **Const correctness / const 正确性** — `const` everything that doesn't need to change
- **No raw `new`/`delete`** — use `std::make_unique`, `std::make_shared`, containers
- **No C-style casts / 不用 C 风格转换** — use `static_cast`, `dynamic_cast`, `reinterpret_cast` (with comment)
- **Prefer references over pointers / 优先引用而非指针** — use pointers only when nullable
- **Use `std::string_view` for read-only strings / 只读字符串用 `string_view`**
- **Use `std::optional` for nullable values / 可空值用 `optional`**
- **Use `std::variant` over unions / 用 `variant` 替代 union**
- **Error handling / 错误处理**: [exceptions / `std::expected` (C++23) / error codes — pick one for the project]
- **Pass by value + move when appropriate / 适当时传值+移动**

### Formatting / 格式化

- Indent: 4 spaces (no tabs) / 4 空格缩进
- Line width: 120 characters / 行宽 120 字符
- Braces: Allman or K&R (pick one, be consistent) / 大括号风格保持一致
- `#pragma once` preferred over include guards / 优先用 `#pragma once`

### Includes / 头文件包含

```cpp
// Order / 顺序:
// 1. Corresponding header / 对应头文件
// 2. C++ standard library / C++ 标准库
// 3. Third-party headers / 第三方头文件
// 4. Project headers / 项目头文件

#include "project/core.h"       // 1. Corresponding
#include <string>               // 2. Standard
#include <vector>
#include <fmt/format.h>         // 3. Third-party
#include "project/utils.h"      // 4. Project
```

## Naming Conventions / 命名规范

| Element / 元素 | Convention / 规范 | Example / 示例 |
|----------------|-------------------|----------------|
| **Classes/Structs / 类/结构体** | PascalCase | `HttpServer`, `UserProfile` |
| **Functions/Methods / 函数/方法** | snake_case or camelCase (pick one) | `get_user_by_id` or `getUserById` |
| **Variables / 变量** | snake_case | `user_count`, `max_retries` |
| **Constants / 常量** | kCamelCase or UPPER_SNAKE | `kMaxConnections` or `MAX_CONNECTIONS` |
| **Macros / 宏** | UPPER_SNAKE_CASE | `PROJECT_VERSION`, `ENABLE_DEBUG` |
| **Namespaces / 命名空间** | snake_case | `project::core`, `project::utils` |
| **Template params / 模板参数** | PascalCase | `typename ValueType` |
| **Files / 文件** | snake_case | `http_server.cpp`, `user_profile.h` |
| **Member variables / 成员变量** | trailing underscore / 尾下划线 | `name_`, `connection_pool_` |
| **Enum values / 枚举值** | PascalCase | `Color::DarkRed` |

## Important Notes / 重要注意事项

- Never use `new`/`delete` directly — always use smart pointers or containers / 不要直接用 `new`/`delete`
- Never use C-style casts `(int)x` — use `static_cast<int>(x)` / 不用 C 风格转换
- Never ignore compiler warnings — treat as errors in CI (`-Werror`) / 不要忽略编译器警告
- Always enable sanitizers in Debug builds (ASAN, UBSAN, TSAN) / Debug 构建总是启用 sanitizers
- Always run `clang-tidy` before committing / 提交前总是运行 `clang-tidy`
- Never commit generated files (build/, CMakeCache.txt) / 不要提交生成文件
- Always write unit tests for new public functions / 新的公共函数总要写单元测试
- Use `[[nodiscard]]` on functions where ignoring return value is likely a bug / 返回值不应被忽略的函数用 `[[nodiscard]]`
- Prefer `constexpr` over `const` when value is known at compile time / 编译期已知的值用 `constexpr`
- Document all public APIs with Doxygen comments (`///`) / 所有公共 API 用 Doxygen 注释
