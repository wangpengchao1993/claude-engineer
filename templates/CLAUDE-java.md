# CLAUDE.md — Java Project Template / Java 项目模板

> Copy this to your Java project root and customize.
> 将此文件复制到 Java 项目根目录并进行自定义。

## Project Overview / 项目概述

<!-- Describe your project / 描述你的项目 -->
[Project Name] is a [Java application/microservice/library] that [primary function].

## Tech Stack / 技术栈

- **Java**: [17 LTS / 21 LTS]
- **Framework / 框架**: [Spring Boot 3.x / Quarkus / Micronaut / None]
- **Build Tool / 构建工具**: [Maven / Gradle]
- **Database / 数据库**: [PostgreSQL / MySQL / MongoDB / None]
- **ORM**: [Spring Data JPA (Hibernate) / MyBatis / jOOQ / None]
- **Cache / 缓存**: [Redis / Caffeine / None]
- **Message Queue / 消息队列**: [Kafka / RabbitMQ / None]
- **Testing / 测试**: JUnit 5 + Mockito + [Testcontainers / H2]
- **Linting / 代码检查**: [Checkstyle / PMD / SpotBugs]
- **Formatting / 代码格式化**: [google-java-format / Spotless]
- **API Docs / API 文档**: [SpringDoc OpenAPI / Swagger]

## Commands / 常用命令

### Maven

```bash
# Build / 构建
mvn clean compile                        # Compile / 编译
mvn clean package                        # Build JAR / 打包 JAR
mvn clean package -DskipTests            # Build without tests / 跳过测试打包
mvn clean install                        # Install to local repo / 安装到本地仓库

# Testing / 测试
mvn test                                 # Run all tests / 运行所有测试
mvn test -Dtest="UserServiceTest"        # Run specific test class / 运行特定测试类
mvn test -Dtest="UserServiceTest#testCreate"  # Run specific method / 运行特定方法
mvn verify                               # Run integration tests / 运行集成测试
mvn jacoco:report                        # Generate coverage report / 生成覆盖率报告

# Code Quality / 代码质量
mvn checkstyle:check                     # Run Checkstyle / 代码风格检查
mvn spotbugs:check                       # Run SpotBugs / Bug 检测
mvn pmd:check                            # Run PMD / 静态分析
mvn spotless:apply                       # Auto-format code / 自动格式化

# Run / 运行
mvn spring-boot:run                      # Start Spring Boot (dev) / 启动 Spring Boot
mvn spring-boot:run -Dspring-boot.run.profiles=dev  # With profile / 指定配置

# Dependencies / 依赖
mvn dependency:tree                      # Show dependency tree / 显示依赖树
mvn versions:display-dependency-updates  # Check for updates / 检查更新
```

### Gradle (alternative / 替代方案)

```bash
./gradlew build                          # Build / 构建
./gradlew test                           # Run tests / 运行测试
./gradlew bootRun                        # Start Spring Boot / 启动
./gradlew dependencies                   # Dependency tree / 依赖树
./gradlew spotlessApply                  # Auto-format / 自动格式化
```

## Architecture / 项目架构

```
project/
├── pom.xml                    # Maven config / Maven 配置
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/company/project/
│   │   │       ├── Application.java       # Entry point / 启动类
│   │   │       ├── config/                # Configuration / 配置类
│   │   │       │   ├── SecurityConfig.java
│   │   │       │   └── WebConfig.java
│   │   │       ├── controller/            # REST endpoints / REST 接口
│   │   │       │   └── UserController.java
│   │   │       ├── service/               # Business logic / 业务逻辑
│   │   │       │   ├── UserService.java         # Interface / 接口
│   │   │       │   └── impl/
│   │   │       │       └── UserServiceImpl.java # Implementation / 实现
│   │   │       ├── repository/            # Data access / 数据访问
│   │   │       │   └── UserRepository.java
│   │   │       ├── model/                 # Entities / 实体
│   │   │       │   ├── entity/
│   │   │       │   │   └── User.java
│   │   │       │   ├── dto/               # Data Transfer Objects / 传输对象
│   │   │       │   │   ├── UserRequest.java
│   │   │       │   │   └── UserResponse.java
│   │   │       │   └── enums/
│   │   │       │       └── UserStatus.java
│   │   │       ├── exception/             # Custom exceptions / 自定义异常
│   │   │       │   ├── BusinessException.java
│   │   │       │   └── GlobalExceptionHandler.java
│   │   │       └── util/                  # Utilities / 工具类
│   │   └── resources/
│   │       ├── application.yml            # Main config / 主配置
│   │       ├── application-dev.yml        # Dev profile / 开发环境配置
│   │       ├── application-prod.yml       # Prod profile / 生产环境配置
│   │       └── db/migration/             # Flyway/Liquibase migrations / 数据库迁移
│   │           ├── V1__init.sql
│   │           └── V2__add_user_status.sql
│   └── test/
│       └── java/
│           └── com/company/project/
│               ├── controller/
│               │   └── UserControllerTest.java    # MockMvc tests / 接口测试
│               ├── service/
│               │   └── UserServiceTest.java       # Unit tests / 单元测试
│               ├── repository/
│               │   └── UserRepositoryTest.java    # @DataJpaTest / 数据库测试
│               └── integration/
│                   └── UserIntegrationTest.java   # @SpringBootTest / 集成测试
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
└── docs/
```

