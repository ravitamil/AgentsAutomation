---
applyTo: "**/pom.xml"
description: "Maven configuration rules and dependency management standards for Java Playwright test automation projects."
---

# Maven Build & Dependency Standards

These rules apply whenever modifying, updating, or reviewing `pom.xml`.

## 1. Compiler Configuration (Java 17+)
Always configure the `maven-compiler-plugin` using the modern `--release 17` flag rather than legacy `-source` / `-target`:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.13.0</version>
    <configuration>
        <release>17</release>
    </configuration>
</plugin>
```

## 2. Core Dependencies & Versions
- **Playwright for Java**: `com.microsoft.playwright:playwright:1.47.0` (or latest stable)
- **JUnit 5 Jupiter**: `org.junit.jupiter:junit-jupiter:5.10.2`
- **AssertJ Core**: `org.assertj:assertj-core:3.25.3`

## 3. Surefire Test Runner Plugin
Ensure `maven-surefire-plugin` is configured with JUnit 5 Jupiter Platform provider:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>3.2.5</version>
    <configuration>
        <testFailureIgnore>false</testFailureIgnore>
        <redirectTestOutputToFile>false</redirectTestOutputToFile>
    </configuration>
</plugin>
```

## 4. Playwright CLI Exec Plugin (Trace Viewer Support)
Include `exec-maven-plugin` so engineers can easily launch the interactive Playwright Trace Viewer without external node installations:

```xml
<plugin>
    <groupId>org.codehaus.mojo</groupId>
    <artifactId>exec-maven-plugin</artifactId>
    <version>3.2.0</version>
</plugin>
```

*Command to inspect trace:*
```bash
mvn exec:java -e -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.args="show-trace target/traces/<TestName>-trace.zip"
```