## Code Conventions / 编码规范

### Core Principles / 核心原则

- **Prefer `final` by default / 默认用 `final`** — variables, parameters, fields should be `final` unless reassigned
- **Use `Optional` for nullable returns / 可空返回值用 `Optional`** — never return `null` from public methods
- **Use Records for DTOs / DTO 用 Record** — `record UserResponse(Long id, String name) {}`
- **Constructor injection only / 仅用构造器注入** — no `@Autowired` on fields
- **Interface-first for services / 服务先定义接口** — `UserService` (interface) + `UserServiceImpl`
- **Validate at boundaries / 在边界处校验** — use `@Valid` + Bean Validation on controller inputs
- **Use Stream API for collections / 集合操作用 Stream** — avoid manual loops for filter/map/reduce
- **Exceptions for exceptional cases / 异常用于异常情况** — not for flow control
- **Immutable objects preferred / 优先不可变对象** — Records, `List.of()`, `Map.of()`

### Error Handling / 错误处理

```java
// ✅ Good / 好的做法: Custom exception + global handler
// 自定义异常 + 全局处理器
throw new BusinessException(ErrorCode.USER_NOT_FOUND, "User %d not found", userId);

// ❌ Bad / 不好的做法: Generic exceptions
throw new RuntimeException("User not found");

// ✅ Good / 好的做法: Optional for nullable queries
// 可空查询用 Optional
Optional<User> user = userRepository.findById(id);
return user.orElseThrow(() -> new BusinessException(ErrorCode.USER_NOT_FOUND));

// ❌ Bad / 不好的做法: Returning null
return userRepository.findById(id); // might be null!
```

### API Response Format / API 响应格式

```java
// Success / 成功
{ "code": 200, "data": { ... }, "message": "OK" }

// Error / 错误
{ "code": 40001, "data": null, "message": "User not found / 用户不存在" }
```

## Naming Conventions / 命名规范

| Element / 元素 | Convention / 规范 | Example / 示例 |
|----------------|-------------------|----------------|
| **Classes / 类** | PascalCase | `UserService`, `HttpClient` |
| **Interfaces / 接口** | PascalCase (no `I` prefix) | `UserRepository`, not `IUserRepository` |
| **Methods / 方法** | camelCase, verb-first | `getUserById`, `createOrder` |
| **Variables / 变量** | camelCase | `userName`, `orderCount` |
| **Constants / 常量** | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT` |
| **Packages / 包** | lowercase, reverse domain | `com.company.project.service` |
| **Enums / 枚举** | PascalCase class, UPPER values | `UserStatus.ACTIVE` |
| **Test classes / 测试类** | ClassNameTest | `UserServiceTest` |
| **Test methods / 测试方法** | should_ExpectedResult_When_Condition | `should_ThrowException_When_UserNotFound` |
| **DTOs / 传输对象** | EntityRequest / EntityResponse | `UserRequest`, `UserResponse` |

## Testing Conventions / 测试规范

```java
// Use descriptive test names / 使用描述性测试名称
@Test
@DisplayName("Should return user when valid ID provided / 当提供有效 ID 时应返回用户")
void should_ReturnUser_When_ValidIdProvided() {
    // Arrange / 准备
    var user = new User(1L, "Alice");
    when(userRepository.findById(1L)).thenReturn(Optional.of(user));

    // Act / 执行
    var result = userService.getUserById(1L);

    // Assert / 断言
    assertThat(result.name()).isEqualTo("Alice");
    verify(userRepository).findById(1L);
}
```

- **Unit tests**: `@ExtendWith(MockitoExtension.class)`, mock all dependencies / 单元测试 mock 所有依赖
- **Integration tests**: `@SpringBootTest` + `@Testcontainers` for real DB / 集成测试用 Testcontainers
- **Controller tests**: `@WebMvcTest` + `MockMvc` / 接口测试
- **Repository tests**: `@DataJpaTest` with H2 or Testcontainers / 数据库测试
- **Coverage target / 覆盖率目标**: 80% line coverage for service layer / service 层 80% 行覆盖

## Important Notes / 重要注意事项

- Never use field injection (`@Autowired` on fields) — use constructor injection / 不用字段注入，用构造器注入
- Never use raw types (`List` instead of `List<User>`) / 不用原始类型
- Never modify existing Flyway/Liquibase migration files / 不修改已有数据库迁移文件
- Never catch `Exception` or `Throwable` broadly — catch specific types / 不要笼统捕获 Exception
- Never put business logic in controllers — controllers only delegate to services / 不在 Controller 中放业务逻辑
- Never use `System.out.println` — use SLF4J logging (`log.info/debug/error`) / 不用 println，用 SLF4J
- Always close resources with try-with-resources / 总是用 try-with-resources 关闭资源
- Always use parameterized queries (JPA/MyBatis) — never concatenate SQL / 总是用参数化查询
- Always set `spring.jpa.open-in-view=false` in production / 生产环境关闭 open-in-view
- Environment variables loaded via `application.yml` + `@ConfigurationProperties` / 配置用 ConfigurationProperties
